import time
import numpy as np
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer

from vector import query
from generate import generate
from planner import plan
from eval_dataset import dataset as eval_data

OUT_OF_SCOPE_REPLY = "That falls outside what I can help with. Please contact the relevant IIT office directly."

scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

metrics = ["rouge_l", "emb_sim"]

print(f"Running eval on {len(eval_data)} questions (generation + local scoring)...\n")

rows = []
start = time.time()

for i, item in enumerate(eval_data, 1):
    q = item["question"]
    gt = item["ground_truth"]
    cat = item.get("category", "unknown")

    t = time.time()
    p = plan(q)
    if p["intent"] == "out_of_scope":
        answer = OUT_OF_SCOPE_REPLY
    elif p.get("is_ambiguous"):
        answer = p.get("clarification") or "Could you be more specific?"
    else:
        results = query(q, plan_dict=p)
        answer = generate(q, results, plan=p)

    rouge_l = scorer.score(gt, answer)["rougeL"].fmeasure
    gt_emb, ans_emb = embedder.encode([gt, answer], normalize_embeddings=True)
    emb_sim = float(gt_emb @ ans_emb)

    rows.append({
        "question": q,
        "category": cat,
        "answer": answer,
        "ground_truth": gt,
        "rouge_l": rouge_l,
        "emb_sim": emb_sim,
    })

    print(f"  [{i:3d}/{len(eval_data)}] ({time.time()-t:.1f}s) [{cat:22s}] {q[:55]}")
    print(f"           rouge_l={rouge_l:.3f}  emb_sim={emb_sim:.3f}")

print(f"\nDone in {time.time()-start:.0f}s\n")

# per-category averages
print(f"{'Category':<25} {'ROUGE-L':>8} {'Emb Sim':>8}  N")
print("-" * 50)
cats = sorted(set(r["category"] for r in rows))
for cat in cats:
    sub = [r for r in rows if r["category"] == cat]
    rl = np.mean([r["rouge_l"] for r in sub])
    es = np.mean([r["emb_sim"] for r in sub])
    print(f"{cat:<25} {rl:>8.3f} {es:>8.3f}  {len(sub)}")

print("-" * 50)
rl_all = np.mean([r["rouge_l"] for r in rows])
es_all = np.mean([r["emb_sim"] for r in rows])
print(f"{'Overall':<25} {rl_all:>8.3f} {es_all:>8.3f}  {len(rows)}")

# worst answers
threshold_rl = 0.1
threshold_es = 0.5
print(f"\nWeak answers (ROUGE-L < {threshold_rl} or Emb Sim < {threshold_es})")
for r in rows:
    if r["rouge_l"] < threshold_rl or r["emb_sim"] < threshold_es:
        print(f"\n  [{r['category']}] {r['question'][:65]}")
        print(f"    rouge_l={r['rouge_l']:.3f}  emb_sim={r['emb_sim']:.3f}")
        print(f"    Answer:  {r['answer'][:120]}")
        print(f"    GT:      {r['ground_truth'][:120]}")

# save
import csv
with open("eval_simple_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["question", "category", "rouge_l", "emb_sim", "answer", "ground_truth"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"\nSaved to eval_simple_results.csv")
print(f"Total wall time: {time.time()-start:.0f}s")
