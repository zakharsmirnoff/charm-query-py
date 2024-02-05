## Charm Query (python version)
This repository contains all the code to run a lightweight demo version to test a hypothesis which I describe here: 
*In short: translating plain English to SQL with the help of vector search*

### Demo
[streamlit-main-2024-02-05-13-02-80.webm](https://github.com/zakharsmirnoff/charm-query-py/assets/89240654/dc573bbb-23b7-461f-a4ec-e05b385d4161)
### Quickstart:
- Clone the repo
- Set environment variables:
```bash
export OPENAI_API_KEY=<your openai_key>
export DB_PATH=<full path to sqlite file>
export DB_COLLECTION_NAME=<the name of your db which will create a collection with the same name in chroma db> # optional, if you don't specify, it will be set to 'default'. If you plan to test multiple databases, you'd better set this variable
```
- Run:
```bash
pip install -r requirements.txt
streamlit run main.py
```
It should work for Python >= 3.7, though for lower versions it must be fine as well.
- Navigate to http://localhost:8501
- Enjoy!

This version has limited functionality but it offers just enough to experience the idea behind it. 
For a more error-prone version please see the Go microservice: https://github.com/zakharsmirnoff/charm-query/

The application uses the following stack: 
- Streamlit frontend
- Sqlite only
- Chroma DB with L2 distance to calculate similarity
- MiniLM is used for embeddings (works well only for English)
