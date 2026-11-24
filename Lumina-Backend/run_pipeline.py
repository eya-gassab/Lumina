import json
from agents.graph import lumina_pipeline


def run_factory(topics: list[str]) -> list[dict]:
    """Exécute le pipeline LangGraph pour une liste de modèles mentaux."""
    results = []
    for topic in topics:
        print(f"\n{'='*50}\n🚀 Lancement pipeline pour : {topic}\n{'='*50}")
        final_state = lumina_pipeline.invoke({
            "topic": topic,
            "research_notes": "",
            "draft": None,
            "is_approved": False,
            "feedback": "",
            "revision_count": 0
        })
        if final_state["draft"]:
            results.append(final_state["draft"].model_dump())
    return results


if __name__ == "__main__":
    sample_topics = [
        "Le Rasoir d'Ockham",
        "Le Biais des Coûts Irrécupérables (Sunk Cost Fallacy)",
        "La Loi de Parkinson"
    ]
    concepts = run_factory(sample_topics)

    print("\n📦 RÉSULTAT FINAL (JSON prêt pour FastAPI / Android) :")
    print(json.dumps(concepts, indent=2, ensure_ascii=False))