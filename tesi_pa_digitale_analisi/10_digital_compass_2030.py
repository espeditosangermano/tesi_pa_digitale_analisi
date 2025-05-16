
import pandas as pd
import matplotlib.pyplot as plt

# === LETTURA DEI CSV DA /data ===
df_competenze = pd.read_csv("data/estat_isoc_sk_dskl_i21_en.csv")
df_specialisti = pd.read_csv("data/estat_isoc_sks_itspt_en.csv")
df_eid = pd.read_csv("data/estat_isoc_eid_ieid_en.csv")
df_ciegi = pd.read_csv("data/estat_isoc_ciegi_ac_en.csv")
df_bigdata = pd.read_csv("data/estat_isoc_eb_ai_en.csv")

# === ESTRAZIONE VALORI PER ITALIA E ANNO PIÙ RECENTE ===
anno_target = 2023

# 1. Competenze digitali base o superiori
competenze_italia = df_competenze[
    (df_competenze["geo"] == "Italy") &
    (df_competenze["TIME_PERIOD"] == anno_target) &
    (df_competenze["indic_is"].str.contains("basic or above basic overall digital skills"))
]
valore_competenze = float(competenze_italia["OBS_VALUE"].values[0])

# 2. Specialisti ICT (percentuale sull’occupazione)
specialisti_italia = df_specialisti[
    (df_specialisti["geo"] == "Italy") &
    (df_specialisti["TIME_PERIOD"] == anno_target)
]
valore_specialisti = float(specialisti_italia["OBS_VALUE"].values[0])

# 3. Uso dell’identità digitale per accesso PA
eid_italia = df_eid[
    (df_eid["geo"] == "Italy") &
    (df_eid["TIME_PERIOD"] == anno_target)
]
valore_eid = float(eid_italia["OBS_VALUE"].values[0])

# 4. eGovernment - uso servizi pubblici online
ciegi_italia = df_ciegi[
    (df_ciegi["geo"] == "Italy") &
    (df_ciegi["TIME_PERIOD"] == anno_target)
]
valore_egov = float(ciegi_italia["OBS_VALUE"].values[0])

# 5. Big Data o AI o Cloud - prendiamo uno dei principali indicatori disponibili
bigdata_italia = df_bigdata[
    (df_bigdata["geo"] == "Italy") &
    (df_bigdata["TIME_PERIOD"] == anno_target)
]
valore_bigdata = float(bigdata_italia["OBS_VALUE"].values[0])

# === TARGET DIGITAL COMPASS 2030 ===
TARGETS = {
    "Competenze digitali": 80,
    "Specialisti ICT": 20,
    "eID / Servizi PA": 100,
    "eGovernment": 100,
    "Big Data / AI / Cloud": 75
}

# === PROGRESSO PERCENTUALE ===
progressi = {
    "Competenze digitali": valore_competenze / TARGETS["Competenze digitali"] * 100,
    "Specialisti ICT": valore_specialisti / TARGETS["Specialisti ICT"] * 100,
    "eID / Servizi PA": valore_eid / TARGETS["eID / Servizi PA"] * 100,
    "eGovernment": valore_egov / TARGETS["eGovernment"] * 100,
    "Big Data / AI / Cloud": valore_bigdata / TARGETS["Big Data / AI / Cloud"] * 100,
}

df_progressi = pd.DataFrame(progressi.items(), columns=["Obiettivo", "Progresso (%)"])
df_progressi.to_csv("data/progresso_digital_compass.csv", index=False)

# === GRAFICO ===
plt.figure(figsize=(9, 5))
plt.bar(df_progressi["Obiettivo"], df_progressi["Progresso (%)"], color="steelblue")
plt.title("Progresso Italia verso gli obiettivi Digital Compass 2030")
plt.ylim(0, 120)
plt.ylabel("Progresso (%)")
plt.xticks(rotation=15)
plt.axhline(100, color="green", linestyle="--", linewidth=1)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("grafici/progresso_digital_compass.png")
plt.close()
