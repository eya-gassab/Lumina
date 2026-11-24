from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes import researcher_node, writer_node, editor_node

MAX_REVISIONS = 2


def should_continue(state: AgentState) -> str:
    """Décide si on termine ou si on renvoie le brouillon au Writer."""
    if state["is_approved"] or state["revision_count"] >= MAX_REVISIONS:
        return END
    return "writer"


def build_lumina_graph():
    """Construit et compile le workflow multi-agents Lumina."""
    workflow = StateGraph(AgentState)

    # 1. Ajout des nœuds
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("editor", editor_node)

    # 2. Définition du flux séquentiel
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "editor")

    # 3. Boucle conditionnelle de validation
    workflow.add_conditional_edges(
        "editor",
        should_continue,
        {
            "writer": "writer",
            END: END
        }
    )

    return workflow.compile()


# Instance compilée prête à être importée par FastAPI demain
lumina_pipeline = build_lumina_graph()