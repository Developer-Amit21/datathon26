import re
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.domain import CaseRecord


class RagService:
    """A production-oriented retrieval layer that combines lexical and metadata scoring."""

    def __init__(self, db: Session):
        self.db = db

    def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, object]]:
        normalized = query.lower()
        records = self.db.query(CaseRecord).all()
        scored: List[Dict[str, object]] = []

        for record in records:
            text = " ".join(
                [
                    record.title,
                    record.category,
                    record.district,
                    record.police_station,
                    record.description,
                    record.accused_name,
                    record.victim_name,
                    record.tags,
                ]
            ).lower()
            lexical_score = self._bm25_like_score(normalized, text)
            metadata_score = self._metadata_score(normalized, record)
            total_score = lexical_score + metadata_score
            if total_score > 0:
                scored.append(
                    {
                        "case": record,
                        "score": round(total_score, 3),
                        "evidence": f"Matched {record.category} in {record.district} around {record.police_station}",
                    }
                )

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:limit]

    def _bm25_like_score(self, query: str, text: str) -> float:
        tokens = re.findall(r"[a-z0-9]+", query)
        if not tokens:
            return 0.0
        score = 0.0
        for token in tokens:
            if token in text:
                score += 1.0
        return score

    def _metadata_score(self, query: str, record: CaseRecord) -> float:
        score = 0.0
        if record.category.lower() in query:
            score += 1.5
        if record.district.lower() in query:
            score += 1.5
        if record.police_station.lower() in query:
            score += 1.0
        if record.accused_name.lower() in query:
            score += 1.5
        if "repeat" in query and record.is_repeat_offender:
            score += 2.0
        return score
