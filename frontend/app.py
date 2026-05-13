import streamlit as st
import requests
import html

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
#  CSS
# ============================================================
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
.exigence-header.en-attente { border-left-color: #3A3D4E; }

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

.refo-card:hover { border-color: #E8A020; }

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

[data-testid="stAlert"] svg { display: none !important; }

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
</style>
""", unsafe_allow_html=True)

# ============================================================
#  CONSTANTES
# ============================================================
API_URL = "http://127.0.0.1:8000"

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
if "reformulations" not in st.session_state:
    st.session_state["reformulations"] = {}

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
                    <div style="font-weight:500; font-size:0.9rem; color:#E8E6E0">{html.escape(fichier.name)}</div>
                    <div style="font-size:0.75rem; color:#6B6B7A">{round(fichier.size / 1024)} Ko</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Lancer l'analyse", use_container_width=True):
                with st.spinner("Lecture du document et extraction des exigences..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/extraire",
                            files={"fichier": (fichier.name, fichier, "application/octet-stream")},
                            timeout=120
                        )

                        if response.status_code == 200:
                            data = response.json()
                            st.session_state["resultats"] = data["taches"]
                            st.session_state["nom_fichier"] = data["nom_fichier"]
                            st.session_state["reformulations"] = {}
                            st.session_state["selections"] = {}
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
    nb_reformulees = len(st.session_state["reformulations"])
    nb_conformes = sum(
        1 for t in taches
        if st.session_state["reformulations"].get(t.get("id"), {}).get("conforme")
    )
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
            <span class="stat-number">{nb_reformulees}/{nb_total}</span>
            <span class="stat-label">Reformulées</span>
        </div>
        <div>
            <span class="stat-number">{nb_selections}/{nb_total}</span>
            <span class="stat-label">Validées</span>
        </div>
        <div style="margin-left:auto; font-size:0.75rem; color:#6B6B7A; font-family:'IBM Plex Mono',monospace;">
            {html.escape(st.session_state["nom_fichier"])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Actions ---
    col_reset, col_all, _ = st.columns([1, 2, 2])
    with col_reset:
        if st.button("← Nouvelle analyse", type="secondary"):
            st.session_state["resultats"] = None
            st.session_state["selections"] = {}
            st.session_state["nom_fichier"] = ""
            st.session_state["reformulations"] = {}
            st.rerun()

    with col_all:
        # Bouton pour reformuler toutes les exigences non encore reformulées
        taches_restantes = [
            t for t in taches
            if t.get("id") not in st.session_state["reformulations"]
        ]
        if taches_restantes:
            if st.button(f"Reformuler toutes ({len(taches_restantes)} restantes)"):
                barre = st.progress(0)
                for i, tache in enumerate(taches_restantes):
                    with st.spinner(f"Reformulation {i+1}/{len(taches_restantes)}..."):
                        try:
                            resp = requests.post(
                                f"{API_URL}/reformuler",
                                json={
                                    "id": tache["id"],
                                    "nom": tache["nom"],
                                    "contenu": tache["contenu"],
                                    "doublon_probable": tache.get("doublon_probable", False)
                                },
                                timeout=60
                            )
                            if resp.status_code == 200:
                                st.session_state["reformulations"][tache["id"]] = resp.json()
                        except Exception:
                            pass
                    barre.progress((i + 1) / len(taches_restantes))
                st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # --- Liste des exigences ---
    for tache in taches:
        tid = tache.get("id", "?")
        nom = tache.get("nom", "Sans titre")
        contenu = tache.get("contenu", "")
        doublon = tache.get("doublon_probable", False)

        # Récupérer les reformulations depuis le session_state
        refo_data = st.session_state["reformulations"].get(tid)
        conforme = refo_data.get("conforme", False) if refo_data else False
        reformulations = refo_data.get("reformulations", []) if refo_data else []

        tid_safe = html.escape(str(tid))
        nom_safe = html.escape(nom)

        # Classe CSS de la carte selon état
        card_class = "exigence-header"
        if refo_data and conforme:
            card_class += " conforme"
        elif doublon:
            card_class += " doublon"

        # En-tête
        st.markdown(f"""
        <div class="{card_class}">
            <div class="exigence-id">{tid_safe}</div>
            <div class="exigence-nom">{nom_safe}</div>
            {"<div class='badge-doublon'>⚠ Doublon probable</div>" if doublon else ""}
            {"<div class='badge-conforme'>✓ Conforme IEEE-830</div>" if (refo_data and conforme) else ""}
        </div>
        """, unsafe_allow_html=True)

        # Contenu original
        st.info(contenu)

        # ── Pas encore reformulé ──────────────────────────────
        if refo_data is None:
            col_btn, _ = st.columns([1, 3])
            with col_btn:
                if st.button(
                    "Analyser et reformuler",
                    key=f"btn_refo_{tid}"
                ):
                    with st.spinner("Reformulation en cours..."):
                        try:
                            resp = requests.post(
                                f"{API_URL}/reformuler",
                                json={
                                    "id": tid,
                                    "nom": nom,
                                    "contenu": contenu,
                                    "doublon_probable": doublon
                                },
                                timeout=60
                            )
                            if resp.status_code == 200:
                                st.session_state["reformulations"][tid] = resp.json()
                                st.rerun()
                            else:
                                st.error("Erreur lors de la reformulation.")
                        except requests.exceptions.Timeout:
                            st.error("Délai dépassé. Réessayez.")

        # ── Déjà conforme ─────────────────────────────────────
        elif conforme:
            st.success("Cette exigence respecte déjà les critères IEEE-830.")
            st.session_state["selections"][tid] = contenu

        # ── Reformulations disponibles ────────────────────────
        elif reformulations:
            st.markdown("""
            <div style="background:#13151F; border:1px solid #2A2D3E; border-top:none;
                        padding:1rem 1.5rem 0.5rem 1.5rem;">
                <div style="font-size:0.65rem; font-weight:600; color:#6B6B7A;
                            letter-spacing:0.15em; text-transform:uppercase;">
                    Reformulations proposées — sélectionnez celle qui convient
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            cols = [col1, col2, col3]
            selection_actuelle = st.session_state["selections"].get(tid)

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

                    label_btn = "✓ Sélectionnée" if est_selectionnee else f"Choisir la version {i + 1}"
                    if st.button(label_btn, key=f"btn_{tid}_{i}", use_container_width=True):
                        st.session_state["selections"][tid] = refo
                        st.rerun()

            st.markdown("""
            <div style="background:#13151F; border:1px solid #2A2D3E; border-top:none;
                        padding:0.5rem 1.5rem 1rem 1.5rem; border-radius:0 0 6px 6px;">
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "↩ Conserver l'exigence originale",
                key=f"btn_{tid}_original",
                type="secondary"
            ):
                st.session_state["selections"][tid] = contenu
                st.rerun()

        st.markdown("<div style='margin-bottom:2rem'></div>", unsafe_allow_html=True)

    # --- Export ---
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if nb_selections == nb_total:
        st.success("Toutes les exigences ont été traitées. Vous pouvez exporter le rapport.")
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