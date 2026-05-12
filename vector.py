import re
import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords
from sentence_transformers import CrossEncoder
import nltk

nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="grad_catalog_v6", embedding_function=ef)
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

catalog = collection.get(include=["documents", "metadatas"])


def tokenize(text):
    return [w for w in text.lower().split() if w not in STOPWORDS]


corpus = [tokenize(doc) for doc in catalog["documents"]]
bm25 = BM25Okapi(corpus) if corpus else None


def store(chunks):
    documents, metadata, ids = [], [], []
    for i, chunk in enumerate(chunks):
        documents.append(chunk["content"])
        metadata.append({k: v for k, v in chunk.items() if k != "content"})
        ids.append(f"chunk_{i}")
    collection.add(documents=documents, metadatas=metadata, ids=ids)
    print(f"Stored {len(documents)} chunks in ChromaDB")


def empty():
    return {"documents": [[]], "metadatas": [[]], "distances": [[]], "ids": [[]]}


def semantic(text, n, where=None):
    kwargs = {"query_texts": [text], "n_results": n}
    if where:
        kwargs["where"] = where
    return collection.query(**kwargs)


def bm25_search(text, n):
    if bm25 is None:
        return empty()
    tokens = tokenize(text)
    scores = bm25.get_scores(tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n]
    if not top_indices:
        return empty()
    top_score = scores[top_indices[0]] or 1e-9
    return {
        "documents": [[catalog["documents"][i] for i in top_indices]],
        "metadatas": [[catalog["metadatas"][i] for i in top_indices]],
        "distances": [[1 - scores[i] / top_score for i in top_indices]],
        "ids": [[catalog["ids"][i] for i in top_indices]],
    }


def rrf(results_list, k=60):
    scores, data = {}, {}
    for results in results_list:
        for rank, (doc, meta, cid) in enumerate(zip(
            results["documents"][0], results["metadatas"][0], results["ids"][0]
        )):
            if cid not in scores:
                scores[cid] = 0
                data[cid] = (doc, meta)
            scores[cid] += 1 / (k + rank + 1)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    docs, metas, ids, dists = [], [], [], []
    for cid, score in ranked:
        docs.append(data[cid][0])
        metas.append(data[cid][1])
        ids.append(cid)
        dists.append(1 - score)
    return {"documents": [docs], "metadatas": [metas], "distances": [dists], "ids": [ids]}


def rerank(text, results, n):
    docs = results["documents"][0]
    if not docs:
        return results
    metas, ids = results["metadatas"][0], results["ids"][0]
    pairs = [(text, doc) for doc in docs]
    scores = cross_encoder.predict(pairs)
    ranked = sorted(zip(scores, docs, metas, ids), key=lambda x: x[0], reverse=True)[:n]
    s, d, m, i = zip(*ranked)
    return {"documents": [list(d)], "metadatas": [list(m)], "distances": [[1 - x for x in s]], "ids": [list(i)]}


def merge_unique(results_list, n):
    seen = set()
    docs, metas, dists, ids = [], [], [], []
    for r in results_list:
        for doc, meta, dist, cid in zip(
            r["documents"][0], r["metadatas"][0], r["distances"][0], r["ids"][0]
        ):
            if cid in seen:
                continue
            seen.add(cid)
            docs.append(doc); metas.append(meta); dists.append(dist); ids.append(cid)
    return {"documents": [docs[:n]], "metadatas": [metas[:n]], "distances": [dists[:n]], "ids": [ids[:n]]}


INTENT_TYPE = {
    "course_lookup": "descriptive",
    "topic_search": "descriptive",
    "program_requirements": "curriculum",
    "admission": "prose",
    "policy": "prose",
    "financial": "prose",
    "definition": None,
    "comparison": None,
}


