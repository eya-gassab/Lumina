import json
from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from api.schemas import DailyConceptsResponse
from api.storage import load_daily_concepts

router = APIRouter(prefix="/api", tags=["Daily Concepts"])


@router.get(
    "/daily",
    response_model=DailyConceptsResponse,
    status_code=status.HTTP_200_OK,
    summary="Récupérer les concepts approuvés du jour",
    description="Retourne les modèles mentaux validés par l'agent Editor, prêts pour la synchronisation Android.",
    responses={
        404: {"description": "Aucun fichier de concepts quotidiens disponible."},
        500: {"description": "Fichier de concepts corrompu ou non conforme au schéma."},
    },
)
def get_daily_concepts() -> DailyConceptsResponse:
    """Expose les concepts approuvés sans déclencher le pipeline IA."""
    try:
        return load_daily_concepts()
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun concept quotidien disponible pour le moment.",
        )
    except (json.JSONDecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Les données quotidiennes sont corrompues ou invalides.",
        )