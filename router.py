import numpy as np
from sentence_transformers import SentenceTransformer
from questions import questions

model = SentenceTransformer("all-MiniLM-L6-v2")

INTENT = {
    "topic_search": "descriptive",
    "program_requirements": "curriculum",
    "policy": "prose",
    "admission": "prose",
    "financial": "prose",
    "general": None,
}

prototype_embeddings = {
    intent: model.encode(examples, normalize_embeddings=True)
    for intent, examples in questions.items()
}

def detect(text):
    query_embedding = model.encode([text], normalize_embeddings=True)[0]
    scores = {
        intent: float(np.mean(query_embedding @ embs.T))
        for intent, embs in prototype_embeddings.items()
    }
    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    # only route if confident enough
    if best_score < 0.25:
        return "general", None

    chunk_type = INTENT[best_intent]
    return best_intent, chunk_type
