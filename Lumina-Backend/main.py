from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(
    title="Lumina Content Factory",
    description="API REST exposant les modèles mentaux générés et validés par le pipeline LangGraph.",
    version="0.2.0",
)

app.include_router(api_router)


@app.get("/health", tags=["System"])
def health_check():
    """Vérifie que le serveur FastAPI est opérationnel."""
    return {"status": "ok"}