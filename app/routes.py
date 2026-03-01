from fastapi import APIRouter, UploadFile, File, Form
from app.services import extract_text_from_pdf, extract_keywords
from app.services import compute_similarity
from app.services import calculate_skill_match
from app.services import calculate_final_score

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

    return {
        "overall_ats_score": final_score,
        "semantic_similarity_score": similarity_score,
        "keyword_match_score": keyword_score,
        "matched_skills_count": len(matched),
        "missing_skills_count": len(missing)
    }