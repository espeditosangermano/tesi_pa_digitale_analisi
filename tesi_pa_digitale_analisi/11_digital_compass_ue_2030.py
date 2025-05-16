import pandas as pd
import matplotlib.pyplot as plt

# === Obiettivi Digital Compass 2030 ===
TARGETS = {
    "Competenze digitali": 80,
    "Specialisti ICT": 20000000,
    "Cloud computing": 75,
    "Big Data": 75,
    "Infrastrutture digitali": 100
}

# === Lettura Competenze digitali ===
df_comp = pd.read_csv("data/estat_isoc_sk_dskl_i21_en.csv", encoding="utf-8")
df_comp = df_comp[(df_comp["indic_is"] == "I_DSK2_AB") & (df_comp["TIME_PERIOD"] == 2023)]
df_comp = df_comp[["geo", "OBS_VALUE"]].rename(columns={"geo": "Paese", "OBS_VALUE": "Competenze digitali"})

# === Lettura Specialisti ICT ===
df_ict = pd.read_csv("data/estat_isoc_sks_itspt_en.csv", encoding="utf-8")
df_ict = df_ict[(df_ict["TIME_PERIOD"] == 2023) & (df_ict["unit"] == "NR")]
df_ict = df_ict[["geo", "OBS_VALUE"]].rename(columns={"geo": "Paese", "OBS_VALUE": "Specialisti ICT"})

# === Lettura Cloud Computing ===
df_cloud = pd.read_excel("data/626058-3.3-enterprises-cloud-firm-size.xls", skiprows=3)
df_cloud.columns.values[0] = "Paese"
df_cloud = df_cloud.rename(columns={df_cloud.columns[1]: "Cloud computing"})
df_cloud = df_cloud[["Paese", "Cloud computing"]]

# === Lettura Big Data ===
df_big = pd.read_excel("data/626071-3.4-enterprises-big-data.xls", skiprows=3)
df_big.columns.values[0] = "Paese"
df_big = df_big.rename(columns={df_big.columns[1]: "Big Data"})
df_big = df_big[["Paese", "Big Data"]]

# === Lettura Infrastrutture digitali ===
df_fibra = pd.read_excel("data/1-10-fibre-in-total-broadband.xls", skiprows=42)
df_fibra.columns.values[0] = "Paese"
df_fibra = df_fibra.rename(columns={df_fibra.columns[1]: "Infrastrutture digitali"})
df_fibra = df_fibra[["Paese", "Infrastrutture digitali"]]

# === Merge flessibile (outer join) ===
df = df_comp.merge(df_ict, on="Paese", how="outer")\
           .merge(df_cloud, on="Paese", how="outer")\
           .merge(df_big, on="Paese", how="outer")\
           .merge(df_fibra, on="Paese", how="outer")

# === Debug: verifica dimensioni e anteprima ===
print("📊 Paesi dopo merge:", df.shape)
print("📌 Esempio: riga mancante di chiusura corretta")
print("📊 Anteprima dati:", df.head())

# === Filtraggio: almeno 3 indicatori su 5 disponibili ===
df["non_nulli"] = df.notnull().sum(axis=1) - 1  # meno 1 per la colonna 'Paese'
df = df[df["non_nulli"] >= 3].drop(columns=["non_nulli"])

# === Conversione a numerico dove necessario ===
for col in ["Competenze digitali", "Specialisti ICT", "Cloud computing", "Big Data", "Infrastrutture digitali"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# === Normalizzazione specialisti ICT ===
pop_eu = 448000000
df["Specialisti ICT %"] = (df["Specialisti ICT"] / (TARGETS["Specialisti ICT"] / pop_eu)) * 100

# === Calcolo Progresso Digital Compass ===
def calcola_progresso(riga):
    pesi = []
    valori = []
    if pd.notnull(riga["Competenze digitali"]):
        pesi.append(1); valori.append(riga["Competenze digitali"] / TARGETS["Competenze digitali"])
    if pd.notnull(riga["Specialisti ICT %"]):
        pesi.append(1); valori.append(riga["Specialisti ICT %"] / 100)
    if pd.notnull(riga["Cloud computing"]):
        pesi.append(1); valori.append(riga["Cloud computing"] / TARGETS["Cloud computing"])
    if pd.notnull(riga["Big Data"]):
        pesi.append(1); valori.append(riga["Big Data"] / TARGETS["Big Data"])
    if pd.notnull(riga["Infrastrutture digitali"]):
        pesi.append(1); valori.append(riga["Infrastrutture digitali"] / TARGETS["Infrastrutture digitali"])
    if pesi:
        return 100 * sum(valori) / sum(pesi)
    return None

df["Progresso %"] = df.apply(calcola_progresso, axis=1)
df = df.dropna(subset=["Progresso %"])

# === Salvataggi ===
df.to_csv("data/classifica_digital_compass_ue.csv", index=False)

# === Visualizzazione ===
df_sorted = df.sort_values("Progresso %", ascending=False)
plt.figure(figsize=(14, 6))
plt.bar(df_sorted["Paese"], df_sorted["Progresso %"], color="mediumseagreen")
plt.title("Classifica Progresso Digital Compass 2030 – Paesi UE")
plt.ylabel("Progresso verso il target (%)")
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("grafici/classifica_digital_compass_ue.png")
plt.close()

# --- Grafico: Progresso medio Digital Compass 2030 per area (media UE) ---
try:
    df_media_ue = pd.read_csv("data/progresso_digital_compass.csv")
    df_media_sorted = df_media_ue.sort_values(by="Progresso (%)", ascending=False)

    plt.figure(figsize=(14, 6))
    plt.bar(df_media_sorted["Obiettivo"], df_media_sorted["Progresso (%)"], color="seagreen")
    plt.axhline(100, color="red", linestyle="--", label="Target 100%%")
    plt.xticks(rotation=45, ha="right")
    plt.title("Progresso medio verso gli obiettivi Digital Compass 2030 (media UE)")
    plt.ylabel("Progresso (%)")
    plt.xlabel("Obiettivi")
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafici/progresso_medio_digital_compass_ue.png")
    print("✅ Grafico 'progresso_medio_digital_compass_ue.png' salvato correttamente.")
except Exception as e:
    print("⚠️ Errore nella generazione del grafico di progresso medio UE:", e)