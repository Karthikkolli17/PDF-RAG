from pageSplitter import load
from chunking import semantic_chunk
from vector import store, query

pages = load("2025-2026 Student Handbook Final Copy_0.pdf")

doc_chunks = []

for page in pages:

    chunks = semantic_chunk(page["text"])

    for chunk in chunks:
        doc_chunks.append({
            "page": page["page"],
            "content": chunk.strip()
        })

store(doc_chunks)

results = query("academic probation GPA requirements")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"Page {meta['page']}: {doc[:200]}")
    print("*&*&*&*&")

# print(f"Total chunks from first 5 pages: {len(doc_chunks)}")
# for chunk in doc_chunks:
#     print(f"Page {chunk['page']}:\n{chunk['content'][:150]}")