from datetime import date, datetime
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.domain import CaseRecord, FinancialTransaction, OffenderProfile


def seed_demo_data() -> None:
    db: Session = SessionLocal()
    if db.query(CaseRecord).count() == 0:
        records = [
            CaseRecord(
                title="Theft FIR 101",
                category="Theft",
                district="Bangalore",
                police_station="HSR Layout",
                occurred_on=date(2025, 1, 10),
                latitude=12.91,
                longitude=77.65,
                accused_name="Ravi Kumar",
                victim_name="Asha Menon",
                severity="High",
                description="Vehicle theft near a residential lane.",
                is_repeat_offender=True,
                risk_score=0.89,
                tags="theft,bangalore,repeat",
            ),
            CaseRecord(
                title="Robbery FIR 205",
                category="Robbery",
                district="Bangalore",
                police_station="Central",
                occurred_on=date(2025, 1, 15),
                latitude=12.97,
                longitude=77.59,
                accused_name="Shiva Rao",
                victim_name="Meera Das",
                severity="Critical",
                description="Robbery near railway station.",
                is_repeat_offender=False,
                risk_score=0.78,
                tags="robbery,railway",
            ),
            CaseRecord(
                title="Cyber Fraud FIR 330",
                category="Cyber Crime",
                district="Mysuru",
                police_station="V V Puram",
                occurred_on=date(2024, 11, 18),
                latitude=12.30,
                longitude=76.64,
                accused_name="Nisha V",
                victim_name="Prakash R",
                severity="Medium",
                description="UPI fraud and account compromise.",
                is_repeat_offender=False,
                risk_score=0.62,
                tags="cyber,upi,financial",
            ),
        ]
        db.add_all(records)

    if db.query(FinancialTransaction).count() == 0:
        txs = [
            FinancialTransaction(
                sender_account="ACC-1092",
                receiver_account="ACC-9921",
                amount=250000.0,
                transaction_type="WIRE",
                timestamp=datetime(2025, 1, 12, 14, 30),
                is_suspicious=True,
                flag_reason="Layering - Rapid multi-account split",
            ),
            FinancialTransaction(
                sender_account="ACC-9921",
                receiver_account="ACC-8833",
                amount=245000.0,
                transaction_type="CRYPTO_EXCHANGE",
                timestamp=datetime(2025, 1, 12, 14, 45),
                is_suspicious=True,
                flag_reason="Structuring below reporting threshold",
            ),
            FinancialTransaction(
                sender_account="ACC-3341",
                receiver_account="ACC-1092",
                amount=15000.0,
                transaction_type="UPI",
                timestamp=datetime(2025, 1, 14, 10, 15),
                is_suspicious=False,
                flag_reason="",
            ),
        ]
        db.add_all(txs)

    if db.query(OffenderProfile).count() == 0:
        profiles = [
            OffenderProfile(
                name="Ravi Kumar",
                alias="Shadow",
                primary_mo="Vehicle Break-in",
                associated_gang="Koramangala Network",
                total_offenses=5,
                recidivism_risk_score=0.89,
                mobility_index=0.75,
                known_associates="Shiva Rao, Suresh P",
            ),
            OffenderProfile(
                name="Shiva Rao",
                alias="Blade",
                primary_mo="Armed Mugging",
                associated_gang="Koramangala Network",
                total_offenses=3,
                recidivism_risk_score=0.78,
                mobility_index=0.45,
                known_associates="Ravi Kumar",
            ),
        ]
        db.add_all(profiles)

    db.commit()
    db.close()

