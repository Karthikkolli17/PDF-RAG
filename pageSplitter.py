import fitz
import re

def load(path):

    doc = fitz.open(path)
    pages = []
    for num, page in enumerate(doc):

        text = page.get_text().strip()
        text = clean(text)
        if text:
            pages.append({
                "page": num+1,
                "text": text
            })
    return pages

def clean(text):

    # remove "Student Handbook #"
    text = re.sub(r"Student Handbook\s+\d+", "", text)
    
    # remove extra whitespace and blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # skip pages that are too short
    if len(text) < 100:
        return None
    
    return text

