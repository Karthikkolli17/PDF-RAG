import fitz

def load(path):

    doc = fitz.open(path)
    pages = []
    for num, page in enumerate(doc):

        text = page.get_text().strip()
        if text:
            pages.append({
                "page": num+1,
                "text": text
            })
    return pages

pages = load("2025-2026 Student Handbook Final Copy_0.pdf")
print(f"Total Pages: ", {len(pages)})
print(f"\nPage 5 sample: \n{pages[4]["text"][:300]}")