import streamlit as st
from db_interaction import ask, generate, execute, add_object, delete_object
import json

st.title("Charm-Query")

if 'question' not in st.session_state:
    st.session_state.question = ""
if 'query' not in st.session_state:
    st.session_state.query = ""

with st.form(key='ask_form'):
    input_text = st.text_input(label='Enter your question')
    submit_button = st.form_submit_button(label='Ask')
    generate_button = st.form_submit_button(label='Generate new')

    if submit_button:
        result = ask(input_text)
        if isinstance(result, dict):
            st.session_state.question = input_text
            st.session_state.data = result["data"]
            st.session_state.source = result["source"]
            st.session_state.query = result["query"]
            st.write("Source: ", st.session_state.source)
            st.write("Query: ", st.session_state.query)
        else:
            st.error(result)
    if generate_button:
        schema = execute("SELECT name, sql from sqlite_master WHERE type='table';")
        query = generate(input_text, json.dumps(schema))
        result = execute(query)
        if isinstance(result, list):
            st.session_state.data = result
            st.session_state.source = "generated"
            st.session_state.query = query
            st.write("Source: ", st.session_state.source)
            st.write("Query: ", st.session_state.query)

with st.form(key="query_form"):
    query_input = st.text_input(label='Edit your query', value=st.session_state.query)

    execute_button = st.form_submit_button(label='Execute')
    delete_button = st.form_submit_button(label="Delete query")

    if execute_button:
        result = execute(query_input)
        if isinstance(result, list):
            st.session_state.data = result
            st.session_state.source = "manual"
            st.session_state.query = query_input
            add_object(st.session_state.question, st.session_state.query)
            st.write("Source: ", st.session_state.source)
            st.write("Query: ", st.session_state.query)
        else:
            st.error(result)

    if delete_button:
        result = delete_object(query=st.session_state.query)
        st.write(result)

if 'data' in st.session_state:
    st.subheader("Results")
    st.table(st.session_state.data)