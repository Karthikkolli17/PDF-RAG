from pageSplitter import load
from chunking import semantic_chunk, descriptions
from classifier import classify
from vector import store, query
from metadata import extract_descp_metadata, extract_curriculum_metadata
import json

pages = load("IIT Graduate Catalog 2024-2025_final.pdf")

doc_chunks = []

for page in pages:

    text = page["text"]
    num = page["page"]
    label = classify(text)

    if label in ("skip","toc"):
        continue
    elif label == "descriptive":
        chunks = descriptions(text)
    elif label == "curriculum":
        chunks = [text]
    else:
        chunks = semantic_chunk(text)

    for chunk in chunks:
        meta = {"page": num, "type": label}

        if label == "descriptive":
            meta.update(extract_descp_metadata(chunk))
        elif label == "curriculum":
            meta.update(extract_curriculum_metadata(chunk))

        doc_chunks.append({
            "content": chunk.strip(),
            **meta
        })

doc_chunks = [c for c in doc_chunks if len(c['content']) > 100]

# forward fill program for consecutive curriculum pages
last_program = None
last_page = None
for c in doc_chunks:
    if c['type'] == 'curriculum':
        if 'program' in c:
            last_program = c['program']
            last_page = c['page']
        elif last_program and last_page and c['page'] - last_page <= 1:
            c['program'] = last_program
        last_page = c['page']

curriculum = [c for c in doc_chunks if c['type'] == 'curriculum']
no_program = [c for c in curriculum if 'program' not in c]
print(f"Curriculum without program: {len(no_program)} out of {len(curriculum)}")

with open("chunks.json", "w") as f:
    json.dump(doc_chunks, f, indent=2)

store(doc_chunks)
print(f"Total chunks stored: {len(doc_chunks)}")


# results = query("What is the GRE waiver policy?")
# for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
#     print(f"Page {meta['page']} ({meta['type']}):\n{doc[:300]}")
#     print("*#**#*##*")

# results = query("What are the GPA requirements for graduate admission?")
# for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
#     print(f"Page {meta['page']}: {doc[:200]}")
#     print("*&*&*&*&")



# print(f"Total chunks from first 5 pages: {len(doc_chunks)}")
# for chunk in doc_chunks:
#     print(f"Page {chunk['page']}:\n{chunk['content'][:150]}")