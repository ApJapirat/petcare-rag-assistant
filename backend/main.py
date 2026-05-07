"""FastAPI app for the PetCare RAG demo."""

import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api.routes import router
from backend.core.config import FRONTEND_STATIC_DIR, INDEX_HTML

app = FastAPI(title="PetCare RAG Assistant")
app.include_router(router)
app.mount("/static", StaticFiles(directory=FRONTEND_STATIC_DIR), name="static")


@app.get("/")
def home():
    """เสิร์ฟหน้าเว็บหลัก"""
    return FileResponse(INDEX_HTML)
