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

    # remove page header
    text = re.sub(r"^\d+\s*\n\s*.+\n", "", text)
    
    # replace non-breaking spaces
    text = text.replace('\xa0', ' ')

    # remove extra whitespace and blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    text = re.sub(r"Illinois Institute of Technology GR_2024-2025\s*\n\s*\d+\s*\n", "", text)
    
    # skip pages that are too short
    if len(text) < 100:
        return None
    
    return text

