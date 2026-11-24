from fastapi import FastAPI
from agents.graph import lumina_graph

app = FastAPI(
    title="Lumina Content Factory",
    description="Backend multi-agents LangGraph pour la génération de modèles mentaux.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Vérifie que le serveur FastAPI est opérationnel."""
    return {"status": "ok"}


@app.post("/debug/run-graph")
def run_graph_debug(topic: str = "Principe de Pareto"):
    """
    Endpoint temporaire de test pour exécuter le graphe LangGraph de bout en bout.
    Sera remplacé par le pipeline batch + GET /api/daily mercredi.
    """
    final_state = lumina_graph.invoke({"topic": topic, "revision_count": 0})
    return {
        "approved": final_state["is_approved"],
        "revisions": final_state["revision_count"],
        "card": final_state["draft"],
    }