def normalize_program(p):
    p = " " + p.lower().strip() + " "
    # canonicalize all master's-degree phrasings to "master of" — covers
    # "MS X", "MS in X", "Master of X", "Master in X", and the catalog's own
    # "Master of Science in X" phrasing (which is identical in meaning).
    p = re.sub(
        r'\b(master of science(?:\s+in)?|m\.?s\.?(?:\s+in)?|master of|master in)\b',
        'master of', p,
    )
    p = re.sub(
        r'\b(ph\.?d\.?(?:\s+in)?|doctor of philosophy(?:\s+in)?|doctor of)\b',
        'doctor of philosophy in', p,
    )
    p = re.sub(r'\s+', ' ', p)
    return p.strip()


def curriculum_by_program(planner_program, top):
    # match against the program metadata only — matching against doc body catches
    # body mentions like "Architectural Engineering" when the user asked for "Architecture"
    needle = normalize_program(planner_program)
    if not needle:
        return None
    keep = []
    for doc, meta, cid in zip(catalog["documents"], catalog["metadatas"], catalog["ids"]):
        if meta.get("type") != "curriculum":
            continue
        hay = normalize_program(meta.get("program", ""))
        if not hay:
            continue
        if needle in hay or hay in needle:
            keep.append((doc, meta, cid))
    if not keep:
        return None
    return {
        "documents": [[k[0] for k in keep[:top]]],
        "metadatas": [[k[1] for k in keep[:top]]],
        "ids": [[k[2] for k in keep[:top]]],
        "distances": [[0.0] * min(len(keep), top)],
    }


def query(text, plan_dict=None, n=3):
    if plan_dict is None:
        fused = rrf([semantic(text, n * 5), bm25_search(text, n * 5)])
        return rerank(text, fused, n)

    intent = plan_dict.get("intent", "definition")
    course_codes = plan_dict.get("course_codes", [])
    departments = plan_dict.get("departments", [])
    programs = plan_dict.get("programs", [])

    if intent in ("admission", "program_requirements"):
        n = max(n, 5)
    top = n * 5

    if course_codes:
        code_results = []
        for code in course_codes:
            try:
                r = semantic(text, n, where={"course_code": code})
                if r["documents"][0]:
                    code_results.append(r)
            except Exception:
                pass
        if code_results:
            if intent == "comparison":
                picks_docs, picks_metas, picks_ids = [], [], []
                for cr in code_results:
                    if cr["documents"][0]:
                        picks_docs.append(cr["documents"][0][0])
                        picks_metas.append(cr["metadatas"][0][0])
                        picks_ids.append(cr["ids"][0][0])
                return {
                    "documents": [picks_docs],
                    "metadatas": [picks_metas],
                    "ids": [picks_ids],
                    "distances": [[0.0] * len(picks_docs)],
                }
            fused = rrf([semantic(text, top), bm25_search(text, top)])
            return merge_unique(code_results + [fused], n)

    if intent == "admission" and departments:
        dept = departments[0]
        try:
            dept_results = semantic(
                text, min(top, 10),
                where={"$and": [{"type": {"$eq": "prose"}}, {"department": {"$eq": dept}}]},
            )
            if dept_results["documents"][0]:
                return rerank(text, dept_results, n)
        except Exception:
            pass

    if intent == "program_requirements" and programs:
        prog_filtered = curriculum_by_program(programs[0], top)
        if prog_filtered:
            # trust the metadata filter — reranking against other curricula buries the right chunks
            return rerank(text, prog_filtered, n)
        type_r = semantic(text, top, where={"type": "curriculum"})
        sem = semantic(text, top)
        bm = bm25_search(text, top)
        fused = rrf([type_r, sem, bm])
        return rerank(text, fused, n)

    if intent == "topic_search":
        type_r = semantic(text, top, where={"type": "descriptive"})
        sem = semantic(text, top)
        fused = rrf([type_r, type_r, sem])
        return rerank(text, fused, n)

    chunk_type = INTENT_TYPE.get(intent)
    if chunk_type:
        type_r = semantic(text, top, where={"type": chunk_type})
        sem = semantic(text, top)
        bm = bm25_search(text, top)
        fused = rrf([sem, bm, type_r])
        return rerank(text, fused, n)

    fused = rrf([semantic(text, top), bm25_search(text, top)])
    return rerank(text, fused, n)
