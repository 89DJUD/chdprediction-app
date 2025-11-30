import streamlit as st
import pandas as pd
import joblib
import os
import io

# Configuration de la page

st.set_page_config(
    page_title="Prédiction du risque de CHD",
    page_icon="🫀",
    layout="centered"
)

st.title("🩺 Application de prédiction du risque de maladie cardiaque (CHD)")
st.write("""
Cette application web a été **développée avec VS Code** et déployée avec **Streamlit**.
Elle utilise un modèle de Machine Learning déjà entraîné et sauvegardé dans `Model.pkl`
(pipeline : prétraitement + ACP + régression logistique) à partir du dataset *CHD.csv*.
""")


# 1. Chargement du modèle

@st.cache_resource
def load_model(path: str = "Model.pkl"):
    """Load a model from local path in a cached resource.

    Returns None if the file does not exist so the UI can prompt the user to upload.
    """
    if os.path.exists(path):
        return joblib.load(path)  # même nom que dans le script d'entraînement
    return None

model = load_model()

# If the Model.pkl is missing from the repo/workdir, offer upload in the UI.
if model is None:
    st.warning("Le fichier Model.pkl est introuvable dans le répertoire. Vous pouvez soit ajouter `Model.pkl` au dépôt, soit le téléverser ci-dessous (ou fournir une URL).")
    uploaded_model = st.file_uploader("Téléverser Model.pkl", type=["pkl", "joblib"])
    if uploaded_model is not None:
        try:
            # joblib.load accepts a file-like object; use the uploaded bytes
            model = joblib.load(uploaded_model)
            st.success("Modèle chargé depuis l'upload!")
        except Exception as e:
            st.error(f"Impossible de charger le modèle téléversé: {e}")

if model is None:
    st.stop()


# 2. Formulaire de saisie des variables
#    Variables : sbp, ldl, adiposity, obesity, age, famhist

st.subheader("🧾 Saisir les informations du patient")

with st.form("chd_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Âge", min_value=10, max_value=100, value=50)
        sbp = st.number_input("Pression systolique (sbp)", min_value=80.0, max_value=250.0, value=140.0)
        ldl = st.number_input("LDL (mauvais cholestérol)", min_value=0.0, max_value=10.0, value=4.0)
    
    with col2:
        adiposity = st.number_input("Adiposity", min_value=0.0, max_value=60.0, value=25.0)
        obesity = st.number_input("Obesity", min_value=0.0, max_value=60.0, value=30.0)
        famhist = st.selectbox("Antécédents familiaux (famhist)", ["Present", "Absent"])
    
    submitted = st.form_submit_button("Prédire le risque")


# 3. Prédiction avec le modèle

if submitted:
    # Construire un DataFrame avec exactement les mêmes colonnes que X
    input_data = {
        "sbp": sbp,
        "ldl": ldl,
        "adiposity": adiposity,
        "obesity": obesity,
        "age": age,
        "famhist": famhist
    }
    
    input_df = pd.DataFrame([input_data])
    
    st.write("### Données saisies")
    st.dataframe(input_df)
    
    # Utiliser le pipeline complet sauvegardé dans Model.pkl
    # Il contient déjà : preprocessor (num + cat) + PCA + LogisticRegression
    proba_chd = model.predict_proba(input_df)[0, 1]  # probabilité CHD = 1
    pred_chd = model.predict(input_df)[0]
    
    st.subheader(" Résultat de la prédiction")
    st.write(f"**Probabilité estimée de CHD (classe 1)** : `{proba_chd:.2f}`")
    
    if pred_chd == 1:
        st.error(" Le modèle prédit **un risque élevé** de maladie cardiaque (CHD = 1).")
    else:
        st.success(" Le modèle prédit **un risque faible** de maladie cardiaque (CHD = 0).")
    
    st.info(" Cette application est à but pédagogique et ne remplace pas un avis médical.")