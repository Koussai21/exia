import streamlit as st
import requests

# ============================================================
#  CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="EXI·IA — Analyse de cahiers des charges",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
#  CSS — Style sobre et professionnel BTP
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Fond général */
.stApp {
    background-color: #F4F2EE;
}

/* Header principal */
.main-header {
    background-color: #1A1A2E;
    color: #F4F2EE;
    padding: 2rem 2.5rem;
    margin: -1rem -1rem 2rem -1rem;
    border-bottom: 3px solid #E8A020;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.main-header h1 {
    font-size: 1.6rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin: 0;
    color: #F4F2EE;
}

.main-header .subtitle {
    font-size: 0.8rem;
    color: #9A9AB0;
    font-weight: 300;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

.logo-accent {
    color: #E8A020;
}

/* Zone d'upload */
.upload-zone {
    background: #FFFFFF;
    border: 2px dashed #C8C4BC;
    border-radius: 4px;
    padding: 2.5rem;
    text-align: center;
    transition: border-color 0.2s;
}

/* Carte d'exigence */
.exigence-card {
    background: #FFFFFF;
    border-left: 4px solid #1A1A2E;
    border-radius: 0 4px 4px 0;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.exigence-card.doublon {
    border-left-color: #E8A020;
}

.exigence-card.conforme {
    border-left-color: #2D7A4F;
}

.exigence-id {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    color: #9A9AB0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.exigence-nom {
    font-size: 1rem;
    font-weight: 600;
    color: #1A1A2E;
    margin-bottom: 0.5rem;
}

.exigence-contenu {
    font-size: 0.875rem;
    color: #4A4A5A;
    line-height: 1.6;
    padding: 0.75rem;
    background: #F4F2EE;
    border-radius: 3px;
    margin-bottom: 1rem;
}

/* Badge doublon */
.badge-doublon {
    display: inline-block;
    background: #FEF3CD;
    color: #856404;
    font-size: 0.7rem;
    font-weight: 500;
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    border: 1px solid #E8A020;
    margin-bottom: 0.75rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Badge conforme */
.badge-conforme {
    display: inline-block;
    background: #D4EDDA;
    color: #155724;
    font-size: 0.7rem;
    font-weight: 500;
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    border: 1px solid #2D7A4F;
    margin-bottom: 0.75rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Label reformulations */
.reformulations-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #9A9AB0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* Boutons de reformulation */
.stRadio > div {
    gap: 0.5rem;
}

/* Stats bar */
.stats-bar {
    background: #1A1A2E;
    color: #F4F2EE;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    display: flex;
    gap: 2rem;
    margin-bottom: 1.5rem;
    align-items: center;
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.4rem;
    font-weight: 500;
    color: #E8A020;
}

.stat-label {
    font-size: 0.65rem;
    color: #9A9AB0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Séparateur section */
.section-divider {
    height: 1px;
    background: linear-gradient(to right, #1A1A2E, transparent);
    margin: 2rem 0 1.5rem 0;
}

/* Bouton principal */
.stButton > button[kind="primary"] {
    background-color: #1A1A2E !important;
    color: #F4F2EE !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 2rem !important;
    transition: background-color 0.2s !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: #E8A020 !important;
    color: #1A1A2E !important;
}

/* Bouton export */
.stDownloadButton > button {
    background-color: #2D7A4F !important;
    color: white !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
}

/* Masquer éléments Streamlit génériques */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
#  HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <div>
        <h1>EXI<span class="logo-accent">·</span>IA</h1>
        <div class="subtitle">Analyse et reformulation d'exigences — Cahiers des charges</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  SESSION STATE
# ============================================================
if "resultats" not in st.session_state:
    st.session_state["resultats"] = None
if "selections" not in st.session_state:
    st.session_state["selections"] = {}
if "nom_fichier" not in st.session_state:
    st.session_state["nom_fichier"] = ""

# ============================================================
#  ZONE D'UPLOAD
# ============================================================
if st.session_state["resultats"] is None:

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("#### Déposer le cahier des charges")
        fichier = st.file_uploader(
            "Formats acceptés : .docx",
            type=["docx"],
            label_visibility="collapsed"
        )

        if fichier:
            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #C8C4BC; border-radius:4px;
                        padding:0.75rem 1rem; margin:0.5rem 0; display:flex;
                        align-items:center; gap:0.75rem;">
                <span style="font-size:1.2rem">📄</span>
                <div>
                    <div style="font-weight:500; font-size:0.9rem; color:#1A1A2E">{fichier.name}</div>
                    <div style="font-size:0.75rem; color:#9A9AB0">{round(fichier.size / 1024)} Ko</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Lancer l'analyse", type="primary", use_container_width=True):
                with st.spinner("Lecture du document et extraction des exigences en cours..."):
                    try:
                        response = requests.post(
                            "http://localhost:8000/analyser",
                            files={"fichier": (fichier.name, fichier, "application/octet-stream")},
                            timeout=300
                        )

                        if response.status_code == 200:
                            data = response.json()
                            st.session_state["resultats"] = data["taches"]
                            st.session_state["nom_fichier"] = data["nom_fichier"]
                            st.rerun()
                        else:
                            st.error(f"Erreur serveur : {response.text}")

                    except requests.exceptions.ConnectionError:
                        st.error("Impossible de contacter le serveur. Vérifiez que FastAPI tourne sur le port 8000.")
                    except requests.exceptions.Timeout:
                        st.error("Le traitement a pris trop de temps. Essayez avec un document plus court.")

# ============================================================
#  RÉSULTATS
# ============================================================
else:
    taches = st.session_state["resultats"]
    nb_total = len(taches)
    nb_doublons = sum(1 for t in taches if t.get("doublon_probable"))
    nb_conformes = sum(1 for t in taches if t.get("reformulations", {}).get("conforme"))
    nb_selections = len(st.session_state["selections"])

    # --- Barre de stats ---
    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">{nb_total}</div>
            <div class="stat-label">Exigences</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{nb_doublons}</div>
            <div class="stat-label">Doublons détectés</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{nb_conformes}</div>
            <div class="stat-label">Conformes IEEE-830</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{nb_selections}/{nb_total}</div>
            <div class="stat-label">Validées</div>
        </div>
        <div style="margin-left:auto; font-size:0.8rem; color:#9A9AB0">
            📄 {st.session_state["nom_fichier"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Actions ---
    col_reset, col_export = st.columns([1, 3])
    with col_reset:
        if st.button("← Nouvelle analyse"):
            st.session_state["resultats"] = None
            st.session_state["selections"] = {}
            st.session_state["nom_fichier"] = ""
            st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # --- Liste des exigences ---
    for tache in taches:
        tid = tache.get("id", "?")
        nom = tache.get("nom", "Sans titre")
        contenu = tache.get("contenu", "")
        doublon = tache.get("doublon_probable", False)
        refo_data = tache.get("reformulations", {})
        conforme = refo_data.get("conforme", False) if isinstance(refo_data, dict) else False
        reformulations = refo_data.get("reformulations", []) if isinstance(refo_data, dict) else []

        # Classe CSS selon état
        card_class = "exigence-card"
        if doublon:
            card_class += " doublon"
        elif conforme:
            card_class += " conforme"

        st.markdown(f"""
        <div class="{card_class}">
            <div class="exigence-id">{tid}</div>
            <div class="exigence-nom">{nom}</div>
            {"<div class='badge-doublon'>⚠ Doublon probable</div>" if doublon else ""}
            {"<div class='badge-conforme'>✓ Conforme IEEE-830</div>" if conforme else ""}
            <div class="exigence-contenu">{contenu}</div>
        </div>
        """, unsafe_allow_html=True)

        # Reformulations
        if conforme:
            st.markdown(
                "<div style='color:#2D7A4F; font-size:0.85rem; margin:-0.5rem 0 1rem 0'>"
                "Cette exigence respecte déjà les critères de rédaction IEEE-830.</div>",
                unsafe_allow_html=True
            )
            st.session_state["selections"][tid] = contenu

        elif reformulations:
            st.markdown('<div class="reformulations-label">Sélectionner une reformulation</div>', unsafe_allow_html=True)

            options = reformulations + ["Conserver l'original"]
            choix = st.radio(
                label=f"Reformulations {tid}",
                options=options,
                label_visibility="collapsed",
                key=f"radio_{tid}"
            )

            if choix == "Conserver l'original":
                st.session_state["selections"][tid] = contenu
            else:
                st.session_state["selections"][tid] = choix

        st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    # --- Export ---
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if nb_selections == nb_total:
        st.markdown(
            "<div style='color:#2D7A4F; font-weight:500; margin-bottom:1rem'>"
            "✓ Toutes les exigences ont été traitées. Vous pouvez exporter le rapport.</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='color:#9A9AB0; font-size:0.85rem; margin-bottom:1rem'>"
            f"{nb_total - nb_selections} exigence(s) en attente de validation.</div>",
            unsafe_allow_html=True
        )

    # Préparer le contenu texte d'export (Word via exercice 7 à brancher)
    lignes_export = [f"RAPPORT D'ANALYSE — {st.session_state['nom_fichier']}\n"]
    lignes_export.append("=" * 60 + "\n")
    for tache in taches:
        tid = tache.get("id", "?")
        nom = tache.get("nom", "")
        selection = st.session_state["selections"].get(tid, tache.get("contenu", ""))
        lignes_export.append(f"\n{tid} — {nom}")
        lignes_export.append(f"Original  : {tache.get('contenu', '')}")
        lignes_export.append(f"Retenu    : {selection}")
        lignes_export.append("-" * 40)

    export_txt = "\n".join(lignes_export)

    st.download_button(
        label="⬇ Télécharger le rapport (.txt)",
        data=export_txt,
        file_name=f"rapport_{st.session_state['nom_fichier'].replace('.docx', '')}.txt",
        mime="text/plain",
        use_container_width=False
    )
    st.caption("Export Word (.docx) — disponible prochainement")