# IIT Graduate Catalog Assistant

A question answering system over the Illinois Institute of Technology Graduate Catalog 2024-2025 (a 618-page PDF).

It uses page-type-aware chunking, an LLM that turns the user's question into a structured query plan, hybrid retrieval (semantic + BM25 with RRF fusion and cross-encoder reranking), and an answer generator that verifies its own page citations against what was actually retrieved.

## Demo

![Chat UI](docs/screenshot_chat.png)

The source chips only show pages the model actually cited in its answer.

## Architecture

![Architecture](docs/architecture.png)

```
PDF
  pageSplitter.py        per-page text, headers and page numbers stripped
  classifier.py          route each page by type
  chunking.py            semantic chunker / pattern chunker
  metadata.py            extract course code, department, program
  vector.py (store)      ChromaDB (MiniLM) + BM25 corpus

Question
  planner.py             LLM JSON: intent, depts, programs, course_codes, etc.
  vector.py (query)      plan-driven retrieval
                           course_codes  -> metadata filter
                           admission+dept-> semantic + dept filter + rerank
                           program_req   -> curriculum metadata match
                           topic_search  -> semantic + type filter
                           fallback      -> RRF(semantic, BM25) + rerank
  generate.py            intent-aware prompt + citation verifier
  app.py (FastAPI)       /chat endpoint + static UI
```

## Document Composition

A graduate catalog is not a uniform document. Out of 618 pages:

![Page composition](docs/page_breakdown.png)

| Page type | Count | Structure | Chunking |
|---|---:|---|---|
| Course descriptions | 165 | `CODE`, title, description, credits | Pattern (regex on course codes) |
| Curriculum / tables | 295 | course codes with credit hours | Whole page |
| Prose / policy | 124 | full paragraphs | Semantic (cosine boundaries between sentences) |
| Dept info / mixed | 19 | mixed | Semantic |
| TOC / skip | 15 | n/a | Discarded |

460 of 618 pages are structured and the rest are prose. One chunking strategy degrades both, so the classifier routes each page to the right chunker.

## Components

| File | Purpose |
|---|---|
| `pageSplitter.py` | PDF loader, header and page-number cleaning (PyMuPDF) |
| `classifier.py` | Heuristic page-type classifier |
| `chunking.py` | Semantic chunker (sentence embeddings with cosine boundary detection) and pattern chunker for course descriptions |
| `metadata.py` | Extracts `course_code`, `department`, `program` per chunk |
| `pipeline.py` | Ingest pipeline: load, classify, chunk, enrich, store. Two-pass department tagging via course-code prefix propagation. |
| `vector.py` | ChromaDB collection plus BM25 index. Plan-driven `query()` with RRF fusion and cross-encoder reranking. |
| `planner.py` | LLM-based structured query planner (Azure OpenAI `o4-mini`, JSON response format) |
| `generate.py` | Intent-aware answer generation and citation verifier |
| `app.py` | FastAPI server with structured logging |
| `static/index.html` | Chat UI. Source chips filtered to cited pages. |
| `eval_simple.py` | ROUGE-L and embedding similarity over 100 questions |
| `eval_new.py` | 28-question regression suite |
| `eval_ragas.py` | RAGAS faithfulness, answer relevancy, context precision and recall |

## Stack

| Layer | Choice |
|---|---|
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector DB | ChromaDB (persistent, local) |
| Lexical retrieval | `rank-bm25` |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Fusion | Reciprocal Rank Fusion (k=60) |
| Planner and LLM | Azure OpenAI `o4-mini` (JSON-mode for planning) |
| Server | FastAPI with Uvicorn |
| Eval | rouge-score, sentence-transformers, RAGAS |

## Retrieval

The planner returns a structured plan and `vector.query()` routes on `intent`:

```json
{
  "intent": "admission",
  "course_codes": [],
  "departments": ["Biomedical Engineering"],
  "programs": ["PhD in Biomedical Engineering"],
  "comparison_entities": [],
  "is_ambiguous": false,
  "clarification": ""
}
```

| Intent | Strategy |
|---|---|
| `course_lookup` | ChromaDB `where={"course_code": ...}` per code |
| `comparison` | One top chunk per `course_code` |
| `admission` with dept | Semantic search filtered to `type=prose AND department=X`, then rerank |
| `program_requirements` | Substring match on normalized `program` metadata (handles "MS in X" vs "Master of Science in X") |
| `topic_search` | Semantic with `type=descriptive` filter |
| `policy`, `financial`, `definition` | Type-filtered semantic, BM25, RRF, rerank |
| Fallback | RRF(semantic, BM25) with rerank |

