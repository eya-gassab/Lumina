from typing import Optional, TypedDict
from pydantic import BaseModel, Field


class ConceptCard(BaseModel):
    """Structure finale d'une carte envoyée à l'application Android."""
    title: str = Field(..., description="Nom du modèle mental ou biais cognitif")
    category: str = Field(..., description="Catégorie (ex: Modèle Mental, Biais Cognitif)")
    tldr: str = Field(..., description="Résumé ultra-concis (2-3 phrases max)")
    practical_application: str = Field(..., description="Cas d'usage concret au quotidien")


class LuminaState(TypedDict, total=False):
    """
    État partagé qui circule entre les nœuds du graphe LangGraph.
    total=False permet à chaque nœud de ne retourner que les clés qu'il modifie.
    """
    topic: str                         # Sujet en entrée (ex: "Rasoir d'Ockham")
    research_notes: str                # Faits sourcés extraits par le Researcher
    draft: Optional[ConceptCard]       # Brouillon structuré généré par le Writer
    is_approved: bool                  # Verdict qualité de l'Editor
    editor_feedback: str               # Consignes de correction si rejeté
    revision_count: int                # Garde-fou pour éviter toute boucle infinie