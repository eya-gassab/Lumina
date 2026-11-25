from agents.graph import lumina_pipeline
from api.storage import save_daily_concepts


def run_factory(topics: list[str]) -> list[dict]:
    """Exécute le pipeline LangGraph et ne conserve que les concepts approuvés par l'Editor."""
    approved_results = []
    for topic in topics:
        print(f"\n{'='*50}\n🚀 Lancement pipeline pour : {topic}\n{'='*50}")
        final_state = lumina_pipeline.invoke({
            "topic": topic,
            "research_notes": "",
            "draft": None,
            "is_approved": False,
            "feedback": "",
            "revision_count": 0,
        })
        if final_state.get("is_approved") and final_state.get("draft"):
            approved_results.append(final_state["draft"].model_dump())
            print(f"✅ Approuvé et retenu : {topic}")
        else:
            print(f"⛔ Rejeté après {final_state.get('revision_count', 0)} révisions : {topic}")
    return approved_results


if __name__ == "__main__":
    sample_topics = [
        "Le Rasoir d'Ockham",
        "Le Biais des Coûts Irrécupérables (Sunk Cost Fallacy)",
        "La Loi de Parkinson",
    ]
    concepts = run_factory(sample_topics)
    saved = save_daily_concepts(concepts)
    print(f"\n📦 {saved.count} concepts approuvés sauvegardés dans data/daily_concepts.json")