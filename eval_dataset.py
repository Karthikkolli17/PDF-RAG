# 100-question ground truth dataset for RAGAS evaluation
# Categories: course_lookup, program_requirements, admission, policy, financial, topic_search, adversarial

dataset = [

    # course lookups
    {
        "category": "course_lookup",
        "question": "What is CSP 554?",
        "ground_truth": "CSP 554 is Big Data Technologies, a 3-credit course covering informatics for data sets beyond the capacity of typical database tools. It surveys technologies for capturing, storing, analyzing, and managing big data. Prerequisite is CS 425 with a minimum grade of C.",
    },
    {
        "category": "course_lookup",
        "question": "What is CS 577?",
        "ground_truth": "CS 577 is Deep Learning, a 3-credit course covering deep neural networks including feedforward networks, convolutional networks, sequence modeling, transformers, and deep generative models. Prerequisite is CS 430.",
    },
    {
        "category": "course_lookup",
        "question": "What is MATH 564?",
        "ground_truth": "MATH 564 is Regression, a 3-credit course that introduces statistical regression models including simple linear regression, multiple regression, model selection, and diagnostics. Prerequisites are MATH 474, MATH 476, or MATH 563 with a minimum grade of C.",
    },
    {
        "category": "course_lookup",
        "question": "What is ECE 543?",
        "ground_truth": "ECE 543 is Computer Network Security, a 3-credit course covering fundamental computer network security topics including cryptography, authentication, firewalls, intrusion detection, and network protocols.",
    },
    {
        "category": "course_lookup",
        "question": "What is ARCH 590?",
        "ground_truth": "ARCH 590 is Specialized Research, a course in the Master of Science program that is synthetic and interdisciplinary in its approach to architectural research.",
    },
    {
        "category": "course_lookup",
        "question": "What is CS 553?",
        "ground_truth": "CS 553 is Cloud Computing, a 3-credit graduate course covering the principles, architectures, and technologies of cloud computing including virtualization, distributed systems, and cloud services.",
    },
    {
        "category": "course_lookup",
        "question": "What is ECE 573?",
        "ground_truth": "ECE 573 is Cloud Computing and Cloud Native Systems, a 3-credit course covering cloud architecture, containerization, orchestration, and cloud-native application development.",
    },
    {
        "category": "course_lookup",
        "question": "What is ITMS 564?",
        "ground_truth": "ITMS 564 is Cloud Computing Security, a 3-credit course covering security principles and practices for cloud environments including data protection, identity management, and compliance.",
    },
    {
        "category": "course_lookup",
        "question": "What is ECE 501?",
        "ground_truth": "ECE 501 is Artificial Intelligence and Edge Computing, a 3-credit course covering AI techniques applied at the edge including machine learning models for embedded and IoT systems.",
    },
    {
        "category": "course_lookup",
        "question": "What is ITMD 524?",
        "ground_truth": "ITMD 524 is Applied Artificial Intelligence and Deep Learning, a 3-credit course covering practical applications of deep learning techniques for real-world problems.",
    },
    {
        "category": "course_lookup",
        "question": "What is CSP 570?",
        "ground_truth": "CSP 570 is Data Science Seminar, a required course in the Master of Data Science program that introduces students to data science research, applications, and professional development.",
    },
    {
        "category": "course_lookup",
        "question": "What is ITMD 514?",
        "ground_truth": "ITMD 514 is Database Organization, a 3-credit course covering database design, relational models, SQL, and database management systems.",
    },
    {
        "category": "course_lookup",
        "question": "What is ITMD 521?",
        "ground_truth": "ITMD 521 is Platforms for Big Data Processing, a 3-credit course covering distributed computing platforms for processing large-scale data including Hadoop and Spark ecosystems.",
    },
    {
        "category": "course_lookup",
        "question": "What are the prerequisites for CSP 554?",
        "ground_truth": "The prerequisite for CSP 554 Big Data Technologies is CS 425 with a minimum grade of C.",
    },
    {
        "category": "course_lookup",
        "question": "What is the prerequisite for CS 577?",
        "ground_truth": "The prerequisite for CS 577 Deep Learning is CS 430.",
    },
    {
        "category": "course_lookup",
        "question": "How many credits is CS 577?",
        "ground_truth": "CS 577 Deep Learning is a 3-credit course.",
    },
    {
        "category": "course_lookup",
        "question": "What does CSP 554 cover?",
        "ground_truth": "CSP 554 Big Data Technologies covers informatics for data sets beyond the capacity of typical database tools, surveying technologies for capturing, storing, analyzing, and managing big data.",
    },
    {
        "category": "course_lookup",
        "question": "Tell me about ECE 543",
        "ground_truth": "ECE 543 is Computer Network Security, a 3-credit course covering cryptography, authentication, firewalls, intrusion detection, and network protocols.",
    },
    {
        "category": "course_lookup",
        "question": "How many credits is MATH 564?",
        "ground_truth": "MATH 564 Regression is a 3-credit course.",
    },
    {
        "category": "course_lookup",
        "question": "What is MATH 474?",
        "ground_truth": "MATH 474 is a probability and statistics course at the graduate level. It is listed as a prerequisite for MATH 564 Regression.",
    },
    {
        "category": "course_lookup",
        "question": "Can I take CSP 554 without CS 425?",
        "ground_truth": "No. CSP 554 Big Data Technologies requires CS 425 as a prerequisite with a minimum grade of C. Students must complete the prerequisite before enrolling.",
    },
    {
        "category": "course_lookup",
        "question": "Describe the CS 577 course in detail",
        "ground_truth": "CS 577 is Deep Learning, a 3-credit graduate course that covers deep neural networks including feedforward, convolutional, and recurrent networks, sequence modeling, transformers, and deep generative models. It requires CS 430 as prerequisite.",
    },
    {
        "category": "course_lookup",
        "question": "What courses does ITMD department offer?",
        "ground_truth": "ITMD courses include ITMD 514 Database Organization, ITMD 521 Platforms for Big Data Processing, and ITMD 524 Applied Artificial Intelligence and Deep Learning, among others.",
    },
    {
        "category": "course_lookup",
        "question": "What are the ECE department graduate courses?",
        "ground_truth": "The ECE department offers graduate courses including ECE 501 Artificial Intelligence and Edge Computing, ECE 543 Computer Network Security, and ECE 573 Cloud Computing and Cloud Native Systems.",
    },
    {
        "category": "course_lookup",
        "question": "What is the credit load for ECE 543?",
        "ground_truth": "ECE 543 Computer Network Security is a 3-credit course.",
    },

    # program requirements
    {
        "category": "program_requirements",
        "question": "What are the requirements for MS in Computer Science?",
        "ground_truth": "Admission requires a minimum undergraduate GPA of 3.0/4.0, GRE scores of at least 300 combined quantitative and verbal with 3.0 analytical writing. The GRE may be waived for applicants with a US bachelor's degree and GPA of 3.0 or higher.",
    },
    {
        "category": "program_requirements",
        "question": "What are the requirements for PhD in Computer Science?",
        "ground_truth": "The PhD in Computer Science requires a minimum undergraduate GPA of 3.0 and master's GPA of 3.5. Students must complete core coursework, pass written and oral qualifying examinations, and make an original research contribution.",
    },
    {
        "category": "program_requirements",
        "question": "What is the curriculum for Master of Cybersecurity?",
        "ground_truth": "The Master of Cybersecurity requires 30 minimum degree credits with 9 minimum core course credits and at least 5 courses from cybersecurity electives.",
    },
    {
        "category": "program_requirements",
        "question": "What courses are required for MS in Data Science?",
        "ground_truth": "The Master of Data Science is a collaborative program with the Department of Applied Mathematics. It includes required courses such as CSP 570 Data Science Seminar and courses in statistics, machine learning, and data management.",
    },
    {
        "category": "program_requirements",
        "question": "How many credits does the Master of Cybersecurity require?",
        "ground_truth": "The Master of Cybersecurity requires a minimum of 30 degree credits.",
    },
    {
        "category": "program_requirements",
        "question": "What are the core course credits for Master of Cybersecurity?",
        "ground_truth": "The Master of Cybersecurity requires 9 minimum core course credits covering foundational cybersecurity topics.",
    },
    {
        "category": "program_requirements",
        "question": "What is the minimum GPA required for MS in Computer Science admission?",
        "ground_truth": "The minimum undergraduate GPA for MS in Computer Science admission is 3.0 out of 4.0.",
    },
    {
        "category": "program_requirements",
        "question": "What qualifying exams are required for the PhD in Computer Science?",
        "ground_truth": "PhD in Computer Science students must pass written and oral qualifying examinations as part of the degree requirements.",
    },
    {
        "category": "program_requirements",
        "question": "What departments collaborate on the MS in Data Science?",
        "ground_truth": "The Master of Data Science is a collaborative program between the Department of Computer Science and the Department of Applied Mathematics.",
    },
    {
        "category": "program_requirements",
        "question": "Is CSP 570 required for data science students?",
        "ground_truth": "Yes, CSP 570 Data Science Seminar is a required course in the Master of Data Science program.",
    },
    {
        "category": "program_requirements",
        "question": "What is the difference between MS and PhD requirements at IIT?",
        "ground_truth": "Master's degrees require a minimum of 30 credit hours. PhD degrees require 72 or more credit hours beyond the bachelor's degree, qualifying examinations, and an original dissertation with at least 36 dissertation research credits.",
    },
    {
        "category": "program_requirements",
        "question": "What research contribution is required for the PhD?",
        "ground_truth": "PhD students must make an original research contribution and complete at least 36 dissertation research credits out of the 72 required beyond the bachelor's degree.",
    },
    {
        "category": "program_requirements",
        "question": "How is the MS in Data Science structured?",
        "ground_truth": "The Master of Data Science includes required courses such as CSP 570 Data Science Seminar, plus courses in statistics, machine learning, and data management. It is a collaborative program with the Applied Mathematics department.",
    },
    {
        "category": "program_requirements",
        "question": "What programs does the Computer Science department offer?",
        "ground_truth": "The Computer Science department offers graduate programs including the Master of Science in Computer Science, Master of Data Science, and Doctor of Philosophy in Computer Science.",
    },
    {
        "category": "program_requirements",
        "question": "What elective requirements exist for the Master of Cybersecurity?",
        "ground_truth": "The Master of Cybersecurity requires at least 5 courses from cybersecurity electives in addition to the 9 core course credits to meet the 30-credit minimum.",
    },
    {
        "category": "program_requirements",
        "question": "What are the PhD in CS admission GPA requirements?",
        "ground_truth": "The PhD in Computer Science requires a minimum undergraduate GPA of 3.0 and a master's GPA of 3.5.",
    },
    {
        "category": "program_requirements",
        "question": "What is the MS in Computer Science GRE requirement?",
        "ground_truth": "MS in Computer Science requires GRE scores of at least 300 combined quantitative and verbal with a minimum analytical writing score of 3.0. The GRE may be waived for US degree holders with GPA of 3.0 or higher.",
    },
    {
        "category": "program_requirements",
        "question": "What does the Master of Data Science program include?",
        "ground_truth": "The Master of Data Science is a collaborative program with Applied Mathematics including CSP 570 Data Science Seminar, statistics courses, machine learning, and data management courses.",
    },
    {
        "category": "program_requirements",
        "question": "What is the minimum credit requirement for all master's degrees?",
        "ground_truth": "All master's degrees at IIT require a minimum of 30 credit hours beyond the bachelor's degree.",
    },
    {
        "category": "program_requirements",
        "question": "Does the PhD require a dissertation?",
        "ground_truth": "Yes. The PhD requires an original research contribution presented as a dissertation. At least 36 of the required 72 credit hours must be dissertation research credits.",
    },

    # admission
    {
        "category": "admission",
        "question": "What are the GPA requirements for graduate admission?",
        "ground_truth": "Most graduate programs require a minimum cumulative undergraduate GPA of 3.0 out of 4.0. PhD programs typically require a minimum GPA of 3.5 for master's level work.",
    },
    {
        "category": "admission",
        "question": "Can GRE be waived for engineering applicants?",
        "ground_truth": "Yes. The GRE requirement is waived for Master of Engineering applicants who hold a Bachelor of Science in a related field from an ABET-accredited US university with a minimum GPA of 3.0.",
    },
    {
        "category": "admission",
        "question": "Are letters of recommendation required for graduate admission?",
        "ground_truth": "Letters of recommendation are required for doctoral applicants and strongly encouraged for master of science and professional master's program applicants.",
    },
    {
        "category": "admission",
        "question": "What GRE scores are required for MS in Computer Science?",
        "ground_truth": "MS in Computer Science requires GRE scores of at least 300 combined quantitative and verbal with 3.0 analytical writing. The GRE may be waived for US bachelor's degree holders with a GPA of 3.0 or higher.",
    },
    {
        "category": "admission",
        "question": "Can the GRE be waived for MS in Computer Science?",
        "ground_truth": "Yes, the GRE may be waived for MS in Computer Science applicants who hold a US bachelor's degree with a minimum GPA of 3.0 or higher.",
    },
    {
        "category": "admission",
        "question": "What is the minimum GRE analytical writing score?",
        "ground_truth": "For MS in Computer Science, the minimum GRE analytical writing score is 3.0.",
    },
    {
        "category": "admission",
        "question": "How many letters of recommendation are required?",
        "ground_truth": "The number of required recommendation letters varies by program. Doctoral programs require them; master's programs strongly encourage them.",
    },
    {
        "category": "admission",
        "question": "Is there an English proficiency requirement?",
        "ground_truth": "International students whose native language is not English must demonstrate English proficiency through TOEFL or IELTS scores as part of the graduate admission requirements.",
    },
    {
        "category": "admission",
        "question": "What documents are required for a PhD application?",
        "ground_truth": "PhD applications typically require transcripts, GRE scores, letters of recommendation, a statement of purpose, and for international students, English proficiency test scores.",
    },
    {
        "category": "admission",
        "question": "What is conditional admission?",
        "ground_truth": "Conditional admission may be granted to applicants who do not fully meet all admission requirements. Students admitted conditionally must satisfy specified conditions during their first semester or year.",
    },
    {
        "category": "admission",
        "question": "Can transfer credits be applied toward a graduate degree?",
        "ground_truth": "Graduate students may transfer a limited number of credits from other accredited institutions toward their degree, subject to program approval and time-in-program restrictions.",
    },
    {
        "category": "admission",
        "question": "What is the GPA requirement for PhD programs?",
        "ground_truth": "PhD programs typically require a minimum undergraduate GPA of 3.0 and a minimum master's level GPA of 3.5.",
    },
    {
        "category": "admission",
        "question": "Is a bachelor's degree required for graduate admission?",
        "ground_truth": "Yes, a bachelor's degree from an accredited institution is required for graduate admission at IIT.",
    },
    {
        "category": "admission",
        "question": "What is the GRE combined score requirement for MS programs?",
        "ground_truth": "For MS in Computer Science, a minimum combined GRE score of 300 on the quantitative and verbal sections is required, with a 3.0 analytical writing score.",
    },
    {
        "category": "admission",
        "question": "Are GRE scores required for all graduate programs?",
        "ground_truth": "GRE requirements vary by program. Some programs allow waivers for qualified applicants. Master of Engineering applicants from ABET-accredited US programs with a 3.0 GPA may have the GRE waived.",
    },

    # academic policies
    {
        "category": "policy",
        "question": "What are the credit hour requirements for a PhD?",
        "ground_truth": "The doctoral degree requires 72 credit hours or more beyond the bachelor's degree, of which at least 36 must be dissertation research credits.",
    },
    {
        "category": "policy",
        "question": "How many credits are needed for a master's degree?",
        "ground_truth": "All master's degrees require a minimum of 30 credit hours beyond the bachelor's degree.",
    },
    {
        "category": "policy",
        "question": "What is the time limit to complete a PhD?",
        "ground_truth": "Doctoral study must be completed within six years of the mandatory doctoral advising session.",
    },
    {
        "category": "policy",
        "question": "What is the policy for incomplete grades?",
        "ground_truth": "An incomplete grade may be approved by the instructor only in cases of illness or unforeseeable circumstances. The student must have substantial equity in the course and must complete the remaining work within the timeframe set by the instructor.",
    },
    {
        "category": "policy",
        "question": "What is the policy for repeating courses?",
        "ground_truth": "Graduate students may repeat up to three distinct courses during their academic career. Students who enroll in an entirely new program may petition for an additional repeat.",
    },
    {
        "category": "policy",
        "question": "How many courses can a graduate student repeat?",
        "ground_truth": "Graduate students may repeat up to three distinct courses during their academic career.",
    },
    {
        "category": "policy",
        "question": "What happens if a PhD student does not finish in 6 years?",
        "ground_truth": "Doctoral students must complete their degree within six years of the mandatory doctoral advising session. Students exceeding this limit may need to petition for an extension.",
    },
    {
        "category": "policy",
        "question": "What is the minimum GPA to maintain good standing?",
        "ground_truth": "Graduate students must maintain a minimum cumulative GPA of 3.0 to remain in good academic standing.",
    },
    {
        "category": "policy",
        "question": "How is an incomplete grade resolved?",
        "ground_truth": "An incomplete grade is resolved when the student completes the remaining coursework within the timeframe set by the instructor. If not completed in time, the incomplete typically converts to a failing grade.",
    },
    {
        "category": "policy",
        "question": "How many dissertation credits are required for the PhD?",
        "ground_truth": "At least 36 of the 72 required credit hours for the PhD must be dissertation research credits.",
    },
    {
        "category": "policy",
        "question": "What are the conditions for receiving an incomplete grade?",
        "ground_truth": "An incomplete grade requires instructor approval and is only granted for illness or unforeseeable circumstances. The student must have substantial equity in the course.",
    },
    {
        "category": "policy",
        "question": "Can a graduate student repeat more than 3 courses?",
        "ground_truth": "Graduate students are limited to repeating up to three distinct courses. Students who enroll in an entirely new program may petition for an additional repeat beyond three.",
    },
    {
        "category": "policy",
        "question": "What is the doctoral advising session?",
        "ground_truth": "The mandatory doctoral advising session is a milestone in PhD study. The six-year time limit for completing doctoral study is counted from this advising session.",
    },
    {
        "category": "policy",
        "question": "What is academic probation for graduate students?",
        "ground_truth": "Graduate students who fail to maintain the required GPA may be placed on academic probation. Students on probation must improve their academic standing within the specified timeframe or face academic dismissal.",
    },
    {
        "category": "policy",
        "question": "Is there a minimum GPA for PhD admission different from master's?",
        "ground_truth": "Yes. Most master's programs require a minimum undergraduate GPA of 3.0. PhD programs additionally require a minimum master's level GPA of 3.5.",
    },

    # financial
    {
        "category": "financial",
        "question": "What is the Employer Tuition Deferment Plan?",
        "ground_truth": "The Employer Tuition Deferment Plan allows students employed by a company that offers tuition reimbursement to defer the reimbursable portion of their tuition until three weeks after grades are posted. A non-refundable deferment fee of $55 is due at the time of application. If tuition is not paid within three weeks of grades being posted, the student authorizes their employer to withhold the amount from their pay.",
    },
    {
        "category": "financial",
        "question": "How does employer tuition reimbursement work at IIT?",
        "ground_truth": "Through the Employer Tuition Deferment Plan, students defer the reimbursable portion of their tuition until three weeks after grades are posted. A $55 non-refundable deferment fee is due at application. Any amount not covered by the employer's reimbursement policy is due in full by the end of the add/drop registration period.",
    },
    {
        "category": "financial",
        "question": "Are graduate assistantships available at IIT?",
        "ground_truth": "Most degree programs provide financial support for teaching assistants (TAs) who help with instruction, and research assistants (RAs) who assist with faculty research projects.",
    },
    {
        "category": "financial",
        "question": "Who is eligible for the Employer Tuition Deferment Plan?",
        "ground_truth": "Students who are employed by a company that offers tuition reimbursement are eligible for the Employer Tuition Deferment Plan. Students must meet their employer's qualifying conditions to be reimbursed. If the employer refuses to pay, the student is personally responsible for the full tuition.",
    },
    {
        "category": "financial",
        "question": "What financial support options exist for graduate students?",
        "ground_truth": "Illinois Institute of Technology's Office of Financial Aid administers financial aid programs. Most degree programs provide financial support for teaching assistants and research assistants. The Employer Tuition Deferment Plan is available for students whose employers offer tuition reimbursement.",
    },

    # topic search
    {
        "category": "topic_search",
        "question": "What courses cover deep learning?",
        "ground_truth": "Courses covering deep learning include CS 577 Deep Learning, ECE 501 Artificial Intelligence and Edge Computing, and ITMD 524 Applied Artificial Intelligence and Deep Learning.",
    },
    {
        "category": "topic_search",
        "question": "What courses cover cloud computing?",
        "ground_truth": "Courses covering cloud computing include CS 553 Cloud Computing, ECE 573 Cloud Computing and Cloud Native Systems, and ITMS 564 Cloud Computing Security.",
    },
    {
        "category": "topic_search",
        "question": "What courses are available on machine learning?",
        "ground_truth": "Machine learning courses at IIT include CS 577 Deep Learning, ITMD 524 Applied Artificial Intelligence and Deep Learning, and related courses in the Computer Science and ITMD departments.",
    },
    {
        "category": "topic_search",
        "question": "Which courses focus on network security?",
        "ground_truth": "Network security is covered in ECE 543 Computer Network Security and ITMS 564 Cloud Computing Security, among other cybersecurity-related courses.",
    },
    {
        "category": "topic_search",
        "question": "What courses cover big data?",
        "ground_truth": "Big data courses include CSP 554 Big Data Technologies and ITMD 521 Platforms for Big Data Processing, covering technologies for storing, processing, and analyzing large datasets.",
    },
    {
        "category": "topic_search",
        "question": "What statistics courses are available for graduate students?",
        "ground_truth": "Statistics courses available at the graduate level include MATH 564 Regression, covering regression models, and other courses in the Applied Mathematics department.",
    },
    {
        "category": "topic_search",
        "question": "Are there courses on cybersecurity?",
        "ground_truth": "Yes, cybersecurity courses include ECE 543 Computer Network Security, ITMS 564 Cloud Computing Security, and courses in the Master of Cybersecurity program.",
    },
    {
        "category": "topic_search",
        "question": "What courses cover database systems?",
        "ground_truth": "Database courses include ITMD 514 Database Organization, which covers database design, relational models, SQL, and database management.",
    },
    {
        "category": "topic_search",
        "question": "What AI-related courses are offered?",
        "ground_truth": "AI courses include ECE 501 Artificial Intelligence and Edge Computing, CS 577 Deep Learning, and ITMD 524 Applied Artificial Intelligence and Deep Learning.",
    },
    {
        "category": "topic_search",
        "question": "What courses are recommended for a data science career?",
        "ground_truth": "For a data science career, recommended courses include CSP 554 Big Data Technologies, MATH 564 Regression, CS 577 Deep Learning, ITMD 514 Database Organization, and CSP 570 Data Science Seminar.",
    },

    # adversarial
    {
        "category": "adversarial",
        "question": "What is the undergraduate tuition at IIT?",
        "ground_truth": "Undergraduate tuition information is not covered in the IIT Graduate Catalog 2024-2025. This falls outside the scope of the graduate catalog.",
    },
    {
        "category": "adversarial",
        "question": "Where are the IIT dormitories located?",
        "ground_truth": "Housing and residential life information is not covered in the IIT Graduate Catalog 2024-2025. Students should contact IIT housing services directly.",
    },
    {
        "category": "adversarial",
        "question": "What is the weather like in Chicago?",
        "ground_truth": "Weather information is outside the scope of the IIT Graduate Catalog. The catalog covers graduate programs, courses, admission, and academic policies.",
    },
    {
        "category": "adversarial",
        "question": "How do I apply for a student visa to study at IIT?",
        "ground_truth": "Student visa application processes are not detailed in the graduate catalog. International students should contact IIT's Office of International Affairs for visa guidance.",
    },
    {
        "category": "adversarial",
        "question": "What is the parking situation on the IIT main campus?",
        "ground_truth": "Parking and campus facilities information is not covered in the IIT Graduate Catalog. This falls outside the scope of the graduate academic catalog.",
    },
    {
        "category": "adversarial",
        "question": "Compare CS 577 and ITMD 524 for someone interested in deep learning",
        "ground_truth": "CS 577 Deep Learning covers deep neural network architectures including feedforward, convolutional, and sequence models with CS 430 as prerequisite. ITMD 524 Applied AI and Deep Learning focuses on practical applications. Both cover deep learning but differ in theoretical depth and prerequisite requirements.",
    },
    {
        "category": "adversarial",
        "question": "What is the difference between the MS and the Master of Engineering?",
        "ground_truth": "The Master of Science is a research-oriented degree. The Master of Engineering is a professional degree. The GRE may be waived for Master of Engineering applicants from ABET-accredited US programs with a 3.0 GPA.",
    },
    {
        "category": "adversarial",
        "question": "Can I take CSP 554 and CS 577 in the same semester?",
        "ground_truth": "The catalog does not restrict taking CSP 554 and CS 577 in the same semester, provided prerequisite requirements are met. CSP 554 requires CS 425 and CS 577 requires CS 430.",
    },
    {
        "category": "adversarial",
        "question": "What is the ranking of IIT's Computer Science program?",
        "ground_truth": "Program rankings are not covered in the IIT Graduate Catalog. This information falls outside the scope of the academic catalog.",
    },
    {
        "category": "adversarial",
        "question": "How does IIT compare to other universities for data science?",
        "ground_truth": "Comparative rankings and institutional comparisons are not covered in the IIT Graduate Catalog. The catalog covers IIT graduate programs, courses, and academic policies only.",
    },
]
