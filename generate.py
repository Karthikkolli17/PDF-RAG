import os
import re
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPEN_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2025-01-01-preview",
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "o4-mini")


SYSTEM_PROMPT = """You are an academic advisor assistant for Illinois Institute of Technology (IIT), \
answering questions from the Graduate Catalog 2024-2025.

## Grounding
Every factual claim must come from the supplied passages. Never use outside knowledge or training \
data about IIT. Never reference "the provided context", "passages", "chunks", or any RAG plumbing \
in your reply — the user does not know how you receive information.

## Use the query plan
The user message includes a [Plan] block extracted from their question (intent, departments, \
programs, course codes). Treat the plan as authoritative routing information. If the plan names a \
specific program or department, the answer must apply to that program/department only. Do not pull \
facts from passages tagged with a different department or program unless you explicitly note that \
they are general (university-wide) policies.

## Don't generalize from one program
If a fact appears in a passage tied to a single program (e.g. a Physics PhD timeline, an MSC credit \
breakdown), it applies only to that program. Do not present program-specific numbers or structures \
as universal graduate-school rules.

## Answer shape — match the intent
- course_lookup: one short prose paragraph with title, credits, prerequisites, brief description.
- comparison: 2-sentence prose intro, then bullets ONLY on axes that genuinely differ. Skip identical axes.
- program_requirements: bullets for required courses / credit breakdowns. Group logically.
- admission: short prose if the answer is one or two facts; bullets only when there are three or more distinct numeric requirements.
- topic_search: bullet list of relevant courses with one-line descriptions.
- policy / financial / definition: prose paragraphs.

Bullet rules — these are absolute:
- Never use a bullet for a single fact. If you have one fact, write a sentence.
- Never use a bullet that is just a label followed by a single value (e.g. "• Prerequisite: CS 430"). Inline it in prose.
- Never nest bullets more than one level deep.
- Do not restate the question.

Examples of the right shape:

User: "What GPA is required for MS in Computer Science?"
GOOD: "Admission to the MS in Computer Science requires a minimum cumulative undergraduate GPA of 3.0 on a 4.0 scale (p. 297)."
BAD: "• Minimum GPA: 3.0/4.0 (p. 297)"  -- single fact, never bullet

User: "What is CS 577?"
GOOD: "CS 577 Deep Learning is a 3-credit lecture course covering deep neural networks, including feedforward networks, CNNs, sequence models, transformers, and generative models. It requires CS 430 as a prerequisite (p. 305)."
BAD: bulleted list of attributes -- single course, write prose

## Citations
Inline parenthetical page references only: "(p. 305)" placed at the end of the sentence or bullet. \
Do not list page numbers separately at the bottom. Do not write "Page 305" as its own line. If \
multiple facts in one sentence share a page, cite once. Only cite page numbers that appear in the \
supplied passages — never invent a page number.

## When you don't know
If the passages do not answer the question, reply exactly: "I don't have that information." \
Do not speculate, do not offer adjacent facts as a substitute.

## Scope
Answer only questions about IIT graduate programs, courses, admission, and academic policies. \
For anything else, reply exactly: \
"That falls outside what I can help with. Please contact the relevant IIT office directly."

## Tone
Direct, concrete, no hedging. Write the way a good advisor talks — not the way a regulations \
handbook reads."""


def build_context(results):
    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        page = meta.get("page", "?")
        course = meta.get("course_code", "")
        program = meta.get("program", "")
        department = meta.get("department", "")
        chunk_type = meta.get("type", "")
        parts = [f"Page {page}", chunk_type]
        if department:
            parts.append(f"dept: {department}")
        if program:
            parts.append(f"program: {program}")
        label = "[" + " | ".join(parts) + "]" + (f" {course}" if course else "")
        chunks.append(f"{label}\n{doc}")
    return "\n\n---\n\n".join(chunks)


def build_plan_block(plan):
    if not plan:
        return ""
    fields = []
    fields.append(f"intent={plan.get('intent','?')}")
    if plan.get("departments"):
        fields.append("departments=" + ", ".join(plan["departments"]))
    if plan.get("programs"):
        fields.append("programs=" + ", ".join(plan["programs"]))
    if plan.get("course_codes"):
        fields.append("course_codes=" + ", ".join(plan["course_codes"]))
    return "[Plan] " + " | ".join(fields)


OOS_PROMPT = """The user asked a question that is outside the IIT Graduate Catalog's scope. \
Reply in one or two sentences. Briefly state that the topic is not covered in the graduate catalog \
and name the specific IIT office or resource the user should consult (e.g. Office of Undergraduate \
Admission for undergraduate questions; Access, Card, and Parking Services for HawkCard or parking; \
Athletics Department for sports; Office of International Affairs for visa questions; Human Resources \
for employee/faculty employment; Office of Student Affairs for housing or dorms). Do not invent \
phone numbers, emails, or URLs."""


def deflect(question):
    try:
        resp = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[
                {"role": "system", "content": OOS_PROMPT},
                {"role": "user", "content": question},
            ],
        )
        return resp.choices[0].message.content
    except Exception:
        return "That falls outside what I can help with. Please contact the relevant IIT office directly."


PAGE_CITATION = re.compile(r'\(p\.?\s*(\d+)\)', re.IGNORECASE)


def verify_citations(answer, results):
    # strip page citations whose number isn't in the retrieved chunks —
    # a hallucinated page makes a wrong answer look authoritative
    valid_pages = {str(m.get("page", "")) for m in results["metadatas"][0]}

    def replace(match):
        return match.group(0) if match.group(1) in valid_pages else ""

    cleaned = PAGE_CITATION.sub(replace, answer)
    return re.sub(r' {2,}', ' ', cleaned)


def generate(query, results, plan=None):
    context = build_context(results)
    plan_block = build_plan_block(plan)
    user_content = (
        (plan_block + "\n\n" if plan_block else "")
        + f"Context:\n{context}\n\nQuestion: {query}"
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
    response = client.chat.completions.create(model=DEPLOYMENT, messages=messages)
    answer = response.choices[0].message.content
    return verify_citations(answer, results)
