import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Funzione per caricamento filtrato a blocchi
def carica_filtrato(path, indicatore, paesi):
    chunks = []
    for chunk in pd.read_csv(path, encoding="utf-8", usecols=["indic_is", "geo", "TIME_PERIOD", "OBS_VALUE"], chunksize=100000):
        filtrato = chunk[
            (chunk["indic_is"] == indicatore) &
            (chunk["geo"].isin(paesi)) &
            (chunk["TIME_PERIOD"].isin([2021, 2022, 2023]))
        ]
        chunks.append(filtrato)
    return pd.concat(chunks, ignore_index=True)

# Carica e filtra i due dataset
df_dskl = carica_filtrato("data/isoc_sk_dskl_i21.csv", "I_DSK2_AB", ["IT", "EU27_2020"])
df_egov = carica_filtrato("data/isoc_ciegi_ac.csv", "I_IGOV12FM", ["IT", "EU27_2020"])

# Aggiunge etichette per leggibilità
df_dskl["Indicatore"] = "Competenze digitali di base"
df_egov["Indicatore"] = "Uso dell'eGovernment"
df_trend = pd.concat([df_dskl, df_egov])

# Pulizia valori
df_trend["OBS_VALUE"] = pd.to_numeric(df_trend["OBS_VALUE"], errors="coerce")
df_trend["TIME_PERIOD"] = df_trend["TIME_PERIOD"].astype(int)

# Raggruppa per media (in caso di duplicati)
df_trend_clean = df_trend.groupby(["geo", "Indicatore", "TIME_PERIOD"], as_index=False)["OBS_VALUE"].mean()

# Salva tabella dati finale
df_trend_clean.to_csv("data/analisi_temporale_indicatori.csv", index=False)

# Grafico temporale
plt.figure(figsize=(10, 6))
sns.lineplot(
    data=df_trend_clean,
    x="TIME_PERIOD",
    y="OBS_VALUE",
    hue="geo",
    style="Indicatore",
    markers=True,
    dashes=False,
    palette={"IT": "#1f77b4", "EU27_2020": "#ff7f0e"}
)
plt.title("Evoluzione Competenze Digitali ed eGovernment (2021–2023)")
plt.xlabel("Anno")
plt.ylabel("Valore (%)")
plt.legend(title="Paese / Indicatore")
plt.tight_layout()
plt.savefig("grafici/analisi_temporale_digitalizzazione.png", dpi=300)
plt.close()
