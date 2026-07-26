from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, chat, analytics, graph, forecast, auth, financial, audit
from app.db.base import Base, engine
from app.db.seed import seed_demo_data

app = FastAPI(title="Crime Intelligence Platform", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(graph.router, prefix="/api/graph", tags=["graph"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["forecast"])
app.include_router(financial.router, prefix="/api/financial", tags=["financial"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])


@app.on_event("startup")
def startup_event() -> None:
    # The database is intentionally created up front so the demo environment is fully runnable.
    Base.metadata.create_all(bind=engine)
    seed_demo_data()
