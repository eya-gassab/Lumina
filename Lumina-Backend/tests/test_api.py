import json
from fastapi.testclient import TestClient

from main import app
from api.storage import save_daily_concepts, load_daily_concepts

client = TestClient(app)


def test_health_check():
    """Vérifie que l'endpoint /health répond 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_save_and_load_daily_concepts(tmp_path):
    """Test unitaire : sauvegarde et rechargement avec assignation d'IDs stables."""
    test_file = tmp_path / "daily_concepts.json"
    sample = [
        {
            "title": "Principe de Pareto",
            "category": "Productivité",
            "tldr": "80% des effets proviennent de 20% des causes.",
            "explanation": "Observé par Vilfredo Pareto, ce principe aide à prioriser l'essentiel.",
            "practical_application": "Identifie les 2 tâches les plus impactantes de ta journée.",
        }
    ]

    saved = save_daily_concepts(sample, file_path=test_file)
    assert saved.count == 1
    assert saved.concepts[0].id == 1

    loaded = load_daily_concepts(file_path=test_file)
    assert loaded.count == 1
    assert loaded.concepts[0].title == "Principe de Pareto"
    assert loaded.concepts[0].practical_application == sample[0]["practical_application"]


def test_get_daily_concepts_success():
    """Vérifie le contrat JSON complet retourné par GET /api/daily."""
    response = client.get("/api/daily")
    assert response.status_code == 200

    body = response.json()
    assert "date" in body
    assert "count" in body
    assert "concepts" in body
    assert body["count"] == len(body["concepts"])
    assert body["count"] >= 1

    first = body["concepts"][0]
    expected_keys = {"id", "title", "category", "tldr", "explanation", "practical_application"}
    assert expected_keys.issubset(first.keys())
    assert isinstance(first["id"], int)


def test_get_daily_concepts_not_found(monkeypatch):
    """Vérifie que l'API renvoie 404 si le fichier de concepts est absent."""
    def mock_missing_file():
        raise FileNotFoundError("Fichier absent")

    monkeypatch.setattr("api.routes.load_daily_concepts", mock_missing_file)
    response = client.get("/api/daily")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_daily_concepts_corrupted_json(monkeypatch):
    """Vérifie que l'API renvoie 500 si le fichier JSON est corrompu."""
    def mock_corrupted_file():
        raise json.JSONDecodeError("Expecting value", "", 0)

    monkeypatch.setattr("api.routes.load_daily_concepts", mock_corrupted_file)
    response = client.get("/api/daily")
    assert response.status_code == 500
    assert "detail" in response.json()
