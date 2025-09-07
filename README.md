# RAG Terminal UI

This project has two parts:

1. **Backend (rag-api)** – FastAPI service that:
   - Stores & queries documents in ChromaDB
   - Encodes queries using SentenceTransformers
   - Sends queries with context to LLaMA (Together API)

2. **Frontend (rag-ui)** – Flask web UI with a Matrix-style terminal:
   - Select a project
   - Chat with the AI using project context
   - Simple cyberpunk design

---

## Backend Setup (rag-api)

### Install requirements
```bash
pip install fastapi uvicorn sentence-transformers chromadb requests
```

### Run backend
```bash
cd rag_git
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

API runs at:  
http://127.0.0.1:8001

### Example query
```bash
curl -X POST "http://127.0.0.1:8001/ask/my_project"   -H "Content-Type: application/json"   -d '{"query": "explain login logic?"}'
```

---

## Frontend Setup (rag-ui)

### Install requirements
```bash
pip install flask requests
```

### Run frontend
```bash
cd rag_git/rag-ui
python app.py
```

UI runs at:  
http://127.0.0.1:5000

---

## Connecting UI to API

In `rag-ui/app.py`:

```python
API_BASE_URL = "http://127.0.0.1:8001"
```

Change if your backend runs elsewhere.

IMPORTANT NOTE: Preferably run as docker

---



