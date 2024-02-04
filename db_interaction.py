import chromadb
import os
import uuid
import sqlite3
from openai import OpenAI
import json

gpt = OpenAI()
client = chromadb.PersistentClient(path="./chroma")
collection = client.get_or_create_collection(name=os.environ.get("DB_COLLECTION_NAME", "default"))

def add_object(question: str, query: str):
    try:
        collection.add(
            documents=[question],
            metadatas=[{"query": query}],
            ids=[str(uuid.uuid4())]
        )
    except Exception as e:
        return f"Error when adding objects: {e}"
    
def generate(question: str, schema: str):
    try:
        completion = gpt.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You should translate all questions to valid SQLite queries. You should provide ONLY SQL code, without formatting or explanations. For assistance, here is the schema: {schema}"},
                {"role": "user", "content": f"{question}. Provide only SQLite code"}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error when calling openai for generation: {e}"

def execute(query: str):
    try:
        conn = sqlite3.connect(os.environ.get("DB_PATH", "sample.sqlite")) 
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        column_names = [column[0] for column in c.description]
        conn.commit()
        conn.close()
        return [dict(zip(column_names, row)) for row in rows]
    except Exception as e:
        return f"Error when executing: {e}"

def find_query(question: str):
    try:
        result = collection.query(
            query_texts=[question],
            n_results=1,
        )
        if result['distances'][0][0] <= 0.11:
            return result['metadatas'][0][0]['query'], "db"
    except Exception as e:
        return f"Error when trying to query the db for similar queries: {e}"
    try:
        schema = execute("SELECT name, sql from sqlite_master WHERE type='table';")
        query = generate(question, json.dumps(schema))
        return query, "generated"
    except Exception as e:
        return f"Error when generating a query: {e}"

def ask(question: str):
    query = ""
    try:
        query, source = find_query(question)
    except Exception as e:
        return f"Error when searching for query: {e}"
    try:
        result = execute(query)
        add_object(question, query)
        return {
            "data": result,
            "source": source,
            "query": query
        }
    except Exception as e:
        return f"Error when executing the query or adding it: {e}"
    
def delete_object(query: str):
    try:
        collection.delete(where={"query": query})
        return f"Query {query} has been succesffully deleted"
    except Exception as e:
        return f"Error {e} when deleting the query: {query}"