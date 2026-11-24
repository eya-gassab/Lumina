from typing import TypedDict, Optional
from pydantic import BaseModel, Field


class ConceptOutput(BaseModel):
    """Structure finale d'une carte Lumina, alignée sur le client Android."""
    title: str = Field(description="Nom du modèle mental ou biais cognitif (court et percutant).")
    category: str = Field(description="Catégorie courte (ex: Productivité, Prise de décision, Biais Cognitif).")
    tldr: str = Field(description="Résumé ultra-clair en 1 à 2 phrases maximum.")
    explanation: str = Field(description="Explication fluide et académique (3 à 4 phrases max).")
    practical_application: str = Field(description="Action concrète applicable dès aujourd'hui (2 phrases max).")


class EditorReview(BaseModel):
    """Verdict structuré de l'agent Éditeur."""
    is_approved: bool = Field(description="True si le contenu respecte le ton calme, académique et concis.")
    feedback: str = Field(description="Si rejeté, instructions précises d'amélioration. Sinon, 'Approuvé'.")


class AgentState(TypedDict):
    """État partagé par tous les nœuds du graphe LangGraph."""
    topic: str
    research_notes: str
    draft: Optional[ConceptOutput]
    is_approved: bool
    feedback: str
    revision_count: int