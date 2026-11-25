from pydantic import BaseModel, Field
from agents.state import ConceptOutput


class ConceptResponse(ConceptOutput):
    """Contrat JSON d'une carte Lumina exposée à Android (hérite de ConceptOutput)."""
    id: int = Field(..., ge=1, description="Identifiant entier stable utilisé comme clé primaire Room.")


class DailyConceptsResponse(BaseModel):
    """Enveloppe de réponse pour GET /api/daily."""
    date: str = Field(..., description="Date de génération au format ISO (YYYY-MM-DD).")
    count: int = Field(..., ge=0, description="Nombre de concepts approuvés retournés.")
    concepts: list[ConceptResponse] = Field(default_factory=list, description="Liste des concepts approuvés.")