from typing import Literal
from langgraph.graph import END, START, StateGraph

from agents.nodes import editor_node, researcher_node, writer_node
from agents.state import LuminaState

# Plafond de sécurité pour garantir la terminaison du graphe
MAX_REVISIONS = 2


def route_after_editor(state: LuminaState) -> Literal["revise", "approved"]:
    """Décide si le brouillon est validé ou doit retourner chez le Writer."""
    if state.get("is_approved", False):
        return "approved"
    if state.get("revision_count", 0) >= MAX_REVISIONS:
        return "approved"
    return "revise"


def build_lumina_graph():
    """Construit et compile le StateGraph multi-agents de Lumina."""
    builder = StateGraph(LuminaState)

    # 1. Déclaration des nœuds
    builder.add_node("researcher", researcher_node)
    builder.add_node("writer", writer_node)
    builder.add_node("editor", editor_node)

    # 2. Connexions linéaires principales
    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "editor")

    # 3. Boucle de validation conditionnelle
    builder.add_conditional_edges(
        "editor",
        route_after_editor,
        {
            "revise": "writer",
            "approved": END,
        },
    )

    return builder.compile()


# Instance compilée une seule fois au démarrage (évite de reconstruire le graphe à chaque requête)
lumina_graph = build_lumina_graph()


if __name__ == "__main__":
    # Test rapide en ligne de commande : python -m agents.graph
    result = lumina_graph.invoke({"topic": "Rasoir d'Ockham", "revision_count": 0})
    print("Approuvé :", result["is_approved"], "| Révisions :", result["revision_count"])
    print("Carte générée :", result["draft"].model_dump_json(indent=2))