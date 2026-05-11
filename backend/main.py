from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from docling.document_converter import DocumentConverter 
import anthropic
import tempfile
import os
import json
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

app = FastAPI(
    title="Cahier des charges IA",
    description="API d'extraction et reformulation de tâches",
    version="0.1.0"
)

derniers_resultats = []

app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],       # en prod, mettre l'URL exacte
       allow_methods=["*"],
       allow_headers=["*"],
   )

#Healthcheck 
@app.get("/")
def health_check():
    return {"status": "ok", "message": "API opérationnelle"}


#Parsing docling
def doc_parser(file):
    try:
        converter = DocumentConverter()
        result = converter.convert(file)
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

#Extraction tâches
def extraire_taches(texte: str) -> list:
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
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
        messages=[{
            "role": "user",
            "content": texte
        }]
    )

    print("=== REPONSE BRUTE CLAUDE ===")
    print(message.content[0].text)
    print("=== FIN REPONSE ===")

    try:
        texte_brut = message.content[0].text
    
        # Nettoyer les backticks Markdown si Claude en ajoute
        texte_propre = texte_brut.strip()
        if texte_propre.startswith("```"):
            texte_propre = texte_propre.split("```")[1] 
            if texte_propre.startswith("json"):
                texte_propre = texte_propre[4:]          
        texte_propre = texte_propre.strip().rstrip("```")
    
        donnees = json.loads(texte_propre)
        return donnees["tasks"]
    except Exception as e:
        print(f"ERREUR JSON : {e}")  # DEBUG
        return []

#reformulateur
def reformuler_tache(tache: dict) -> dict:
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        system=(
            "Tu es un expert en rédaction d'exigences techniques pour des cahiers des charges BTP. "
            "Une exigence de qualité doit respecter 4 critères selon la norme IEEE-830 1998 : "
            "1. Claire et non ambiguë : comprise de la même façon par toutes les parties prenantes. "
            "Éviter les termes vagues comme 'rapide', 'correct', 'bonne qualité'. "
            "2. Mesurable / vérifiable : on doit pouvoir tester objectivement si elle est respectée. "
            "3. Réalisable / faisable : techniquement et économiquement possible. "
            "4. Nécessaire / pertinente : répond à un besoin réel avec une justification fonctionnelle. "
            "Tu t'adresses à des ingénieurs de chantier. "
            "Pour l'exigence reçue, vérifie si elle respecte ces critères. "
            "Si elle est déjà conforme, indique-le. "
            "Sinon, propose 3 reformulations améliorées. "
            "Retourne UNIQUEMENT un JSON valide sans texte autour : "
            '{"id": "...", "conforme": false, "reformulations": ["...", "...", "..."]}'
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Voici l'exigence à analyser :\n"
                f"ID : {tache['id']}\n"
                f"Nom : {tache['nom']}\n"
                f"Contenu : {tache['contenu']}"
            )
        }]
    )

    try:
        return json.loads(nettoyer_json(message.content[0].text))
    except Exception:
        return {
            "id": tache.get("id", "?"),
            "conforme": None,
            "reformulations": ["Erreur de reformulation"]
        }

@app.post("/analyser")
async def analyser(fichier: UploadFile = File(...)):

    global derniers_resultats
    
    # Vérification docx
    if not fichier.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Le document doit être un fichier .docx")

    contenu = await fichier.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(contenu)
        chemin_tmp = tmp.name

    texte = doc_parser(chemin_tmp)

    print("=== APERCU DOCLING ===")
    print(texte[:2000])
    print("=== FIN APERCU ===")
    os.unlink(chemin_tmp)

    taches = extraire_taches(texte)

    for tache in taches:
        tache["reformulations"] = reformuler_tache(tache)

    derniers_resultats = taches

    return { 
    "nom_fichier": fichier.filename,
    "nb_taches": len(taches),
    "taches": taches
    }

@app.get("/taches/{id}")
def get_tache(id: str):
    for tache in derniers_resultats:
        if tache["id"] == id:
            return tache
    raise HTTPException(status_code=404, detail=f"Tâche {id} introuvable")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))