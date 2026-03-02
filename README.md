# AI-Powered Resume Analyzer (ATS Simulation)

An ATS-style resume evaluation engine built with **FastAPI** that combines keyword matching and semantic similarity using transformer-based embeddings to score and rank candidates against job descriptions.

---

## Overview

Traditional Applicant Tracking Systems (ATS) rely heavily on exact keyword matching.  
This project enhances that approach by integrating semantic understanding using transformer embeddings.

The system:

- Extracts skills using NLP (spaCy)
- Computes semantic similarity using MiniLM
- Combines keyword and semantic scoring
- Measures improvement over keyword-only baseline
- Supports multi-resume ranking

---

## Core Features

- PDF resume parsing using `pdfplumber`
- Keyword extraction using `spaCy`
- Semantic similarity using `sentence-transformers`
- Hybrid weighted scoring model
- Multi-candidate ranking
- Skill gap detection (matched & missing skills)

---

## Scoring Methodology

### Baseline Score (Keyword-Only)

```text
keyword_score = (matched_keywords / total_jd_keywords) * 100
```

### Semantic Similarity

```text
semantic_score = cosine_similarity(resume_embedding, jd_embedding)
```

### Hybrid Advanced Score

```text
final_score = keyword_score + (0.3 * semantic_score)
```

---

## Improvement Calculation

```text
improvement_percentage = ((advanced_score - baseline_score) / baseline_score) * 100
```

Observed improvement range:

- Typical: 10–25%
- Strong semantic alignment: up to ~30%

---

## API Endpoints

### POST /analyze

Returns:

- baseline_keyword_score
- advanced_weighted_score
- improvement_percentage
- semantic_similarity_score
- matched_skills_count
- missing_skills_count

### POST /rank

Returns:

- average_improvement_percentage
- ranked_candidates (sorted by advanced score)

---

## Project Structure

```text
ai-resume-analyzer/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── services.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone <repo-url>
cd ai-resume-analyzer
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download spaCy model:

```bash
python -m spacy download en_core_web_sm
```

Run the server:

```bash
uvicorn app.main:app
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## Tech Stack

- FastAPI
- spaCy
- SentenceTransformers (MiniLM)
- scikit-learn
- pdfplumber
