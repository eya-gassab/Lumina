import json
from datetime import date
from pathlib import Path
from api.schemas import ConceptResponse, DailyConceptsResponse

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "daily_concepts.json"


def save_daily_concepts(
    approved_concepts: list[dict],
    file_path: Path = DEFAULT_DATA_PATH,
) -> DailyConceptsResponse:
    """Assigne des IDs stables et sauvegarde uniquement les concepts approuvés en JSON."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    formatted = [
        ConceptResponse(id=index, **concept)
        for index, concept in enumerate(approved_concepts, start=1)
    ]

    payload = DailyConceptsResponse(
        date=date.today().isoformat(),
        count=len(formatted),
        concepts=formatted,
    )

    file_path.write_text(
        payload.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return payload


def load_daily_concepts(file_path: Path = DEFAULT_DATA_PATH) -> DailyConceptsResponse:
    """Charge et valide les concepts approuvés depuis le fichier JSON local."""
    if not file_path.exists():
        raise FileNotFoundError(f"Aucun fichier de concepts trouvé à : {file_path}")

    raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    return DailyConceptsResponse.model_validate(raw_data)