import json
import anthropic
from typing import List
from .token_optimizer import TokenOptimizer


def doc_parser(file_path: str) -> str:
    from docling.document_converter import DocumentConverter

    try:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
    except Exception as e:
        raise Exception(f"Erreur lecture document : {e}")


def nettoyer_json(texte_brut: str) -> str:
    texte = texte_brut.strip()
    if texte.startswith("```"):
        texte = texte.split("```")[1]
        if texte.startswith("json"):
            texte = texte[4:]
    return texte.strip().rstrip("```").strip()


def extraire_exigences(texte: str, max_tokens: int = 3000) -> List[dict]:
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=(
            "Tu es un expert en analyse de cahiers des charges techniques. "
            "Tu sais reconnaître une exigence quelle que soit sa mise en forme : "
            "tableau, liste à puces, texte linéaire, numérotation, etc. "
            "Une exigence est une tâche concrète à réaliser sur un chantier. "
            "Elle peut avoir un identifiant explicite (EX-001, REQ-01, EXI-01...) "
            "ou pas d'identifiant du tout — dans ce cas génère un id de la forme EX-001, EX-002... "
            "Elle a toujours un contenu décrivant ce qui doit être fait. "
            "Elle peut avoir un nom ou titre, ou pas — dans ce cas résume-le en 5 mots. "
            "RÈGLE IMPORTANTE : n'extrait que les exigences qui ont un contenu réel. "
            "Si une exigence est juste mentionnée par son nom sans détail, ignore-la — c'est un faux positif. "
            "Si deux exigences décrivent la même chose avec des mots différents, "
            "extrait-les toutes les deux mais ajoute un champ 'doublon_probable': true sur chacune. "
            "Retourne UNIQUEMENT un JSON valide, sans texte autour : "
            '{\"tasks\": [{'
            '\"id\": \"EX-001\", '
            '\"nom\": \"...\", '
            '\"contenu\": \"...\", '
            '\"doublon_probable\": false'
            '}]}'
        ),
        messages=[{"role": "user", "content": texte}]
    )

    try:
        texte_brut = message.content[0].text
        texte_propre = nettoyer_json(texte_brut)
        donnees = json.loads(texte_propre)
        tasks = donnees.get("tasks", [])

        for task in tasks:
            task["complexity_score"] = TokenOptimizer.calculate_complexity(task)

        return tasks
    except Exception as e:
        print(f"ERREUR JSON extraction : {e}")
        return []
