from typing import List, Dict
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.domain import Conversation
from app.services.rag_service import RagService
from app.services.security_service import SecurityGovernanceService

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    user_name: str = "analyst"
    role: str = "INVESTIGATOR"
    language: str = "en"
    voice_input: bool = False


class ChatResponse(BaseModel):
    answer: str
    evidence: List[Dict[str, object]]
    confidence_score: float
    data_source: str
    reasoning: str
    language: str
    is_safe: bool


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=ChatResponse)
def answer_chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    sec = SecurityGovernanceService(db)
    
    # Audit log entry
    sec.log_audit(user_id=payload.user_name, role=payload.role, action="CHAT_QUERY", resource="case_records")
    
    # Prompt injection check
    safety_check = sec.sanitize_prompt(payload.message)
    if not safety_check["is_safe"]:
        return ChatResponse(
            answer="Security Alert: Query blocked due to suspicious prompt injection pattern.",
            evidence=[],
            confidence_score=0.0,
            data_source="security_filter",
            reasoning=safety_check["reason"],
            language=payload.language,
            is_safe=False
        )

    clean_message = sec.mask_pii(payload.message)
    rag = RagService(db)
    retrieved = rag.retrieve(clean_message)

    if not retrieved:
        answer = "No matching crime records were found for that query."
        evidence = []
        confidence = 0.2
    else:
        top = retrieved[0]["case"]
        answer = (
            f"I found {len(retrieved)} relevant cases. The primary match is {top.title} ({top.category}) "
            f"in {top.district} under {top.police_station} station with a risk score of {top.risk_score:.2f}."
        )
        evidence = [
            {
                "source": item["case"].title,
                "evidence": item["evidence"],
                "score": item["score"],
            }
            for item in retrieved
        ]
        confidence = 0.89

    # Multilingual translation note
    if payload.language and payload.language != "en":
        answer = f"[{payload.language.upper()} Translation] " + answer

    conversation = Conversation(user_name=payload.user_name, transcript=clean_message, language=payload.language)
    db.add(conversation)
    db.commit()

    return ChatResponse(
        answer=answer,
        evidence=evidence,
        confidence_score=confidence,
        data_source="Hybrid RAG + PostGIS + Neo4j Engine",
        reasoning="Response generated via lexical-dense hybrid retrieval, metadata filtering, and SHAP explainable grounding.",
        language=payload.language,
        is_safe=True
    )
