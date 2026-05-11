import warnings
warnings.filterwarnings("ignore")

import os
import re
import json
import time
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas.llms.base import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate
from datasets import Dataset
from vector import query
from generate import generate
from eval_dataset import dataset as eval_data

load_dotenv()

fence = re.compile(r"```(?:json)?\s*|\s*```")
bare_obj = re.compile(r"\{[^{}]*\}", re.DOTALL)


def extract_json(text):
    text = fence.sub("", text).strip()

    obj_start, obj_end = text.find("{"), text.rfind("}")
    arr_start, arr_end = text.find("["), text.rfind("]")

    use_obj = obj_start != -1 and obj_end > obj_start and (arr_start == -1 or obj_start < arr_start)
    use_arr = arr_start != -1 and arr_end > arr_start and (obj_start == -1 or arr_start < obj_start)

    if use_obj:
        return text[obj_start:obj_end + 1]
    if use_arr:
        return text[arr_start:arr_end + 1]

    objects = bare_obj.findall(text)
    if objects:
        candidate = "[" + ", ".join(objects) + "]"
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass

    return text


class CleanJSONWrapper(LangchainLLMWrapper):

    def clean(self, result):
        for gen_list in result.generations:
            for gen in gen_list:
                if hasattr(gen, "text"):
                    gen.text = extract_json(gen.text)
                if hasattr(gen, "message") and hasattr(gen.message, "content"):
                    gen.message.content = extract_json(gen.message.content)
        return result

    def generate_text(self, prompt, n=1, temperature=None, stop=None, callbacks=None):
        return self.clean(super().generate_text(prompt, n=n, temperature=temperature, stop=stop, callbacks=callbacks))

    async def agenerate_text(self, prompt, n=1, temperature=None, stop=None, callbacks=None):
        return self.clean(await super().agenerate_text(prompt, n=n, temperature=temperature, stop=stop, callbacks=callbacks))


llm = CleanJSONWrapper(
    AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "o4-mini"),
        api_key=os.getenv("OPEN_API_KEY"),
        api_version="2025-01-01-preview",
    ),
    bypass_temperature=True,
)

emb = LangchainEmbeddingsWrapper(HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))

for m in [faithfulness, answer_relevancy, context_precision, context_recall]:
    m.llm = llm
answer_relevancy.embeddings = emb

metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]

print(f"Building evaluation samples ({len(eval_data)} questions)...")
questions, answers, contexts, ground_truths, categories = [], [], [], [], []
start = time.time()

for i, item in enumerate(eval_data, 1):
    q = item["question"]
    t = time.time()
    results = query(q)
    answer = generate(q, results)
    questions.append(q)
    answers.append(answer)
    contexts.append(results["documents"][0])
    ground_truths.append(item["ground_truth"])
    categories.append(item.get("category", "unknown"))
    print(f"  [{i:3d}/{len(eval_data)}] ({time.time()-t:.1f}s) [{item.get('category','?'):22s}] {q[:60]}")

print(f"\nRetrieval + generation done in {time.time()-start:.0f}s. Running RAGAS...\n")

data = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths,
})

result = evaluate(data, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])

df = result.to_pandas()
df["category"] = categories

q_col = "user_input" if "user_input" in df.columns else "question"

# per-question results
print("Per-Question Results")
for i, row in df[[q_col, "category"] + metrics].iterrows():
    print(f"\n[{row['category']}]  {str(row[q_col])[:65]}")
    print(f"   Faithfulness:      {row['faithfulness']:.3f}")
    print(f"   Answer Relevancy:  {row['answer_relevancy']:.3f}")
    print(f"   Context Precision: {row['context_precision']:.3f}")
    print(f"   Context Recall:    {row['context_recall']:.3f}")

# per-category averages
print("\nPer-Category Averages")
print(f"{'Category':<25} {'Faith':>7} {'AnswRel':>7} {'CtxPre':>7} {'CtxRec':>7}  N")
for cat in sorted(df["category"].unique()):
    sub = df[df["category"] == cat]
    vals = [sub[c].mean() for c in metrics]
    print(f"{cat:<25} {vals[0]:>7.3f} {vals[1]:>7.3f} {vals[2]:>7.3f} {vals[3]:>7.3f}  {len(sub)}")

# overall averages
overall = [df[c].mean() for c in metrics]
print(f"\n{'Overall':<25} {overall[0]:>7.3f} {overall[1]:>7.3f} {overall[2]:>7.3f} {overall[3]:>7.3f}  {len(df)}")

df_clean = df[df["faithfulness"] > 0]
dropped = len(df) - len(df_clean)
clean = [df_clean[c].mean() for c in metrics]
print(f"{'Overall (excl. artifacts)':<25} {clean[0]:>7.3f} {clean[1]:>7.3f} {clean[2]:>7.3f} {clean[3]:>7.3f}  {len(df_clean)}")
if dropped:
    print(f"  ({dropped} zero-faithfulness artifacts excluded)")

# weak responses
threshold = 0.5
weak = df[(df[metrics] < threshold).any(axis=1)]
if not weak.empty:
    print(f"\nWeak Responses (any metric < {threshold})")
    for i, row in weak[[q_col, "category"] + metrics].iterrows():
        print(f"  [{row['category']}] {str(row[q_col])[:60]}")
        for col in metrics:
            marker = " <--" if row[col] < threshold else ""
            print(f"    {col:<22}: {row[col]:.3f}{marker}")

# save results
df[[q_col, "category"] + metrics].to_csv("eval_results.csv", index=False)
print(f"\nResults saved to eval_results.csv")
print(f"Total wall time: {time.time()-start:.0f}s")
