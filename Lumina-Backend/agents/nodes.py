from agents.state import ConceptCard, LuminaState


def researcher_node(state: LuminaState) -> dict:
    """
    Agent 1 (Researcher) : rassemble les faits clés et la définition sourcée du sujet.
    """
    topic = state["topic"]

    # TODO (Mardi) : remplacer par l'appel LLM + prompt de recherche sourcée
    notes = (
        f"Origine et principe fondamental de '{topic}'. "
        "Utile pour la prise de décision et la clarté mentale."
    )

    return {"research_notes": notes}


def writer_node(state: LuminaState) -> dict:
    """
    Agent 2 (Writer) : transforme les notes de recherche en une carte éditoriale calme et concise.
    Prend en compte le feedback de l'Editor lors d'une seconde passe.
    """
    topic = state["topic"]
    feedback = state.get("editor_feedback", "")

    # TODO (Mardi) : remplacer par l'appel LLM en sortie structurée (ConceptCard)
    tldr_text = (
        f"{topic} permet de simplifier une décision complexe en allant à l'essentiel."
        if not feedback
        else f"{topic} : version affinée suite au retour éditorial ({feedback})."
    )

    card = ConceptCard(
        title=topic,
        category="Modèle Mental",
        tldr=tldr_text,
        practical_application=f"Appliquez '{topic}' avant de lancer une nouvelle tâche cette semaine.",
    )

    return {"draft": card}


def editor_node(state: LuminaState) -> dict:
    """
    Agent 3 (Editor) : vérifie la qualité, la concision et le ton académique/calme.
    Incrémente le compteur de révisions à chaque passage.
    """
    draft = state.get("draft")
    revisions = state.get("revision_count", 0) + 1

    # TODO (Mardi) : remplacer cette validation basique par le prompt critique de l'Editor
    if draft and len(draft.tldr) >= 20 and draft.practical_application:
        return {
            "is_approved": True,
            "editor_feedback": "",
            "revision_count": revisions,
        }

    return {
        "is_approved": False,
        "editor_feedback": "Le TL;DR est trop court ou l'application pratique manque.",
        "revision_count": revisions,
    }