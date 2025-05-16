import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression

PAESI = ["IT", "FR", "DE", "ES", "EU27_2020"]
INDICATORE_CIEGI = "I_IGOV12FM"
INDICATORE_EID = "I_IEID"
COLONNA_EID = "2023 "
ETICHETTE = {
    "I_IGOV12FM": "Accesso PA digitale",
    "I_IEID": "Uso identità digitale"
}
ANNO_TARGET = "2023"

def carica_ciegi(path, indicatore, paesi):
    all_data = []
    for chunk in pd.read_csv(path, sep="\t", encoding="utf-8", chunksize=5000, engine="python"):
        try:
            chunk[["freq", "indic_is", "unit", "ind_type", "geo"]] = chunk[chunk.columns[0]].str.split(",", expand=True)
            chunk["indic_is"] = chunk["indic_is"].str.strip()
            chunk["geo"] = chunk["geo"].str.strip()
            chunk = chunk[(chunk["indic_is"] == indicatore) & (chunk["geo"].isin(paesi))]
            chunk.columns = [col.strip() for col in chunk.columns]
            years = [col for col in chunk.columns if col.isdigit()]
            chunk_melt = chunk.melt(id_vars=["geo", "indic_is"], value_vars=years,
                                    var_name="anno", value_name="valore")
            chunk_melt["valore"] = chunk_melt["valore"].astype(str).str.replace(":", "").str.replace("u", "")
            chunk_melt["valore"] = pd.to_numeric(chunk_melt["valore"], errors="coerce")
            all_data.append(chunk_melt)
        except:
            continue
    return pd.concat(all_data, ignore_index=True)

def proietta(df, indicatore, anno_target):
    predizioni = []
    for geo in df["geo"].unique():
        df_geo = df[(df["geo"] == geo) & (df["indic_is"] == indicatore)].dropna()
        if len(df_geo) >= 2:
            X = df_geo["anno"].astype(int).values.reshape(-1, 1)
            y = df_geo["valore"].values
            model = LinearRegression()
            model.fit(X, y)
            pred = model.predict([[int(anno_target)]])[0]
            predizioni.append({"geo": geo, "indic_is": indicatore, "valore": pred})
    return pd.DataFrame(predizioni)

def carica_eid(path, indicatore, paesi):
    chunks = []
    for chunk in pd.read_csv(path, sep="\t", encoding="utf-8", chunksize=10000, engine="python"):
        try:
            chunk[["freq", "ind_type", "indic_is", "unit", "geo"]] = chunk[chunk.columns[0]].str.split(",", expand=True)
            chunk["indic_is"] = chunk["indic_is"].str.strip()
            chunk["geo"] = chunk["geo"].str.strip()
            chunk = chunk[(chunk["indic_is"] == indicatore) & (chunk["geo"].isin(paesi))]
            chunk["valore"] = chunk[COLONNA_EID].astype(str).str.replace(":", "").str.replace("u", "")
            chunk["valore"] = pd.to_numeric(chunk["valore"], errors="coerce")
            chunks.append(chunk[["geo", "indic_is", "valore"]])
        except:
            continue
    return pd.concat(chunks, ignore_index=True)

def radar_chart(df, path_out):
    df = df.groupby(["geo", "indic_is"], as_index=False).agg({"valore": "mean"})  # deduplicazione
    df_pivot = df.pivot(index="geo", columns="indic_is", values="valore")
    if df_pivot.empty:
        print("⚠️ Nessun dato per radar chart")
        return
    categories = [ETICHETTE[i] for i in df_pivot.columns]
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for idx, row in df_pivot.iterrows():
        values = [row[i] for i in df_pivot.columns]
        values += values[:1]
        ax.plot(angles, values, label=idx)
        ax.fill(angles, values, alpha=0.1)
    ax.set_title(f"Radar Chart PA Digitale - {ANNO_TARGET}", y=1.08)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    plt.tight_layout()
    plt.savefig(path_out)
    plt.close()

def classifica(df, indicatore):
    df_ind = df[df["indic_is"] == indicatore].copy()
    if df_ind.empty:
        return
    df_ind = df_ind.groupby("geo", as_index=False).agg({"valore": "mean"})  # deduplica
    df_ind = df_ind.sort_values(by="valore", ascending=False).reset_index(drop=True)
    df_ind["posizione"] = df_ind.index + 1
    df_ind.to_csv(f"data/classifica_{indicatore}_{ANNO_TARGET}.csv", index=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_ind, x="valore", y="geo", palette="crest")
    plt.title(f"Classifica {indicatore} - {ANNO_TARGET}")
    plt.xlabel("Valore (%)")
    plt.ylabel("Paese")
    plt.tight_layout()
    plt.savefig(f"grafici/classifica_{indicatore}_{ANNO_TARGET}.png")
    plt.close()

# MAIN
df_ciegi = carica_ciegi("data/estat_isoc_ciegi_ac.tsv", INDICATORE_CIEGI, PAESI)
df_proj = proietta(df_ciegi, INDICATORE_CIEGI, ANNO_TARGET)
df_eid = carica_eid("data/estat_isoc_eid_ieid.tsv", INDICATORE_EID, PAESI)

df_finale = pd.concat([df_proj, df_eid])
df_finale.to_csv("data/indicatori_pa_digitali_2023.csv", index=False)

radar_chart(df_finale, "grafici/radar_pa_digitale_2023.png")
for indic in df_finale["indic_is"].unique():
    classifica(df_finale, indic)
