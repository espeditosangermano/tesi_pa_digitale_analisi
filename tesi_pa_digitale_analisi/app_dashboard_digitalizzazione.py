
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="📊 Dashboard Completa Digitalizzazione", layout="wide")
st.title("📊 Dashboard Completa - Digitalizzazione PA e Confronto UE")

@st.cache_data
def carica_csv(percorso):
    return pd.read_csv(percorso)

# === Percorsi ===
DATA_DIR = "data"
GRAFICI_DIR = "grafici"
REPORT_PDF = "report_digitalizzazione_con_previsioni.pdf"

# === Tabs ===
tabs = st.tabs([
    "🌍 Confronto Europeo",
    "🇮🇹 Indicatori Italiani",
    "🎯 Digital Compass 2030",
    "📥 Download e Report"
])


# 🌍 TAB 1: Confronto Europeo
with tabs[0]:
    st.header("Confronto Europeo su Indicatori Digitali")
    df = carica_csv(os.path.join(DATA_DIR, "confronto_digitale_europa.csv"))
    df["Valore"] = (
    df["Valore"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
    .astype(float)
)
    df["Anno"] = df["Anno"].astype(str)

    indicatore = st.selectbox("Scegli un indicatore:", df["Indicatore"].unique())
    df_sel = df[df["Indicatore"] == indicatore]

    anni_disponibili = sorted(df_sel["Anno"].unique())
    anni_default = [a for a in ["2021", "2022", "2023"] if a in anni_disponibili]
    anni = st.multiselect("Anni:", anni_disponibili, default=anni_default)

    paesi_disponibili = sorted(df_sel["Paese"].unique())
    paesi_default = [p for p in ["IT", "FR", "DE", "ES"] if p in paesi_disponibili]
    paesi = st.multiselect("Paesi:", paesi_disponibili, default=paesi_default)

    df_plot = (
    df_sel[(df_sel["Paese"].isin(paesi)) & (df_sel["Anno"].isin(anni))]
    .groupby(["Anno", "Paese", "Indicatore"], as_index=False)["Valore"]
    .mean()
)

    fig = px.bar(
        df_plot,
        x="Anno",
        y="Valore",
        color="Paese",
        barmode="group",
        text="Valore",
        labels={"Valore": "Percentuale"},
        title=f"Confronto Europeo ({', '.join(anni)}) – Indicatore: {indicatore}"
    )

    fig.update_traces(texttemplate='%{text:.1f}%', textposition="outside")
    fig.update_layout(
        yaxis=dict(range=[0, 100], title="Percentuale (%)"),
        xaxis_title="Anno"
    )

    st.plotly_chart(fig, use_container_width=True)

    

# 🇮🇹 TAB 2: Indicatori Italiani
with tabs[1]:
    st.header("Indicatori per l'Italia")
    st.image(os.path.join(GRAFICI_DIR, "adozione_pnrr_regioni.png"))
    st.image(os.path.join(GRAFICI_DIR, "accesso_servizi_digitali.png"))
    
    st.image(os.path.join(GRAFICI_DIR, "indice_digitalizzazione_regioni.png"))
    
    

# 🎯 TAB 3: Digital Compass 2030
with tabs[2]:
    st.header("Target Digital Compass 2030")
    st.subheader("📈 Italia: andamento rispetto agli obiettivi")
    st.image(os.path.join(GRAFICI_DIR, "target_competenze_digitali.png"))
    
    st.image(os.path.join(GRAFICI_DIR, "progresso_digital_compass.png"))

    st.subheader("🌐 Europa: classifica Digital Compass")
    st.image(os.path.join(GRAFICI_DIR, "classifica_digital_compass_ue.png"))
    st.image(os.path.join(GRAFICI_DIR, "progresso_medio_digital_compass_ue.png"))

# 📥 TAB 4: Download
with tabs[3]:
    st.header("Download file e report")
    st.subheader("📁 Dataset principali")
    file_list = [
        "confronto_digitale_europa.csv",
        "correlazione_digitale_pnrr.csv",
        "indicatori_pa_digitali_2023.csv",
        "progresso_digital_compass.csv",
        "classifica_digital_compass_ue.csv"
    ]
    for file in file_list:
        path = os.path.join(DATA_DIR, file)
        if os.path.exists(path):
            with open(path, "rb") as f:
                st.download_button(f"⬇️ Scarica {file}", f, file_name=file)

    st.subheader("📄 Report PDF Finale")
    if os.path.exists(REPORT_PDF):
        with open(REPORT_PDF, "rb") as f:
            st.download_button("⬇️ Scarica report finale", f, file_name="report_digitalizzazione_con_previsioni.pdf")