## Generation

`generate.py` does a few things:

1. Grounds every claim in retrieved passages and never mentions retrieval plumbing in the reply.
2. Picks an answer shape from the intent. Prose for single facts. Bullets only when there are at least three numeric requirements or distinct comparison axes.
3. Runs a citation verifier. A regex pass strips any `(p. XXX)` whose page is not in the retrieved chunks.
4. Handles out-of-scope questions through `deflect()`, which asks the LLM to name the specific IIT office the user should contact (Athletics, Access/Card/Parking, Office of International Affairs, Office of Undergraduate Admission, HR, and so on).

## Evaluation

128 questions total. 100 baseline questions across admission, course lookup, program requirements, policy, financial, topic search, definition, and comparison. 28 regression questions covering department-specific admission, edge programs, and out-of-scope variants.

Trajectory on the same 100-question baseline:

| Version | ROUGE-L | Emb Sim | Change |
|---|---:|---:|---|
| v1 | 0.165 | 0.598 | Semantic chunking with ChromaDB |
| v2 | 0.221 | 0.681 | Added hybrid chunking (page classifier and per-type strategies) |
| v3 | 0.298 | 0.751 | Added BM25, RRF, cross-encoder rerank, dept-filtered admission |
| v4 | **0.352** | **0.801** | Added LLM planner, plan-driven retrieval, citation verifier, OOS deflect |

Per-category at v4:

| Category | ROUGE-L | Emb Sim |
|---|---:|---:|
| `course_lookup` | 0.41 | 0.84 |
| `admission` | 0.39 | 0.83 |
| `program_requirements` | 0.34 | 0.80 |
| `policy` | 0.32 | 0.78 |
| `financial` | 0.36 | 0.81 |
| `topic_search` | 0.31 | 0.77 |
| `adversarial` (OOS) | 0.51 | 0.86 |

## Setup

Requirements:

- Python 3.10+
- About 2 GB disk for ChromaDB and model weights
- An Azure OpenAI deployment of `o4-mini` or another compatible chat model

Install:

```bash
git clone <repo-url>
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPEN_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=o4-mini
```

Place the catalog PDF in the project root and run the ingest pipeline once:

```bash
python pipeline.py
```

This writes `chunks.json` and populates `chroma_db/`. Takes about 5 to 10 minutes.

Start the server:

```bash
uvicorn app:app --reload --port 8000
```

Open `http://localhost:8000`.

Run the evaluations:

```bash
python eval_simple.py
python eval_new.py
python eval_ragas.py
```

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .env                          # not committed
├── 2024-2025_final.pdf           # source document
│
├── pageSplitter.py
├── classifier.py
├── chunking.py
├── metadata.py
├── pipeline.py
│
├── planner.py
├── vector.py
├── generate.py
├── app.py
│
├── eval_simple.py
├── eval_new.py
├── eval_ragas.py
│
├── static/
│   ├── index.html
│   └── slides.html
│
├── chroma_db/                    # generated by pipeline.py
└── chunks.json                   # generated by pipeline.py
```

## Design Notes

**Why an LLM planner instead of regex extractors and a prototype-embedding router.** An earlier version used regex to pull out course codes and departments and prototype-embedding similarity to detect intent. It misrouted queries like "MS Data Science course list" (no `BME`-style prefix to grab) and could not normalize "MS in X" against "Master of Science in X". One JSON-mode LLM call replaces all of it and is more accurate.

**Why verify citations.** LLMs hallucinate page numbers, and a fake `(p. 305)` makes a wrong answer look authoritative. A short regex pass strips any citation whose page is not in the retrieved chunks.

**Why hybrid chunking.** Semantic chunking on 165 pages of `CODE`, title, description, credits produces small fragments that lose the course as a unit. Pattern matching on course codes recovers the natural unit. Prose pages get the opposite treatment because pattern matching gives nothing useful there.

**Why two-pass department tagging.** Many pages (admission intros, thesis info, certificate descriptions) don't contain course codes but still belong to a department. The pipeline propagates department from nearby course-code pages (forward first, then backward, within 15 pages) so a `where={"department": "Biomedical Engineering"}` filter still pulls them in.

## Limitations

- The catalog is a single 2024-2025 snapshot. Refreshing means re-running `pipeline.py`.
- Department propagation is heuristic and a few edge pages may be tagged wrong.
- Topic search relies on keyword overlap with course descriptions. Courses without it won't surface.
- One LLM call for planning and one for generation. End-to-end latency is around 3 to 5 seconds on `o4-mini`.
