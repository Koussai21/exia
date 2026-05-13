import json
import anthropic
from typing import List, Dict
from .token_optimizer import TokenOptimizer
from .models import ReformulationResult


def nettoyer_json(texte_brut: str) -> str:
    texte = texte_brut.strip()
    if texte.startswith("```"):
        texte = texte.split("```")[1]
        if texte.startswith("json"):
            texte = texte[4:]
    return texte.strip().rstrip("```").strip()


def reformuler_batch(requirements: List[dict], batch_size: int = 10, model: str = "claude-haiku-4-5-20251001") -> Dict[str, ReformulationResult]:
    client = anthropic.Anthropic()
    results = {}

    total_input_tokens = 0
    total_output_tokens = 0

    for i in range(0, len(requirements), batch_size):
        batch = requirements[i : i + batch_size]

        batch_text = "\n---\n".join(
            f"ID: {req['id']}\nNom: {req['nom']}\nContenu: {req['contenu']}\nComplexité: {req.get('complexity_score', 1)}/5"
            for req in batch
        )

        message = client.messages.create(
            model=model,
            max_tokens=3000,
            system=(
                "Tu es un expert en rédaction d'exigences techniques pour des cahiers des charges BTP. "
                "Une exigence de qualité doit respecter 4 critères selon la norme IEEE-830 1998 : "
                "1. Claire et non ambiguë : comprise de la même façon par toutes les parties prenantes. "
                "Éviter les termes vagues comme 'rapide', 'correct', 'bonne qualité'. "
                "2. Mesurable / vérifiable : on doit pouvoir tester objectivement si elle est respectée. "
                "3. Réalisable / faisable : techniquement et économiquement possible. "
                "4. Nécessaire / pertinente : répond à un besoin réel avec une justification fonctionnelle. "
                "Tu t'adresses à des ingénieurs de chantier. "
                "Pour chaque exigence, vérifie si elle respecte ces critères. "
                "Si elle est déjà conforme, indique-le. "
                "Sinon, propose 3 reformulations améliorées. "
                "Retourne UNIQUEMENT un JSON valide sans texte autour avec une clé par ID : "
                '{"EX-001": {"id": "EX-001", "conforme": false, "reformulations": ["...", "...", "..."]}, "EX-002": {...}}'
            ),
            messages=[{"role": "user", "content": f"Voici les exigences à analyser :\n\n{batch_text}"}]
        )

        total_input_tokens += message.usage.input_tokens
        total_output_tokens += message.usage.output_tokens

        try:
            texte_brut = message.content[0].text
            texte_propre = nettoyer_json(texte_brut)
            batch_results = json.loads(texte_propre)

            for req_id, refo_data in batch_results.items():
                results[req_id] = ReformulationResult(
                    id=refo_data.get("id", req_id),
                    conforme=refo_data.get("conforme"),
                    reformulations=refo_data.get("reformulations", [])
                )
        except Exception as e:
            print(f"ERREUR JSON reformulation batch : {e}")
            for req in batch:
                results[req["id"]] = ReformulationResult(
                    id=req["id"],
                    conforme=None,
                    reformulations=["Erreur lors de la reformulation"]
                )

    return results, {"input_tokens": total_input_tokens, "output_tokens": total_output_tokens}


def reformuler_selection(requirements: List[dict], requirement_ids: List[str] = None, model: str = "claude-haiku-4-5-20251001") -> tuple:
    to_reformulate = requirements
    if requirement_ids:
        to_reformulate = [r for r in requirements if r["id"] in requirement_ids]

    if not to_reformulate:
        return {}, {"input_tokens": 0, "output_tokens": 0}

    return reformuler_batch(to_reformulate, batch_size=10, model=model)
