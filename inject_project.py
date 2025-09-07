import os
import json
import git
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

GITHUB_REPO_URL = "https://github.com/navuy/Helping_Hands.git"  # Replace with actual repo
CLONE_DIR = "repo_clone"
EMBEDDABLE_EXTENSIONS = {'.py', '.js', '.html', '.css', '.ts', '.tsx', '.jsx', '.json', '.md'}

if os.path.exists(CLONE_DIR):
    print(f"Removing old clone at {CLONE_DIR}")
    import shutil
    shutil.rmtree(CLONE_DIR)

print(f"Cloning {GITHUB_REPO_URL} into {CLONE_DIR}")
git.Repo.clone_from(GITHUB_REPO_URL, CLONE_DIR)

file_chunks = []
for root, dirs, files in os.walk(CLONE_DIR):
    for file in files:
        if any(file.endswith(ext) for ext in EMBEDDABLE_EXTENSIONS):
            full_path = os.path.join(root, file)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if content.strip():  # Avoid empty files
                        file_chunks.append({
                            "id": full_path.replace("/", "_"),  # Unique ID
                            "content": f"File: {full_path}\n\n{content}",
                            "filepath": full_path
                        })
            except Exception as e:
                print(f"Error reading {full_path}: {e}")

print(f"Collected {len(file_chunks)} files for embedding.")

embedder = SentenceTransformer("all-MiniLM-L6-v2")
texts = [chunk["content"] for chunk in file_chunks]
ids = [chunk["id"] for chunk in file_chunks]
embeddings = embedder.encode(texts).tolist()

chroma_client = PersistentClient(path=".chromadb")
collection = chroma_client.get_or_create_collection(name="project")

collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=ids,
    metadatas=[{"filepath": chunk["filepath"]} for chunk in file_chunks]
)

print("Injection completed into ChromaDB.")
