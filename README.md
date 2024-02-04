## Charm Query (python version)
This repository contains all the code to run a lightweight demo version to test a hypothesis which I describe here: 
*In short: translating plain English to SQL*
### Quickstart:
- Clone the repo
- Run:
```bash
pip install -r requirements.txt
streamlit run main.py
```
It should work for Python >= 3.7, though for lower versions it must be fine as well.
- Navigate to http://localhost:8501
- Enjoy!

This version has limited functionality but it offers just enough to experience the idea behind it. 
For a more error-prone version please see the Go microservice:

The following application uses the following stack: 
- Streamlit frontend
- Sqlite only
- Chroma DB with L2 distance to calculate similarity
- MiniLM is used for embeddings (works well only for English)
