from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="AI Resume Analyzer")

app.include_router(router)