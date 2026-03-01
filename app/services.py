from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_keywords(text):
    doc = nlp(text)
    keywords = set()

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            keywords.add(token.text.lower())

    return keywords

def compute_similarity(text1, text2):
    embedding1 = model.encode(text1)
    embedding2 = model.encode(text2)

    score = cosine_similarity([embedding1], [embedding2])[0][0]

    return round(float(score) * 100, 2)

def calculate_skill_match(resume_keywords, jd_keywords):
    matched = resume_keywords.intersection(jd_keywords)
    missing = jd_keywords.difference(resume_keywords)

    if len(jd_keywords) == 0:
        keyword_score = 0
    else:
        keyword_score = (len(matched) / len(jd_keywords)) * 100

    return matched, missing, round(keyword_score, 2)

def calculate_final_score(semantic_score, keyword_score):
    final_score = (0.6 * semantic_score) + (0.4 * keyword_score)
    return round(final_score, 2)