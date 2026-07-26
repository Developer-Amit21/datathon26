from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class CaseRecord(Base):
    __tablename__ = "case_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    district = Column(String, nullable=False)
    police_station = Column(String, nullable=False)
    occurred_on = Column(Date, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accused_name = Column(String, nullable=False)
    victim_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    is_repeat_offender = Column(Boolean, default=False)
    risk_score = Column(Float, default=0.0)
    tags = Column(String, default="")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    transcript = Column(Text, nullable=False)
    language = Column(String, default="en")


class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_account = Column(String, nullable=False, index=True)
    receiver_account = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_suspicious = Column(Boolean, default=False)
    flag_reason = Column(String, default="")


class OffenderProfile(Base):
    __tablename__ = "offender_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    alias = Column(String, default="")
    primary_mo = Column(String, nullable=False)
    associated_gang = Column(String, default="Independent")
    total_offenses = Column(Integer, default=1)
    recidivism_risk_score = Column(Float, default=0.5)
    mobility_index = Column(Float, default=0.3)
    known_associates = Column(Text, default="")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    role = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, default="127.0.0.1")

