import re

DEPT_MAP = {
    "BME": "Biomedical Engineering",
    "CAE": "Civil, Architectural, and Environmental Engineering",
    "CS": "Computer Science",
    "CSP": "Computer Science",
    "ECE": "Electrical and Computer Engineering",
    "MMAE": "Mechanical, Materials, and Aerospace Engineering",
    "CHE": "Chemical and Biological Engineering",
    "MATH": "Mathematics",
    "PHYS": "Physics",
    "ARCH": "Architecture",
    "BA": "Stuart School of Business",
    "FIN": "Stuart School of Business",
    "MGT": "Stuart School of Business",
    "ITMD": "Information Technology and Management",
    "ITMS": "Information Technology and Management",
    "ITMT": "Information Technology and Management",
    "IE": "Industrial Engineering",
    "ENVE": "Environmental Engineering",
    "COM": "Communication",
    "PSYC": "Psychology",
    "SCI": "Science",
    "MAE": "Mechanical and Aerospace Engineering",
    "BUS": "Stuart School of Business",
    "HUM": "Humanities",
    "LA": "Landscape Architecture",
    "FDSN": "Food Safety and Nutrition",
    "PHIL": "Philosophy",
    "ITM": "Information Technology and Management",
    "TECH": "Technology",
    "SMGT": "Sports Management",
    "STAT": "Statistics",
    "ITMO": "Information Technology and Management",
    "MAX": "Maxwell Institute",
    "BIOL": "Biology",
    "SSB": "Stuart School of Business",
    "MBA": "Stuart School of Business",
    "IDX": "Institute of Design",
    "HIST": "History",
    "CHEM": "Chemistry",
    "SAM": "Sustainability Analytics and Management",
    "BIM": "Building Information Modeling",
    "MSC": "Stuart School of Business",
    "IDN": "Institute of Design",
    "PA": "Public Administration",
    "EMS": "Environmental Management and Sustainability",
    "ITMM": "Information Technology and Management",
    "ENGR": "Engineering",
    "MSF": "Master of Science in Finance",
}

def get_department(course_code):
    prefix = course_code.split()[0]
    return DEPT_MAP.get(prefix, "Unknown")

def extract_descp_metadata(text):

    metadata = {}

    # course code
    first_line = text.strip().split('\n')[0].strip()
    code_match = re.match(r'^([A-Z]{2,5}\s\d{3})', first_line)
    if code_match:
        metadata['course_code'] = code_match.group(1).replace('\xa0', ' ')
        metadata['department'] = get_department(metadata['course_code'])

    lines = text.strip().split('\n')
    if len(lines) > 1:
        metadata['course_title'] = lines[1].strip()

    lecture_match = re.search(r'Lecture:\s*(\d+)', text)
    if lecture_match:
        metadata['lectures'] = int(lecture_match.group(1))

    lab_match = re.search(r'Lab:\s*(\d+)', text)
    if lab_match:
        metadata['labs'] = int(lab_match.group(1))

    credits_match = re.search(r'Credits:\s*(\d+)', text)
    if credits_match:
        metadata['credits'] = int(credits_match.group(1))
    elif re.search(r'[Vv]ariable\s*credit|[Cc]redit.*[Vv]ariable|\d+[-–]\d+\s*hours?', text):
        metadata['credits'] = 'Variable'

    return metadata

def extract_curriculum_metadata(text):
    
    metadata = {}

    program_match = re.search(
        r'(Master of [^\n]+|Doctor of Philosophy in [^\n]+|Master of Engineering in [^\n]+|Certificate in [^\n]+)',
        text
    )

    if program_match:
        metadata['program'] = program_match.group(1).strip()
    
    return metadata