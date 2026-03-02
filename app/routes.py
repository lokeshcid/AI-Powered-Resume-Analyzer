from fastapi import APIRouter, UploadFile, File, Form
from app.services import extract_text_from_pdf, extract_keywords
from app.services import compute_similarity
from app.services import calculate_skill_match
from app.services import calculate_final_score
from typing import List

router = APIRouter()

@router.get("/")
def root():
    return {"message": "ATS Engine Running"}

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(resume.file)

    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    similarity_score = compute_similarity(resume_text, job_description)

    matched, missing, keyword_score = calculate_skill_match(
        resume_keywords, jd_keywords
    )

    final_score = calculate_final_score(
        similarity_score,
        keyword_score
    )

    baseline_score = keyword_score
    advanced_score = final_score

    if baseline_score > 0:
        improvement_percentage = (
            (advanced_score - baseline_score) / baseline_score
        ) * 100
    else:
        improvement_percentage = 0

    return {
        "baseline_keyword_score": baseline_score,
        "advanced_weighted_score": advanced_score,
        "improvement_percentage": round(improvement_percentage, 2),
        "semantic_similarity_score": similarity_score,
        "matched_skills_count": len(matched),
        "missing_skills_count": len(missing)
    }

@router.post("/rank")
async def rank_resumes(
    resumes: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    results = []

    for resume in resumes:
        resume_text = extract_text_from_pdf(resume.file)

        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(job_description)

        similarity_score = compute_similarity(resume_text, job_description)

        matched, missing, keyword_score = calculate_skill_match(
            resume_keywords, jd_keywords
        )

        final_score = calculate_final_score(
            similarity_score,
            keyword_score
        )

        baseline_score = keyword_score
        advanced_score = final_score

        if baseline_score > 0:
            improvement_percentage = (
                (advanced_score - baseline_score) / baseline_score
            ) * 100
        else:
            improvement_percentage = 0

        results.append({
            "filename": resume.filename,
            "baseline_keyword_score": baseline_score,
            "advanced_weighted_score": advanced_score,
            "improvement_percentage": round(improvement_percentage, 2),
            "semantic_similarity_score": similarity_score
        })

    ranked = sorted(
        results,
        key=lambda x: x["advanced_weighted_score"],
        reverse=True
    )

    # Optional: calculate average improvement
    if ranked:
        avg_improvement = sum(r["improvement_percentage"] for r in ranked) / len(ranked)
    else:
        avg_improvement = 0

    return {
        "average_improvement_percentage": round(avg_improvement, 2),
        "ranked_candidates": ranked
    }