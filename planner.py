import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPEN_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2025-01-01-preview",
)
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "o4-mini")

DEPARTMENTS = [
    "Architecture", "Biology", "Biomedical Engineering", "Building Information Modeling",
    "Chemical and Biological Engineering", "Chemistry",
    "Civil, Architectural, and Environmental Engineering", "Communication",
    "Computer Science", "Electrical and Computer Engineering", "Engineering",
    "Environmental Engineering", "Environmental Management and Sustainability",
    "Food Safety and Nutrition", "History", "Humanities",
    "Information Technology and Management", "Institute of Design",
    "Landscape Architecture", "Master of Science in Finance", "Mathematics",
    "Maxwell Institute", "Mechanical and Aerospace Engineering",
    "Mechanical, Materials, and Aerospace Engineering", "Philosophy", "Physics",
    "Psychology", "Public Administration", "Science", "Sports Management",
    "Statistics", "Stuart School of Business", "Sustainability Analytics and Management",
    "Technology",
]

SYSTEM_PROMPT = f"""You extract structured query information for a RAG system over the IIT Graduate Catalog 2024-2025.

Return a JSON object with exactly these fields:

- intent (string, required): one of
  * "course_lookup"          asks about a specific course by code, e.g. "What is CS 577?"
  * "topic_search"           asks what courses cover a topic, e.g. "Which courses cover deep learning?"
  * "program_requirements"   asks about curriculum, credits, courses for a NAMED program
  * "admission"              asks about GPA, GRE, TOEFL, prerequisites, application requirements
  * "policy"                 academic policy: thesis, dismissal, residence, grading, incomplete grades
  * "financial"              tuition, scholarships, fellowships, assistantships, payment plans
  * "definition"             "what is X" where X is a concept, not a course
  * "comparison"             compares 2+ entities
  * "ambiguous"              too vague to commit; set is_ambiguous=true
  * "out_of_scope"           about IIT but outside the graduate catalog (undergrad, parking, dorms, sports, rankings, HawkCard, weather, faculty salaries, visa)

- course_codes (list[string]): course codes mentioned, format "CS 511" (uppercase prefix + single space + 3 digits). Empty list if none.
- departments (list[string]): EXACT match against this allowed list, no others:
{json.dumps(DEPARTMENTS)}
- programs (list[string]): program-level entities like "MS in Data Science", "PhD in Biomedical Engineering", "Master of Architecture". Use the form the user wrote.
- comparison_entities (list[string]): if intent="comparison", the things being compared. Otherwise [].
- is_ambiguous (bool): true if multiple distinct interpretations are reasonable.
- clarification (string): if is_ambiguous=true, a short clarifying question naming 2-3 likely interpretations. Else "".

Rules:
- Resolve dept abbreviations (BME, CS, ECE) to canonical full names from the allowed list.
- "PhD in CS admission" -> intent=admission, departments=["Computer Science"], programs=["PhD in Computer Science"].
- "Compare CS 577 and CS 580" -> intent=comparison, course_codes=["CS 577","CS 580"], comparison_entities=["CS 577","CS 580"].
- Out-of-scope examples: parking, undergraduate tuition, sports teams, dorms, HawkCard, professor salaries, rankings, weather, visa.

Respond with ONLY the JSON object. No prose, no markdown."""

cache = {}

def plan(question):
    q = question.strip()
    if q in cache:
        return cache[q]

    resp = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q},
        ],
        response_format={"type": "json_object"},
    )
    try:
        result = json.loads(resp.choices[0].message.content)
    except json.JSONDecodeError:
        result = empty_plan()

    result.setdefault("intent", "definition")
    result.setdefault("course_codes", [])
    result.setdefault("departments", [])
    result.setdefault("programs", [])
    result.setdefault("comparison_entities", [])
    result.setdefault("is_ambiguous", False)
    result.setdefault("clarification", "")

    result["departments"] = [d for d in result["departments"] if d in DEPARTMENTS]

    cache[q] = result
    return result


def empty_plan():
    return {
        "intent": "definition",
        "course_codes": [],
        "departments": [],
        "programs": [],
        "comparison_entities": [],
        "is_ambiguous": False,
        "clarification": "",
    }
