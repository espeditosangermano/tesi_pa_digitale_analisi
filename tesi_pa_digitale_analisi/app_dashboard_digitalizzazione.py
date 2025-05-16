
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dashboard Digitalizzazione PA", layout="wide")
st.title("📊 Dashboard - Digitalizzazione della Pubblica Amministrazione")

st.markdown("""
Questa dashboard interattiva raccoglie i principali risultati delle analisi sulla digitalizzazione della Pubblica Amministrazione italiana:
- Adozione PNRR
- Competenze Digitali
- Accesso ai Servizi Pubblici
- Confronto Europeo
- Indicatori Regionali
- Previsioni 2030
""")

# Sezione 1: Indicatori Principali
st.header("📌 Indicatori chiave e confronti")

st.image("grafici/accesso_servizi_digitali.png", caption="Accesso ai Servizi Pubblici Digitali (Italia)", use_container_width=True)
st.image("grafici/adozione_pnrr_regioni.png", caption="Adozione PNRR per Regione", use_container_width=True)

# Sezione 2: Confronto Europeo
st.header("🌍 Confronto Europeo")

col1, col2 = st.columns(2)
with col1:
    st.image("grafici/confronto_barre_I_DSK2_AB.png", caption="Competenze Digitali (I_DSK2_AB)")
with col2:
    st.image("grafici/confronto_barre_I_IGOV12FM.png", caption="Uso Servizi Digitali (I_IGOV12FM)")

# Sezione 3: Indicatori Regionali
st.header("🏛️ Digitalizzazione Regionale e Zonale")
col3, col4 = st.columns(2)
with col3:
    st.image("grafici/indice_digitalizzazione_regioni.png", caption="Indice Digitalizzazione per Regione")
with col4:
    st.image("grafici/indice_digitalizzazione_zone.png", caption="Indice Digitalizzazione per Zona")

st.image("grafici/distribuzione_classi_adozione.png", caption="Distribuzione Classi Adozione Digitale", use_container_width=True)

# Sezione 4: Previsioni
st.header("📈 Previsione Target Competenze Digitali")

st.image("grafici/target_competenze_digitali.png", caption="Competenze Digitali - Italia vs Target UE 2030", use_container_width=True)
st.image("grafici/previsione_target_80.png", caption="Previsione Raggiungimento 80% Competenze Digitali", use_container_width=True)

# Conclusione
st.markdown("""
---
**Nota**: I grafici sono il risultato dell'elaborazione dati su fonti ISTAT, Eurostat e PA Digitale. Le previsioni sono basate su modelli lineari sviluppati con Python.

© 2025 – Analisi realizzata nell'ambito di un progetto di tesi magistrale.
""")


# --- Sezione Download ---
st.header("📥 Scarica Report e Dati")

report_path = "report_digitalizzazione_con_previsioni.pdf"
if os.path.exists(report_path):
    with open(report_path, "rb") as f:
        st.download_button(
            label="📄 Scarica Report PDF",
            data=f,
            file_name="report_digitalizzazione.pdf",
            mime="application/pdf"
        )

# Carica file CSV principali se esistono
csv_files = {
    "📊 Correlazione Digitale": "data/correlazione_digitale_pnrr.csv",
    "🏛️ Adozione PNRR per Regione": "data/adozione_pnrr_regioni.csv",
}

for label, path in csv_files.items():
    if os.path.exists(path):
        with open(path, "rb") as f:
            st.download_button(
                label=f"⬇️ Scarica {label}",
                data=f,
                file_name=os.path.basename(path),
                mime="text/csv"
            )
