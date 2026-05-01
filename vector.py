import chromadb
import re
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords
from sentence_transformers import CrossEncoder
import nltk
from router import detect

nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="grad_catalog_v5", embedding_function=ef)

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

catalog = collection.get(include=["documents", "metadatas"])

def tokenize(text):
    return [w for w in text.lower().split() if w not in STOPWORDS]

corpus = [tokenize(doc) for doc in catalog["documents"]]
bm25 = BM25Okapi(corpus)

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

def bm25_search(text, n):
    tokens = tokenize(text)
    scores = bm25.get_scores(tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n]
    return {
        "documents": [[catalog["documents"][i] for i in top_indices]],
        "metadatas": [[catalog["metadatas"][i] for i in top_indices]],
        "distances": [[1 - scores[i] / (scores[top_indices[0]] + 1e-9) for i in top_indices]],
        "ids": [[catalog["ids"][i] for i in top_indices]]
    }

def rrf(results_list, k=60):
    scores = {}
    data = {}

    for results in results_list:
        for rank, (doc, meta, chunk_id) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["ids"][0]
        )):
            if chunk_id not in scores:
                scores[chunk_id] = 0
                data[chunk_id] = (doc, meta)
            scores[chunk_id] += 1 / (k + rank + 1)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    docs, metas, ids, distances = [], [], [], []
    for chunk_id, score in ranked:
        docs.append(data[chunk_id][0])
        metas.append(data[chunk_id][1])
        ids.append(chunk_id)
        distances.append(1 - score)

    return {
        "documents": [docs],
        "metadatas": [metas],
        "distances": [distances],
        "ids": [ids]
    }

def rerank(text, results, n):
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    ids = results["ids"][0]

    pairs = [(text, doc) for doc in docs]
    scores = cross_encoder.predict(pairs)

    ranked = sorted(zip(scores, docs, metas, ids), key=lambda x: x[0], reverse=True)[:n]
    ranked_scores, ranked_docs, ranked_metas, ranked_ids = zip(*ranked)
    return {
        "documents": [list(ranked_docs)],
        "metadatas": [list(ranked_metas)],
        "distances": [list(1 - s for s in ranked_scores)],
        "ids": [list(ranked_ids)]
    }

def extract_codes(text):
    return re.findall(r'\b[A-Z]{2,5}\s\d{3}\b', text)

def semantic(text, n):
    return collection.query(query_texts=[text], n_results=n)

def filter_by_code(code, text, n):
    return collection.query(
        query_texts=[text],
        where={"course_code": code},
        n_results=n
    )

def filter_by_type(chunk_type, text, n):
    return collection.query(
        query_texts=[text],
        where={"type": chunk_type},
        n_results=n
    )

def merge(results_list, n):
    seen = set()
    docs, metas, dists, ids = [], [], [], []

    for results in results_list:
        for doc, meta, dist, chunk_id in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
            results["ids"][0]
        ):
            if chunk_id not in seen:
                seen.add(chunk_id)
                docs.append(doc)
                metas.append(meta)
                dists.append(dist)
                ids.append(chunk_id)

    return {
        "documents": [docs[:n]],
        "metadatas": [metas[:n]],
        "distances": [dists[:n]],
        "ids": [ids[:n]]
    }

def query(text, n=3):
    codes = extract_codes(text)
    top = n * 5

    semantic_results = semantic(text, top)
    bm25_results = bm25_search(text, top)

    if codes:
        code_results = []
        for code in codes:
            try:
                r = filter_by_code(code, text, n)
                if r["documents"][0]:
                    code_results.append(r)
            except Exception:
                pass

        if code_results:
            fused = rrf([semantic_results, bm25_results])
            return merge(code_results + [fused], n)

    chunk_type = detect(text)[1]

    if chunk_type:
        type_results = filter_by_type(chunk_type, text, top)
        fused = rrf([semantic_results, bm25_results, type_results])
    else:
        fused = rrf([semantic_results, bm25_results])

    return rerank(text, fused, n)
