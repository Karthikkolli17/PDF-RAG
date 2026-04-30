import chromadb
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="grad_catalog_v5", embedding_function=ef)

def store(chunks):

    documents = []
    metadata = []
    ids = []

    for i, chunk in enumerate(chunks):

        documents.append(chunk["content"])
        meta = {k: v for k, v in chunk.items() if k != "content"}
        metadata.append(meta)
        ids.append(f"chunk_{i}")

    collection.add(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )
    print(f"Stored {len(documents)} chunks in ChromaDB")

def query(text, n=3):
    results = collection.query(
        query_texts=[text],
        n_results=n
    )

    return results