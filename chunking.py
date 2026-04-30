from sentence_transformers import SentenceTransformer
import numpy as np
import nltk
import re

nltk.download("punkt_tab", quiet = True)

model = SentenceTransformer("all-MiniLM-L6-v2")

# cosine similarity
def cosine(a, b):
    return np.dot(a, b)/ (np.linalg.norm(a) * np.linalg.norm(b))

def split(text):
    return nltk.sent_tokenize(text)

# text = """Students must submit assignments before the deadline.
#     Late submissions will receive a 10% penalty per day.
#     The cafeteria is open from 8am to 8pm on weekdays.
#     Lunch includes vegetarian and vegan meal options.
# """

# sentences = split(text)

# def simi(senteces):

#     embeddings = model.encode(senteces)
#     similarities = []

#     for i in range(len(senteces) - 1):

#         sim = cosine(embeddings[i], embeddings[i+1])
#         similarities.append(sim)
    
#     return similarities, embeddings

# similarities, embeddings = simi(sentences)

# for i, sim in enumerate(similarities):
#     print(f"{i+1} -> {i+2}: {sim:.4f}")


# # boundary detection
# def boundary(similarities, percentile = 25):

#     threshold = np.percentile(similarities, percentile)
#     boundaries = []
#     for i, sim in enumerate(similarities):

#         if sim < threshold:
#             boundaries.append(i)
#     return boundaries, threshold

# boundaries, threshold = boundary(similarities)

# print(f"Threshold: {threshold:.4f}")
# print(f"Boundaries after sentence index: {boundaries}")

# def chunks(sentences, boundaries):

#     chunks = []
#     start = 0
#     for boundary in boundaries:

#         chunk = " ".join(sentences[start: boundary + 1])
#         chunks.append(chunk)
#         start = boundary + 1

#     chunks.append(" ".join(sentences[start:]))
#     return chunks

# chunks = chunks(sentences, boundaries)
# for i, chunk in enumerate(chunks):

#     print(f"\nChunk {i+1}:\n{chunk}")

def semantic_chunk(text):

    sentences = nltk.sent_tokenize(text)

    if len(sentences) < 2:
        return [text.strip()]

    embeddings = model.encode(sentences)

    similarities = []
    for i in range(len(sentences) - 1):
        
        sim = cosine(embeddings[i], embeddings[i+1])
        similarities.append(sim)

    threshold = np.percentile(similarities, 25)

    boundaries = []
    for i, sim in enumerate(similarities):

        if sim < threshold:
            boundaries.append(i)
    
    chunks = []
    start = 0

    for boundary in boundaries:

        chunk = " ".join(sentences[start: boundary + 1])
        chunks.append(chunk)
        start = boundary + 1

    chunks.append(" ".join(sentences[start:]))

    return merge(chunks)

def merge(chunks, size = 200):

    merged = []
    buffer = ""

    for chunk in chunks:
        if len(buffer) + len(chunk) < size:
            buffer = buffer + " " + chunk
        else:
            if buffer:
                merged.append(buffer.strip())
            buffer = chunk

    if buffer:
        merged.append(buffer.strip())

    return merged

def descriptions(text):

    matches = list(re.finditer(r'^[A-Z]{2,5}\s\d{3}', text, re.MULTILINE))

    if not matches:
        return [text.strip()]

    chunks = []

    for i, match in enumerate(matches):
        start = match.start()

        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

    return chunks 

# new_text = """      
#   Students are expected to attend all lectures and labs.                                                                                                                                                                     
#   Attendance will be taken at the beginning of each session.                                                                                                                                                                 
#   More than three unexcused absences may result in a grade penalty.
                                                                                                                                                                                                                             
#   The course covers machine learning fundamentals including supervised and unsupervised learning. 
#   Week 3 focuses on linear regression and gradient descent.                                                                                                                                                                  
#   Neural networks and deep learning are introduced in week 7.                                                                                                                                                                
                                                                                                                                                                                                                             
#   All assignments must be submitted through the course portal.                                                                                                                                                               
#   Late submissions will be penalized 10% per day.                                                                                                                                                                            
#   Extensions will only be granted with prior approval from the instructor.
#   """                                                                                                                                                                                                                        

# print(semantic_chunk(new_text))