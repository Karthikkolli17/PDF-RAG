import time
import numpy as np
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from planner import plan
from vector import query
from generate import generate, deflect

scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

OUT_OF_SCOPE_REPLY = "That falls outside what I can help with. Please contact the relevant IIT office directly."

# 28 new questions not in the original 100
# Tests: dept-specific admission, new programs, edge cases, out-of-scope variants
new_dataset = [

    # dept-specific admission — tests the new department filtering
    {
        "category": "admission_dept",
        "question": "What is the minimum GPA for PhD in Biomedical Engineering?",
        "ground_truth": "The minimum cumulative undergraduate GPA for admission to PhD programs in Biomedical Engineering is 3.0 on a 4.0 scale.",
    },
    {
        "category": "admission_dept",
        "question": "What GRE scores are required for MS in Electrical and Computer Engineering?",
        "ground_truth": "For the MS in Electrical and Computer Engineering, professional master's degrees do not require GRE scores for applicants holding U.S. undergraduate degrees with a minimum GPA of 3.0. The PhD program requires GRE scores.",
    },
    {
        "category": "admission_dept",
        "question": "What are the admission requirements for the PhD in Applied Mathematics?",
        "ground_truth": "The PhD in Applied Mathematics requires a minimum cumulative undergraduate GPA of 3.5 on a 4.0 scale.",
    },
    {
        "category": "admission_dept",
        "question": "What GPA is required for MS in Computer Science?",
        "ground_truth": "The minimum cumulative undergraduate GPA required for the MS in Computer Science is 3.0 on a 4.0 scale, with a minimum GRE score of 305 combined quantitative and verbal.",
    },
    {
        "category": "admission_dept",
        "question": "What are the TOEFL requirements for the CS PhD program?",
        "ground_truth": "International applicants to the CS PhD program must submit a TOEFL score of 70 or demonstrate English proficiency through a degree from an English-language institution.",
    },
    {
        "category": "admission_dept",
        "question": "Can the GRE be waived for the Master of Information Technology and Management?",
        "ground_truth": "The GRE requirement may be waived for applicants to ITM programs under certain conditions related to their undergraduate institution and GPA.",
    },

    # program requirements — new programs not in original 100
    {
        "category": "program_requirements",
        "question": "What are the requirements for the Master of Artificial Intelligence?",
        "ground_truth": "The Master of Artificial Intelligence requires a minimum of 30 credit hours with no more than 10 credits at the 400-level and at least 18 credits in CS or CSP courses. Core courses include CS 581 Advanced Artificial Intelligence and CS 584 Machine Learning or MATH 569 Statistical Learning.",
    },
    {
        "category": "program_requirements",
        "question": "What courses are required for the Master of Cybersecurity?",
        "ground_truth": "The Master of Cybersecurity requires 30 total credit hours including 9 core credit hours. Core courses are organized into three groups including CS 528 Data Privacy and Security, CS 549 Cryptography and Network Security, CS 458 Introduction to Information Security, and CS 557 Cyber-Physical Systems Security.",
    },
    {
        "category": "program_requirements",
        "question": "What is the structure of the PhD in Information Technology?",
        "ground_truth": "The PhD in Information Technology requires coursework, qualifying exams, a comprehensive exam, and a thesis defense. PhD research credits are taken through ITM 691.",
    },
    {
        "category": "program_requirements",
        "question": "What is the curriculum for the Master of Design?",
        "ground_truth": "The Master of Design requires a minimum of 54 credit hours which may increase to 66 with ESP and Design corequisites or 69 if Foundation prerequisites are required. The program is offered by the Institute of Design and covers design methods, research, and studio practice.",
    },
    {
        "category": "program_requirements",
        "question": "How many credits does the Doctor of Philosophy in Computer Science require?",
        "ground_truth": "The PhD in Computer Science requires 40 credit hours for students entering with a Master of Science in Computer Science, 49 credit hours for those entering with a master's degree not in computer science, and 72 credit hours for those entering with a Bachelor of Science in Computer Science.",
    },
    {
        "category": "program_requirements",
        "question": "What specializations are available in the MS in Applied Mathematics?",
        "ground_truth": "The MS in Applied Mathematics offers specializations in Computational Mathematics and Mechanics, Stochastic Computation, Quantitative Risk Management, and Applied Statistics.",
    },

    # course lookups — departments not covered in original 100
    {
        "category": "course_lookup",
        "question": "What is BIOL 501?",
        "ground_truth": "BIOL 501 is Graduate Laboratory Techniques, a course in the Biology department covering laboratory methods for graduate research.",
    },
    {
        "category": "course_lookup",
        "question": "What is MATH 540?",
        "ground_truth": "MATH 540 is Probability, a graduate-level course in the Applied Mathematics department.",
    },
    {
        "category": "course_lookup",
        "question": "What is IDN 501?",
        "ground_truth": "IDN 501 is Communication Systems Exploration, a course in the Institute of Design.",
    },
    {
        "category": "course_lookup",
        "question": "What is CHEM 500?",
        "ground_truth": "CHEM 500 is a graduate chemistry course offered by the Chemistry department.",
    },

    # policy — edge cases
    {
        "category": "policy",
        "question": "What is the maximum number of credits a graduate student can transfer?",
        "ground_truth": "Graduate students may transfer a limited number of credits from other accredited institutions toward their degree, subject to approval by the graduate adviser.",
    },
    {
        "category": "policy",
        "question": "What is the co-terminal degree program at IIT?",
        "ground_truth": "The co-terminal degree program allows qualified undergraduate students to begin graduate coursework and earn both a bachelor's and master's degree.",
    },
    {
        "category": "policy",
        "question": "What happens to incomplete grades if not resolved?",
        "ground_truth": "Incomplete grades that are not resolved within the allowed time period are converted to a failing grade.",
    },

    # financial — new questions
    {
        "category": "financial",
        "question": "What is the payment plan for graduate students?",
        "ground_truth": "IIT offers a payment plan for graduate students through the student accounting office at web.iit.edu/student-accounting.",
    },

    # topic search — new topics
    {
        "category": "topic_search",
        "question": "What courses cover computer vision?",
        "ground_truth": "CS 512 Computer Vision covers feature extraction, object recognition, and the application of deep neural networks in vision. CS 577 Deep Learning also covers convolutional networks and visual applications.",
    },
    {
        "category": "topic_search",
        "question": "What courses cover bioinformatics?",
        "ground_truth": "BIOL 550 Bioinformatics introduces life science graduates to Unix/Linux, Perl programming, sequence analysis, and bioinformatics tools and databases.",
    },
    {
        "category": "topic_search",
        "question": "What courses are available on robotics?",
        "ground_truth": "CS 582 Computational Robotics covers locomotion, non-visual sensors, uncertainty modeling, Kalman filtering, visual sensing, and path planning algorithms.",
    },

    # adversarial — new out-of-scope variants
    {
        "category": "adversarial",
        "question": "What undergraduate courses does IIT offer in computer science?",
        "ground_truth": "Undergraduate course information is not covered in the IIT Graduate Catalog. Please contact the Office of Undergraduate Admission for information on undergraduate computer science courses.",
    },
    {
        "category": "adversarial",
        "question": "How do I get a HawkCard?",
        "ground_truth": "HawkCard information is not covered in the Graduate Catalog. Please contact IIT Access, Card and Parking Services for information on obtaining a HawkCard.",
    },
    {
        "category": "adversarial",
        "question": "What is the salary of a professor at IIT?",
        "ground_truth": "Faculty salary information is not covered in the IIT Graduate Catalog. Please contact IIT Human Resources for information on faculty compensation.",
    },
    {
        "category": "adversarial",
        "question": "What sports teams does IIT have?",
        "ground_truth": "Athletics information is not covered in the IIT Graduate Catalog. Please contact the IIT Athletics Department for details on sports teams.",
    },
    {
        "category": "adversarial",
        "question": "Is IIT a good school for engineering?",
        "ground_truth": "Institutional quality assessments and rankings are not covered in the Graduate Catalog. Please contact the Office of Undergraduate Admission for information on IIT engineering program reputation.",
    },
]

