import warnings
warnings.filterwarnings("ignore")

import os
import re
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

FENCE = re.compile(r"```(?:json)?\s*|\s*```")


def extract_json(text: str) -> str:
    text = FENCE.sub("", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return text


class CleanJSONWrapper(LangchainLLMWrapper):

    def _clean(self, result):
        for gen_list in result.generations:
            for gen in gen_list:
                if hasattr(gen, "text"):
                    gen.text = extract_json(gen.text)
                if hasattr(gen, "message") and hasattr(gen.message, "content"):
                    gen.message.content = extract_json(gen.message.content)
        return result

    def generate_text(self, prompt, n=1, temperature=None, stop=None, callbacks=None):
        return self._clean(super().generate_text(prompt, n=n, temperature=temperature, stop=stop, callbacks=callbacks))

    async def agenerate_text(self, prompt, n=1, temperature=None, stop=None, callbacks=None):
        return self._clean(await super().agenerate_text(prompt, n=n, temperature=temperature, stop=stop, callbacks=callbacks))


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

print(f"Building evaluation samples ({len(eval_data)} questions)...")
questions, answers, contexts, ground_truths = [], [], [], []

for i, item in enumerate(eval_data, 1):
    q = item["question"]
    results = query(q)
    answer = generate(q, results)
    questions.append(q)
    answers.append(answer)
    contexts.append(results["documents"][0])
    ground_truths.append(item["ground_truth"])
    print(f"  [{i}/{len(eval_data)}] {q[:65]}")

print("\nRunning RAGAS evaluation...")
data = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths,
})

result = evaluate(
    data,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)

df = result.to_pandas()
print("RAGAS Evaluation Results")

q_col = "user_input" if "user_input" in df.columns else "question"
metric_cols = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]
for _, row in df[[q_col] + metric_cols].iterrows():
    print(f"\nQ: {str(row[q_col])[:65]}")
    print(f"   Faithfulness:      {row['faithfulness']:.3f}")
    print(f"   Answer Relevancy:  {row['answer_relevancy']:.3f}")
    print(f"   Context Precision: {row['context_precision']:.3f}")
    print(f"   Context Recall:    {row['context_recall']:.3f}")

print("Averages (all)")
for col in metric_cols:
    print(f"  {col:25s}: {df[col].mean():.3f}")

df_clean = df[df["faithfulness"] > 0]
dropped = len(df) - len(df_clean)
print(f"\n-Averages excluding {dropped} zero-faithfulness artifacts:")
for col in metric_cols:
    print(f"  {col:25s}: {df_clean[col].mean():.3f}")
