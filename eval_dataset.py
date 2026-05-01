# Ground truth Q&A pairs for RAGAS evaluation
# Covers: course lookups, program requirements, admission, policies, financial

dataset = [
    {
        "question": "What is CSP 554?",
        "ground_truth": "CSP 554 is Big Data Technologies, a 3-credit course covering informatics for data sets beyond the capacity of typical database tools. It surveys technologies for capturing, storing, analyzing, and managing big data. Prerequisite is CS 425 with a minimum grade of C.",
    },
    {
        "question": "What is CS 577?",
        "ground_truth": "CS 577 is Deep Learning, a 3-credit course covering deep neural networks including feedforward networks, convolutional networks, sequence modeling, transformers, and deep generative models. Prerequisite is CS 430.",
    },
    {
        "question": "What is MATH 564?",
        "ground_truth": "MATH 564 is Regression, a 3-credit course that introduces statistical regression models including simple linear regression, multiple regression, model selection, and diagnostics. Prerequisites are MATH 474, MATH 476, or MATH 563 with a minimum grade of C.",
    },
    {
        "question": "What is ECE 543?",
        "ground_truth": "ECE 543 is Computer Network Security, a 3-credit course covering fundamental computer network security topics including cryptography, authentication, firewalls, intrusion detection, and network protocols.",
    },
    {
        "question": "What is ARCH 590?",
        "ground_truth": "ARCH 590 is Specialized Research, a course in the Master of Science program that is synthetic and interdisciplinary in its approach to architectural research.",
    },
    {
        "question": "What are the requirements for MS in Computer Science?",
        "ground_truth": "Admission requires a minimum undergraduate GPA of 3.0/4.0, GRE scores of at least 300 combined quantitative and verbal with 3.0 analytical writing. The GRE may be waived for applicants with a US bachelor's degree and GPA of 3.0 or higher.",
    },
    {
        "question": "What are the requirements for PhD in Computer Science?",
        "ground_truth": "The PhD in Computer Science requires a minimum undergraduate GPA of 3.0 and master's GPA of 3.5. Students must complete core coursework, pass written and oral qualifying examinations, and make an original research contribution.",
    },
    {
        "question": "What is the curriculum for Master of Cybersecurity?",
        "ground_truth": "The Master of Cybersecurity requires 30 minimum degree credits with 9 minimum core course credits and at least 5 courses from cybersecurity electives.",
    },
    {
        "question": "What courses are required for MS in Data Science?",
        "ground_truth": "The Master of Data Science is a collaborative program with the Department of Applied Mathematics. It includes required courses such as CSP 570 Data Science Seminar and courses in statistics, machine learning, and data management.",
    },
    {
        "question": "What are the GPA requirements for graduate admission?",
        "ground_truth": "Most graduate programs require a minimum cumulative undergraduate GPA of 3.0 out of 4.0. PhD programs typically require a minimum GPA of 3.5 for master's level work.",
    },
    {
        "question": "Can GRE be waived for engineering applicants?",
        "ground_truth": "Yes. The GRE requirement is waived for Master of Engineering applicants who hold a Bachelor of Science in a related field from an ABET-accredited US university with a minimum GPA of 3.0.",
    },
    {
        "question": "Are letters of recommendation required for graduate admission?",
        "ground_truth": "Letters of recommendation are required for doctoral applicants and strongly encouraged for master of science and professional master's program applicants.",
    },
    {
        "question": "What are the credit hour requirements for a PhD?",
        "ground_truth": "The doctoral degree requires 72 credit hours or more beyond the bachelor's degree, of which at least 36 must be dissertation research credits.",
    },
    {
        "question": "How many credits are needed for a masters degree?",
        "ground_truth": "All master's degrees require a minimum of 30 credit hours beyond the bachelor's degree.",
    },
    {
        "question": "What is the time limit to complete a PhD?",
        "ground_truth": "Doctoral study must be completed within six years of the mandatory doctoral advising session.",
    },
    {
        "question": "What is the policy for incomplete grades?",
        "ground_truth": "An incomplete grade may be approved by the instructor only in cases of illness or unforeseeable circumstances. The student must have substantial equity in the course and must complete the remaining work within the timeframe set by the instructor.",
    },
    {
        "question": "What is the policy for repeating courses?",
        "ground_truth": "Graduate students may repeat up to three distinct courses during their academic career. Students who enroll in an entirely new program may petition for an additional repeat.",
    },
    {
        "question": "What is the Employer Tuition Deferment Plan?",
        "ground_truth": "The Employer Tuition Deferment Plan allows students employed by a company that offers tuition reimbursement to defer tuition payment until reimbursement is received from their employer.",
    },
    {
        "question": "What courses cover deep learning?",
        "ground_truth": "Courses covering deep learning include CS 577 Deep Learning, ECE 501 Artificial Intelligence and Edge Computing, and ITMD 524 Applied Artificial Intelligence and Deep Learning.",
    },
    {
        "question": "What courses cover cloud computing?",
        "ground_truth": "Courses covering cloud computing include CS 553 Cloud Computing, ECE 573 Cloud Computing and Cloud Native Systems, and ITMS 564 Cloud Computing Security.",
    },
]
