
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# === DATI COMPETENZE DIGITALI: ITALIA ===
# Anni e valori reali da sdg_04_70.csv
anni_italia = [2021, 2023]
valori_italia = [45.6, 45.8]  # Media italiana

model_italia = LinearRegression()
model_italia.fit(np.array(anni_italia).reshape(-1, 1), np.array(valori_italia))
previsione_2030 = model_italia.predict([[2030]])[0]
trend = model_italia.coef_[0]
raggiunto = previsione_2030 >= 80

# === ANALISI PAESE ===
print("📊 Analisi Italia:")
print(f"  - Competenze digitali attuali (2023): {valori_italia[-1]}%")
print(f"  - Previsione per il 2030: {previsione_2030:.1f}%")
if raggiunto:
    print("✅ L'Italia raggiungerà il target dell'80% entro il 2030")
else:
    print("❌ L'Italia NON raggiungerà il target dell'80% entro il 2030")

# === DATI PAESE UE ===
df_ue = pd.read_csv("data/sdg_04_70.csv")
df_ue_validi = df_ue[df_ue["TIME_PERIOD"].isin([2021, 2023])].dropna(subset=["OBS_VALUE"])

# Paesi che superano l'80%
df_target = (
    df_ue_validi[df_ue_validi["OBS_VALUE"] >= 80]
    .groupby("TIME_PERIOD")["geo"].nunique()
    .reset_index(name="Paesi_80")
)
df_tot = (
    df_ue_validi.groupby("TIME_PERIOD")["geo"].nunique()
    .reset_index(name="Totale_Paesi")
)

df_merged = pd.merge(df_target, df_tot, on="TIME_PERIOD")
df_merged["Percentuale_Paesi_80"] = (df_merged["Paesi_80"] / df_merged["Totale_Paesi"]) * 100

# === ANALISI UE ===
print("\n📊 Analisi Unione Europea:")
for _, row in df_merged.iterrows():
    print(f"  - Anno {int(row['TIME_PERIOD'])}: {int(row['Paesi_80'])} su {int(row['Totale_Paesi'])} paesi hanno superato l'80% ({row['Percentuale_Paesi_80']:.1f}%)")

if df_merged["Percentuale_Paesi_80"].iloc[-1] < 20:
    print("❌ Attualmente meno del 20% dei paesi UE ha superato l'80% di competenze digitali. Il target 2030 è lontano.")

# === RACCOMANDAZIONI PER L'ITALIA ===
print("\n🛠️ Raccomandazioni per accelerare la digitalizzazione in Italia:")
print("  1. Aumentare l'investimento in formazione digitale per adulti e lavoratori.")
print("  2. Rafforzare la sinergia tra PA e scuole per promuovere competenze.")
print("  3. Potenziare la comunicazione sull'utilità dei servizi digitali (App IO, SPID, CIE).")
print("  4. Incentivare la migrazione dei servizi PA ai canali digitali in piccoli comuni.")
print("  5. Monitorare costantemente l'adozione e usabilità dei servizi.")

