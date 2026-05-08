import streamlit as st
import requests

st.title("Aide à la rédaction — Cahier des charges")

# 1. Upload du fichier
fichier = st.file_uploader("Dépose ton cahier des charges", type=["docx"])

# 2. Bouton Analyser
if fichier and st.button("Analyser"):

    with st.spinner("Analyse en cours... (peut prendre 1-2 minutes)"):
        response = requests.post(
            "http://localhost:8000/analyser",
            files={"fichier": (fichier.name, fichier, "application/octet-stream")}
        )

    # 3. Afficher les résultats
    if response.status_code == 200:
        data = response.json()
        st.success(f"{data['nb_taches']} exigences trouvées")

        for tache in data["taches"]:
            st.divider()
            st.markdown(f"**{tache['id']} — {tache['nom']}**")
            st.info(tache["contenu"])

            if tache.get("doublon_probable"):
                st.warning("Doublon probable détecté")

            refo = tache.get("reformulations", {})
            if not refo.get("conforme"):
                for i, r in enumerate(refo.get("reformulations", []), 1):
                    st.success(f"Version {i} : {r}")
            else:
                st.success("Exigence déjà conforme IEEE-830")
    else:
        st.error(f"Erreur : {response.text}")