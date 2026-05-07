"""Service layer for loading and calling the PetCare RAG system."""

import os
from functools import lru_cache
from typing import Any

from rag.answer import PetRAG


@lru_cache(maxsize=1)
def get_rag() -> PetRAG:
    """โหลด RAG หนึ่งครั้งแล้ว cache ไว้ให้ API ใช้ซ้ำ"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    return PetRAG(llm_provider="gemini", api_key=api_key)


def answer_question(question: str, top_k: int = 3) -> dict[str, Any]:
    """ส่งคำถามให้ RAG แล้วคืนผลลัพธ์ดิบรูปแบบเดิม"""
    return get_rag().answer(question, top_k=top_k)
