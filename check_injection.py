from chromadb import PersistentClient

# Connect to ChromaDB persistent storage
client = PersistentClient(path=".chromadb")

# Get the 'family' collection
collection = client.get_collection("project")

# Print total number of documents
print(f"✅ Total documents: {collection.count()}")

# Fetch all documents (optional: limit or use filters)
data = collection.get()

# Display each document's ID and content
for doc_id, content in zip(data["ids"], data["documents"]):
    print(f"\n🆔 ID: {doc_id}\n📄 Content: {content}")
