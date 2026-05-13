import streamlit as st
import requests
import html
from datetime import datetime

API_URL = "https://exia-production-e983.up.railway.app"

st.set_page_config(
    page_title="EXI·IA — Analyse de cahiers des charges",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp {
    background-color: #0F1117;
    color: #E8E6E0;
}

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

.exigence-header {
    background: #1C1F2E;
    border-left: 4px solid #3A3D4E;
    border-radius: 6px 6px 0 0;
    padding: 1rem 1.5rem 0.75rem 1.5rem;
    margin-bottom: 0;
}

.exigence-header.doublon { border-left-color: #E8A020; }
.exigence-header.conforme { border-left-color: #3DAA6B; }

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
    margin-bottom: 0.4rem;
}

.badge-doublon {
    display: inline-block;
    background: rgba(232,160,32,0.15);
    color: #E8A020;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.2rem 0.7rem;
    border-radius: 2px;
    border: 1px solid #E8A020;
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
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.refo-card {
    background: #1C1F2E;
    border: 1px solid #2A2D3E;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    height: 100%;
    min-height: 120px;
    transition: border-color 0.2s;
}

.refo-card:hover {
    border-color: #E8A020;
}

.refo-card.selected {
    border-color: #E8A020;
    background: rgba(232,160,32,0.08);
}

.refo-number {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    color: #E8A020;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.refo-text {
    font-size: 0.85rem;
    color: #B0AFA8;
    line-height: 1.6;
}

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

.section-divider {
    height: 1px;
    background: linear-gradient(to right, #E8A020, transparent);
    margin: 2rem 0 1.5rem 0;
    opacity: 0.4;
}

[data-testid="stFileUploader"] {
    background-color: #1C1F2E;
    border: 1px dashed #3A3D4E;
    border-radius: 6px;
    padding: 1rem;
}

[data-testid="stAlert"] {
    background-color: #1A1D2C !important;
    border: 1px solid #2A2D3E !important;
    border-top: none !important;
    border-radius: 0 0 6px 6px !important;
    color: #B0AFA8 !important;
    margin-top: 0 !important;
}

[data-testid="stAlert"] p {
    color: #B0AFA8 !important;
    font-size: 0.875rem !important;
    line-height: 1.7 !important;
}

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

.stButton > button:hover { background-color: #F5B53A !important; }

.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #6B6B7A !important;
    border: 1px solid #3A3D4E !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: #E8A020 !important;
    color: #E8A020 !important;
}

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

h1, h2, h3, h4 { color: #E8E6E0 !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.step-indicator {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    align-items: center;
}

.step-number {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    font-weight: 600;
    color: #0F1117;
    background: #E8A020;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.step-text {
    font-size: 0.9rem;
    color: #E8E6E0;
    font-weight: 500;
}

.step-divider {
    flex: 1;
    height: 1px;
    background: #3A3D4E;
    margin: 0 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div>
        <h1>EXI<span class="logo-accent">·</span>IA</h1>
        <div class="subtitle">Analyse et reformulation d'exigences — Cahiers des charges</div>
    </div>
</div>
""", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "requirements" not in st.session_state:
    st.session_state.requirements = None
if "reformulations" not in st.session_state:
    st.session_state.reformulations = None
if "selections" not in st.session_state:
    st.session_state.selections = {}
if "filename" not in st.session_state:
    st.session_state.filename = ""
if "selected_for_reformulation" not in st.session_state:
    st.session_state.selected_for_reformulation = None

def reset_analysis():
    st.session_state.step = 1
    st.session_state.session_id = None
    st.session_state.requirements = None
    st.session_state.reformulations = None
    st.session_state.selections = {}
    st.session_state.filename = ""
    st.session_state.selected_for_reformulation = None
    st.rerun()

if st.session_state.step == 1:
    st.markdown("## Étape 1: Extraction des exigences")

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
                    <div style="font-weight:500; font-size:0.9rem; color:#E8E6E0">{html.escape(fichier.name)}</div>
                    <div style="font-size:0.75rem; color:#6B6B7A">{round(fichier.size / 1024)} Ko</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Extraire les exigences", use_container_width=True):
                with st.spinner("Extraction des exigences en cours..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/extract",
                            files={"fichier": (fichier.name, fichier, "application/octet-stream")},
                            timeout=300
                        )

                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.session_id = data["session_id"]
                            st.session_state.requirements = data["requirements"]
                            st.session_state.filename = data.get("filename", fichier.name)
                            st.session_state.step = 2
                            st.rerun()
                        else:
                            st.error(f"Erreur serveur : {response.text}")

                    except requests.exceptions.Timeout:
                        st.error("Le traitement a pris trop de temps. Essayez avec un document plus court.")
                    except requests.exceptions.ConnectionError:
                        st.error("Impossible de contacter le serveur.")

elif st.session_state.step == 2:
    st.markdown("## Étape 2: Vérification des exigences extraites")

    if st.button("← Nouvelle analyse", type="secondary"):
        reset_analysis()

    reqs = st.session_state.requirements or []
    nb_total = len(reqs)
    nb_doublons = sum(1 for r in reqs if r.get("doublon_probable"))

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
        <div style="margin-left:auto; font-size:0.75rem; color:#6B6B7A; font-family:'IBM Plex Mono',monospace;">
            {html.escape(st.session_state.filename)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    for req in reqs:
        req_id = req.get("id", "?")
        nom = req.get("nom", "Sans titre")
        contenu = req.get("contenu", "")
        doublon = req.get("doublon_probable", False)

        card_class = "exigence-header"
        if doublon:
            card_class += " doublon"

        st.markdown(f"""
        <div class="{card_class}">
            <div class="exigence-id">{html.escape(str(req_id))}</div>
            <div class="exigence-nom">{html.escape(nom)}</div>
            {"<div class='badge-doublon'>⚠ Doublon probable</div>" if doublon else ""}
        </div>
        """, unsafe_allow_html=True)

        st.info(contenu)
        st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("→ Reformuler TOUTES les exigences", use_container_width=True):
            st.session_state.selected_for_reformulation = [r["id"] for r in reqs]
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("→ Sélectionner les exigences à reformuler", use_container_width=True):
            st.session_state.step = 2.5
            st.rerun()

elif st.session_state.step == 2.5:
    st.markdown("## Sélectionner les exigences à reformuler")

    if st.button("← Retour", type="secondary"):
        st.session_state.step = 2
        st.rerun()

    reqs = st.session_state.requirements or []
    selected_ids = []

    for req in reqs:
        req_id = req.get("id", "?")
        nom = req.get("nom", "Sans titre")

        if st.checkbox(f"{req_id} — {nom}", value=True):
            selected_ids.append(req_id)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if st.button(f"→ Reformuler {len(selected_ids)} exigence(s)", use_container_width=True):
        if selected_ids:
            st.session_state.selected_for_reformulation = selected_ids
            st.session_state.step = 3
            st.rerun()
        else:
            st.warning("Sélectionnez au moins une exigence")

elif st.session_state.step == 3:
    st.markdown("## Étape 3: Reformulation des exigences")

    if st.button("← Nouvelle analyse", type="secondary"):
        reset_analysis()

    session_id = st.session_state.session_id
    selected_ids = st.session_state.selected_for_reformulation

    with st.spinner("Reformulation en cours..."):
        try:
            response = requests.post(
                f"{API_URL}/reformulate/{session_id}",
                json={
                    "requirement_ids": selected_ids,
                    "batch_size": 10,
                    "model": "claude-haiku-4-5-20251001"
                },
                timeout=300
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.reformulations = data["reformulations"]
                st.session_state.step = 4
                st.rerun()
            else:
                st.error(f"Erreur serveur : {response.text}")

        except requests.exceptions.Timeout:
            st.error("Le traitement a pris trop de temps.")
        except requests.exceptions.ConnectionError:
            st.error("Impossible de contacter le serveur.")

elif st.session_state.step == 4:
    st.markdown("## Étape 4: Sélection et export")

    if st.button("← Nouvelle analyse", type="secondary"):
        reset_analysis()

    reqs = st.session_state.requirements or []
    refos = st.session_state.reformulations or {}
    nb_total = len(reqs)
    nb_selections = len(st.session_state.selections)

    st.markdown(f"""
    <div class="stats-bar">
        <div>
            <span class="stat-number">{nb_total}</span>
            <span class="stat-label">Exigences</span>
        </div>
        <div>
            <span class="stat-number">{nb_selections}/{nb_total}</span>
            <span class="stat-label">Validées</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    for req in reqs:
        req_id = req.get("id", "?")
        nom = req.get("nom", "Sans titre")
        contenu = req.get("contenu", "")
        refo_data = refos.get(req_id, {})
        conforme = refo_data.get("conforme", False)
        reformulations = refo_data.get("reformulations", [])

        st.markdown(f"""
        <div class="exigence-header">
            <div class="exigence-id">{html.escape(str(req_id))}</div>
            <div class="exigence-nom">{html.escape(nom)}</div>
        </div>
        """, unsafe_allow_html=True)

        if conforme:
            st.success("✓ Conforme IEEE-830 — exigence conservée")
            st.session_state.selections[req_id] = contenu
        elif reformulations:
            st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
            selection_actuelle = st.session_state.selections.get(req_id)

            for i, (col, refo) in enumerate(zip(cols, reformulations[:3])):
                with col:
                    refo_safe = html.escape(refo)
                    est_selectionnee = selection_actuelle == refo
                    card_style = "refo-card selected" if est_selectionnee else "refo-card"

                    st.markdown(f"""
                    <div class="{card_style}">
                        <div class="refo-number">Version {i + 1}</div>
                        <div class="refo-text">{refo_safe}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    label_btn = "✓ Sélectionnée" if est_selectionnee else f"Version {i + 1}"
                    if st.button(label_btn, key=f"btn_{req_id}_{i}", use_container_width=True):
                        st.session_state.selections[req_id] = refo
                        st.rerun()

            if st.button(
                "↩ Garder l'original",
                key=f"btn_{req_id}_original",
                type="secondary",
                use_container_width=True
            ):
                st.session_state.selections[req_id] = contenu
                st.rerun()
        else:
            st.warning("Erreur lors de la reformulation")

        st.markdown("<div style='margin-bottom:2rem'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if nb_selections == nb_total:
        st.success("✓ Toutes les exigences ont été traitées")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Télécharger (Word)", use_container_width=True):
                with st.spinner("Génération du fichier..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/export/{st.session_state.session_id}",
                            json={
                                "format": "word",
                                "selected_requirements": st.session_state.selections
                            }
                        )
                        if response.status_code == 200:
                            st.download_button(
                                label="💾 Télécharger (Word)",
                                data=response.content,
                                file_name=f"cahier_reformule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Erreur : {e}")

        with col2:
            if st.button("📊 Télécharger (Excel)", use_container_width=True):
                with st.spinner("Génération du fichier..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/export/{st.session_state.session_id}",
                            json={
                                "format": "excel",
                                "selected_requirements": st.session_state.selections
                            }
                        )
                        if response.status_code == 200:
                            st.download_button(
                                label="💾 Télécharger (Excel)",
                                data=response.content,
                                file_name=f"exigences_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Erreur : {e}")
    else:
        remaining = nb_total - nb_selections
        st.markdown(
            f"<div style='color:#6B6B7A; font-size:0.825rem; margin-bottom:1rem'>"
            f"{remaining} exigence(s) en attente de validation.</div>",
            unsafe_allow_html=True
        )
