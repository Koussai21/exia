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
#  CSS — Dark mode industriel / BTP
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Fond général dark */
.stApp {
    background-color: #0F1117;
    color: #E8E6E0;
}

/* Header */
.main-header {
    background-color: #0F1117;
    border-bottom: 2px solid #E8A020;
    padding: 1.5rem 2.5rem;
    margin: -1rem -1rem 2rem -1rem;
}

.main-header h1 {
    font-size: 1.8rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    margin: 0;
    color: #E8E6E0;
    text-transform: uppercase;
}

.main-header .subtitle {
    font-size: 0.75rem;
    color: #6B6B7A;
    font-weight: 300;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

.logo-accent { color: #E8A020; }

/* Paragraphes et textes généraux */
p, span, div, label {
    color: #E8E6E0;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #1C1F2E;
    border: 1px dashed #3A3D4E;
    border-radius: 6px;
    padding: 1rem;
}

[data-testid="stFileUploader"] label {
    color: #A0A0B0 !important;
}

/* Carte exigence */
.exigence-card {
    background: #1C1F2E;
    border-left: 4px solid #3A3D4E;
    border-radius: 0 6px 6px 0;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.exigence-card.doublon { border-left-color: #E8A020; }
.exigence-card.conforme { border-left-color: #3DAA6B; }

.exigence-id {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    color: #6B6B7A;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.exigence-nom {
    font-size: 1rem;
    font-weight: 600;
    color: #E8E6E0;
    margin-bottom: 0.6rem;
}

.exigence-contenu {
    font-size: 0.875rem;
    color: #B0AFA8;
    line-height: 1.7;
    padding: 0.75rem 1rem;
    background: #0F1117;
    border-radius: 4px;
    border: 1px solid #2A2D3E;
    margin-bottom: 0.75rem;
}

/* Badges */
.badge-doublon {
    display: inline-block;
    background: rgba(232,160,32,0.15);
    color: #E8A020;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.2rem 0.7rem;
    border-radius: 2px;
    border: 1px solid #E8A020;
    margin-bottom: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.badge-conforme {
    display: inline-block;
    background: rgba(61,170,107,0.15);
    color: #3DAA6B;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.2rem 0.7rem;
    border-radius: 2px;
    border: 1px solid #3DAA6B;
    margin-bottom: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Stats bar */
.stats-bar {
    background: #1C1F2E;
    border: 1px solid #2A2D3E;
    color: #E8E6E0;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    display: flex;
    gap: 2.5rem;
    margin-bottom: 1.5rem;
    align-items: center;
}

.stat-number {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    color: #E8A020;
    display: block;
}

.stat-label {
    font-size: 0.62rem;
    color: #6B6B7A;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* Séparateur */
.section-divider {
    height: 1px;
    background: linear-gradient(to right, #E8A020, transparent);
    margin: 2rem 0 1.5rem 0;
    opacity: 0.4;
}

/* Label reformulations */
.reformulations-label {
    font-size: 0.65rem;
    font-weight: 600;
    color: #6B6B7A;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* Radio buttons */
[data-testid="stRadio"] label {
    color: #B0AFA8 !important;
    font-size: 0.875rem !important;
}

[data-testid="stRadio"] > div {
    background: #0F1117;
    border: 1px solid #2A2D3E;
    border-radius: 4px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.25rem;
}

/* Bouton principal */
.stButton > button {
    background-color: #E8A020 !important;
    color: #0F1117 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
}

.stButton > button:hover {
    background-color: #F5B53A !important;
}

/* Bouton secondaire (← Nouvelle analyse) */
.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #6B6B7A !important;
    border: 1px solid #3A3D4E !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: #E8A020 !important;
    color: #E8A020 !important;
}

/* Download button */
.stDownloadButton > button {
    background-color: #3DAA6B !important;
    color: #0F1117 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
}

/* Spinner */
[data-testid="stSpinner"] {
    color: #E8A020 !important;
}

/* Titres */
h1, h2, h3, h4 {
    color: #E8E6E0 !important;
}

/* Success / Error messages */
[data-testid="stAlert"] {
    background-color: #1C1F2E !important;
    border-color: #3A3D4E !important;
    color: #E8E6E0 !important;
}

/* Masquer éléments Streamlit */
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
            <div style="background:#1C1F2E; border:1px solid #2A2D3E; border-radius:6px;
                        padding:0.75rem 1rem; margin:0.5rem 0; display:flex;
                        align-items:center; gap:0.75rem;">
                <span style="font-size:1.2rem">📄</span>
                <div>
                    <div style="font-weight:500; font-size:0.9rem; color:#E8E6E0">{fichier.name}</div>
                    <div style="font-size:0.75rem; color:#6B6B7A">{round(fichier.size / 1024)} Ko</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Lancer l'analyse", use_container_width=True):
                with st.spinner("Lecture du document et extraction des exigences..."):
                    try:
                        response = requests.post(
                            "https://exia-production-e983.up.railway.app/analyser",
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
                        st.error("Impossible de contacter le serveur.")
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
        <div>
            <span class="stat-number">{nb_total}</span>
            <span class="stat-label">Exigences</span>
        </div>
        <div>
            <span class="stat-number">{nb_doublons}</span>
            <span class="stat-label">Doublons</span>
        </div>
        <div>
            <span class="stat-number">{nb_conformes}</span>
            <span class="stat-label">Conformes IEEE-830</span>
        </div>
        <div>
            <span class="stat-number">{nb_selections}/{nb_total}</span>
            <span class="stat-label">Validées</span>
        </div>
        <div style="margin-left:auto; font-size:0.75rem; color:#6B6B7A; font-family:'IBM Plex Mono',monospace;">
            {st.session_state["nom_fichier"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Actions ---
    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("← Nouvelle analyse", type="secondary"):
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

        if conforme:
            st.markdown(
                "<div style='color:#3DAA6B; font-size:0.85rem; margin:-0.5rem 0 1.5rem 0'>"
                "Cette exigence respecte déjà les critères IEEE-830.</div>",
                unsafe_allow_html=True
            )
            st.session_state["selections"][tid] = contenu

        elif reformulations:
            st.markdown('<div class="reformulations-label">Sélectionner une reformulation</div>',
                        unsafe_allow_html=True)
            options = reformulations + ["Conserver l'original"]
            choix = st.radio(
                label=f"Reformulations {tid}",
                options=options,
                label_visibility="collapsed",
                key=f"radio_{tid}"
            )
            st.session_state["selections"][tid] = contenu if choix == "Conserver l'original" else choix

        st.markdown("<div style='margin-bottom:0.25rem'></div>", unsafe_allow_html=True)

    # --- Export ---
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if nb_selections == nb_total:
        st.markdown(
            "<div style='color:#3DAA6B; font-weight:500; margin-bottom:1rem; font-size:0.875rem'>"
            "✓ Toutes les exigences ont été traitées.</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='color:#6B6B7A; font-size:0.825rem; margin-bottom:1rem'>"
            f"{nb_total - nb_selections} exigence(s) en attente de validation.</div>",
            unsafe_allow_html=True
        )

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
        label="Télécharger le rapport (.txt)",
        data=export_txt,
        file_name=f"rapport_{st.session_state['nom_fichier'].replace('.docx', '')}.txt",
        mime="text/plain",
        use_container_width=False
    )
    st.caption("Export Word (.docx) — disponible prochainement")