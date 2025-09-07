from fastapi import FastAPI, Body
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import requests

app = FastAPI()

embedder = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = PersistentClient(path=".chromadb")

class Question(BaseModel):
    query: str

LLAMA_ENDPOINT = "https://api.together.xyz/v1/chat/completions"
LLAMA_API_KEY = "a2913ee8affa530183c194efaaaeb74a8c0580738efc2118d1d983a122a5a70b"

@app.post("/ask/{project}")
def ask_project(project: str, query: Question = Body(...)):
    try:
        collection = chroma_client.get_or_create_collection(project)
    except Exception as e:
        return {"error": f"Failed to load collection: {e}"}

    query_embedding = embedder.encode([query.query])[0].tolist()

    try:
        result = collection.query(query_embeddings=[query_embedding], n_results=1)
        context = result["documents"][0][0]
    except (IndexError, KeyError):
        return {"answer": "Sorry, I couldn't find any relevant information in the project."}

    prompt = (
        f"You are in a RAG-based setup. Answer the user question based only on the context.\n\n"
        f"Context: {context}\n\n"
        f"Question: {query.query}"
    )

    llama_payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant in a RAG-based setup."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLAMA_API_KEY}"
    }

    try:
        response = requests.post(LLAMA_ENDPOINT, json=llama_payload, headers=headers)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        try:
            error_text = response.text
        except:
            error_text = str(e)
        answer = f"(Fallback) Context: {context}\n\nLLaMA error: {error_text}"

    return {"answer": answer}
