import re
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.domain import AuditLog


class SecurityGovernanceService:
    """Enterprise Security & Governance service managing fine-grained RBAC, 
    prompt injection sanitization, PII masking, and audit logging."""

    ROLES_PERMISSIONS = {
        "INVESTIGATOR": ["read_cases", "read_network", "read_forecast", "chat_query", "voice_query"],
        "ANALYST": ["read_cases", "read_network", "read_forecast", "read_financial", "export_reports"],
        "ADMIN": ["read_cases", "read_network", "read_forecast", "read_financial", "export_reports", "manage_users", "view_audit"],
        "AUDITOR": ["read_cases", "view_audit"]
    }

    PROMPT_INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"system prompt",
        r"drop database",
        r"delete from",
        r"reveal passwords",
        r"bypass auth"
    ]

    def __init__(self, db: Session):
        self.db = db

    def check_permission(self, role: str, required_permission: str) -> bool:
        user_permissions = self.ROLES_PERMISSIONS.get(role.upper(), [])
        return required_permission in user_permissions

    def sanitize_prompt(self, user_prompt: str) -> Dict[str, Any]:
        normalized = user_prompt.lower()
        for pattern in self.PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, normalized):
                return {
                    "is_safe": False,
                    "sanitized_prompt": "[BLOCKED] Potential Prompt Injection Detected",
                    "reason": f"Matched suspicious pattern: {pattern}"
                }
        return {
            "is_safe": True,
            "sanitized_prompt": user_prompt,
            "reason": "Clean input"
        }

    def mask_pii(self, text: str) -> str:
        # Mask 12-digit Aadhaar / 10-digit Phone numbers
        masked = re.sub(r"\b\d{10}\b", "XXXXXX-PHONE", text)
        masked = re.sub(r"\b\d{12}\b", "XXXX-XXXX-AADHAAR", masked)
        return masked

    def log_audit(self, user_id: str, role: str, action: str, resource: str) -> None:
        log_entry = AuditLog(
            user_id=user_id,
            role=role,
            action=action,
            resource=resource,
            timestamp=datetime.utcnow(),
            ip_address="127.0.0.1"
        )
        self.db.add(log_entry)
        self.db.commit()

    def get_audit_trail(self, limit: int = 10) -> List[Dict[str, Any]]:
        logs = self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
        return [
            {
                "id": log.id,
                "user_id": log.user_id,
                "role": log.role,
                "action": log.action,
                "resource": log.resource,
                "timestamp": str(log.timestamp),
                "ip_address": log.ip_address
            }
            for log in logs
        ]
