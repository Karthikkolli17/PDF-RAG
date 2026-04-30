import re
from pageSplitter import load

def classify(text):

    if len(text) < 200:
        return "skip"
    
    if "TABLE OF CONTENTS" in text or text.count("...") > 5:
        return "toc"
    
    codes = re.findall(r'[A-Z]{2,5}\s\d{3}', text)

    if len(codes) >= 3 and "Lecture: " in text:
        return "descriptive"
    
    credit_pattern = re.findall(r'\n\d{1,2}\n|\s\d{1,2}$', text, re.MULTILINE)
    if len(codes) >= 8 and len(credit_pattern) >=5 and "Lecture: " not in text:
        return "curriculum"
    
    if len(text) > 1500:
        return "prose"
    
    return "mixed"