print(f"Running {len(new_dataset)} new questions...\n")
rows = []
start = time.time()

for i, item in enumerate(new_dataset, 1):
    q = item["question"]
    gt = item["ground_truth"]
    cat = item["category"]

    t = time.time()
    p = plan(q)
    intent = p["intent"]
    if intent == "out_of_scope":
        answer = deflect(q)
    elif p.get("is_ambiguous"):
        answer = p.get("clarification") or "Could you be more specific?"
    else:
        results = query(q, plan_dict=p)
        answer = generate(q, results, plan=p)

    rouge_l = scorer.score(gt, answer)["rougeL"].fmeasure
    gt_emb, ans_emb = embedder.encode([gt, answer], normalize_embeddings=True)
    emb_sim = float(gt_emb @ ans_emb)

    rows.append({"question": q, "category": cat, "answer": answer, "ground_truth": gt, "rouge_l": rouge_l, "emb_sim": emb_sim, "intent": intent})

    print(f"  [{i:2d}/{len(new_dataset)}] ({time.time()-t:.1f}s) [{cat:22s}] {q[:55]}")
    print(f"           intent={intent}  rouge_l={rouge_l:.3f}  emb_sim={emb_sim:.3f}")

print(f"\nDone in {time.time()-start:.0f}s\n")

metrics = ["rouge_l", "emb_sim"]
print(f"{'Category':<25} {'ROUGE-L':>8} {'Emb Sim':>8}  N")
print("-" * 50)
for cat in sorted(set(r["category"] for r in rows)):
    sub = [r for r in rows if r["category"] == cat]
    print(f"{cat:<25} {np.mean([r['rouge_l'] for r in sub]):>8.3f} {np.mean([r['emb_sim'] for r in sub]):>8.3f}  {len(sub)}")
print("-" * 50)
print(f"{'Overall':<25} {np.mean([r['rouge_l'] for r in rows]):>8.3f} {np.mean([r['emb_sim'] for r in rows]):>8.3f}  {len(rows)}")

print("\nPer-question detail:")
for r in rows:
    flag = " <-- WEAK" if r["rouge_l"] < 0.1 or r["emb_sim"] < 0.5 else ""
    print(f"  [{r['category']}] {r['question'][:60]}{flag}")
    print(f"    rouge_l={r['rouge_l']:.3f}  emb_sim={r['emb_sim']:.3f}  intent={r['intent']}")
    if flag:
        print(f"    Answer: {r['answer'][:150]}")
        print(f"    GT:     {r['ground_truth'][:150]}")
