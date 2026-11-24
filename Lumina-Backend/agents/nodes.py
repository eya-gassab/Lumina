import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from agents.state import AgentState, ConceptOutput, EditorReview
from agents.prompts import RESEARCHER_PROMPT, WRITER_PROMPT, EDITOR_PROMPT

load_dotenv()

# Modèle unique partagé : rapide, performant en français, température basse pour la rigueur
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY")
)

# Versions avec sortie JSON garantie via Pydantic
writer_llm = llm.with_structured_output(ConceptOutput)
editor_llm = llm.with_structured_output(EditorReview)


def researcher_node(state: AgentState) -> dict:
    """Agent 1 : Rassemble les faits clés sur le sujet."""
    print(f"🔎 [Researcher] Recherche sur : {state['topic']}...")
    response = llm.invoke([
        SystemMessage(content=RESEARCHER_PROMPT),
        HumanMessage(content=f"Sujet à documenter : {state['topic']}")
    ])
    return {"research_notes": response.content}


def writer_node(state: AgentState) -> dict:
    """Agent 2 : Rédige ou révise la carte éditoriale."""
    attempt = state.get("revision_count", 0) + 1
    print(f"✍️  [Writer] Rédaction (tentative {attempt})...")

    user_content = f"Notes de recherche :\n{state['research_notes']}"
    if state.get("feedback"):
        user_content += f"\n\nFeedback de l'Éditeur à corriger :\n{state['feedback']}"

    draft: ConceptOutput = writer_llm.invoke([
        SystemMessage(content=WRITER_PROMPT),
        HumanMessage(content=user_content)
    ])
    return {
        "draft": draft,
        "revision_count": attempt
    }


def editor_node(state: AgentState) -> dict:
    """Agent 3 : Valide la qualité éditoriale et la concision."""
    print("🧐 [Editor] Vérification qualité...")
    draft_json = state["draft"].model_dump_json(indent=2)

    review: EditorReview = editor_llm.invoke([
        SystemMessage(content=EDITOR_PROMPT),
        HumanMessage(content=f"Carte à évaluer :\n{draft_json}")
    ])
    print(f"   -> Verdict : {'✅ Approuvé' if review.is_approved else '❌ À réviser'} ({review.feedback})")
    return {
        "is_approved": review.is_approved,
        "feedback": review.feedback
    }