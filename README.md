# EXI-IA

Outil d'aide à la rédaction de cahiers des charges assisté par intelligence artificielle.
EXI-IA parse des documents Word techniques, en extrait automatiquement les exigences,
évalue leur conformité à la norme IEEE-830 et propose des reformulations améliorées
présentées côte à côte pour validation par l'ingénieur.

---

## Contexte

Dans les projets BTP et ferroviaires, la rédaction des exigences est une tâche critique
et chronophage. Une exigence mal formulée — trop vague, non vérifiable, ou ambiguë —
peut générer des litiges, des surcoûts ou des non-conformités en phase de réalisation.

EXI-IA assiste les ingénieurs en automatisant l'extraction des exigences depuis les
cahiers des charges et en proposant des reformulations conformes aux bonnes pratiques
de rédaction technique (norme IEEE-830, 1998).

---

## Fonctionnalités

- Upload d'un fichier Word (.docx) via une interface web dark mode
- Parsing du document avec extraction du contenu textuel et des tableaux
- Identification automatique des exigences quelle que soit leur mise en forme
  (tableau, liste, texte linéaire, numérotation)
- Détection des doublons probables entre exigences
- Analyse de conformité de chaque exigence selon la norme IEEE-830
- Génération de 3 reformulations par exigence non conforme
- Interface de validation avec les 3 reformulations affichées côte à côte
- Sélection de la reformulation retenue par simple clic
- Option de conservation de l'exigence originale
- Compteur de validation en temps réel (X/N exigences validées)
- Export du rapport au format texte
- API REST documentée via Swagger UI

---

## Stack technique

**Backend**

- Python 3.11
- FastAPI — framework API REST
- Uvicorn — serveur ASGI
- Docling (IBM Research) — parsing de documents Word, extraction de tableaux et schémas
- Anthropic Claude Sonnet 4 — extraction des exigences
- Anthropic Claude Haiku 4.5 — reformulation (3x moins cher, suffisant pour cette tâche)
- python-docx — manipulation de fichiers Word
- python-multipart — gestion des uploads de fichiers

**Frontend**

- Streamlit — interface utilisateur web dark mode
- Requests — appels HTTP vers le backend

**Déploiement**

- Backend : Railway (branch main → production)
- Frontend : Streamlit Cloud
- Branches : main (prod), dev (développement)

---

## Architecture

```
EXI_IA/
├── backend/
│   └── main.py          API FastAPI (parsing, extraction, reformulation)
├── frontend/
│   └── app.py           Interface Streamlit dark mode
├── .streamlit/
│   └── config.toml      Configuration thème Streamlit
├── .env                 Variables d'environnement (non versionné)
├── requirements.txt     Dépendances Python
├── Procfile             Commande de démarrage Railway
└── README.md
```

Le frontend appelle le backend via HTTP. Cette séparation permet de remplacer
l'interface Streamlit par n'importe quel autre client (React, outil interne,
script batch) sans modifier la logique métier.

---

## Endpoints API

| Methode | Route | Description |
|---------|-------|-------------|
| GET | / | Health check |
| POST | /analyser | Upload et traitement complet d'un fichier .docx |
| GET | /taches/{id} | Recuperation d'une exigence par son identifiant |

La documentation interactive est disponible sur `/docs` une fois le serveur démarré.

---

## Installation locale

Prerequis : Python 3.11+, uv

```bash
git clone https://github.com/Koussai21/exia.git
cd exia
uv venv
uv sync
```

Créer un fichier `.env` à la racine :

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

---

## Lancement local

```bash
# Terminal 1 — Backend
uvicorn backend.main:app --reload

# Terminal 2 — Frontend
streamlit run frontend/app.py
```

Backend : `http://localhost:8000`
Frontend : `http://localhost:8501`
Swagger : `http://localhost:8000/docs`

---

## Déploiement

**Backend — Railway**

```
Root Directory  : (vide)
Start Command   : uvicorn backend.main:app --host 0.0.0.0 --port $PORT
Branch          : main (prod), dev (développement)
Variables       : ANTHROPIC_API_KEY
```

**Frontend — Streamlit Cloud**

```
Repository  : Koussai21/exia
Branch      : main
Main file   : frontend/app.py
```

---

## Workflow de développement

```bash
# Travailler sur la branche dev
git checkout dev

# Développer, tester
git add .
git commit -m "feat: description"
git push origin dev

# Merger en prod quand validé
git checkout main
git merge dev
git push origin main
```

---

## Modèles IA

| Tache | Modele | Raison |
|-------|--------|--------|
| Extraction des exigences | claude-sonnet-4-20250514 | Fenetre 1M tokens, meilleure comprehension documentaire |
| Reformulation | claude-haiku-4-5-20251001 | 3x moins cher, largement suffisant pour reformuler |

---

## Conformité IEEE-830

Chaque exigence est évaluée selon 4 critères :

1. Claire et non ambigue — comprise de la même façon par toutes les parties prenantes
2. Mesurable et vérifiable — on peut tester objectivement si elle est respectée
3. Réalisable — techniquement et économiquement possible
4. Nécessaire — répond à un besoin réel avec une justification fonctionnelle

---

## Estimation des coûts API

| Volume | Modeles | Cout estimé |
|--------|---------|-------------|
| 20 exigences | Sonnet + Haiku | ~0.04 USD |
| 300 exigences (300 pages) | Sonnet + Haiku | ~1.10 USD |

---

## Roadmap

- Export du rapport au format Word (.docx)
- Gestion des documents longs par découpage sémantique par sections
- Authentification utilisateur
- Historique des analyses en base de données
- Branche open source avec Ollama (modeles locaux, zero cout API, données privées)
- Dockerisation pour déploiement en entreprise
- Tests automatisés

---

## Licence

Projet privé — tous droits réservés.
