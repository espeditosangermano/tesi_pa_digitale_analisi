import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# Caricamento dei dati dalla cartella /data
df_pa = pd.read_csv("data/Interazione con la PA - reg. e tipo di comune.csv", sep=",", encoding="utf-8", on_bad_lines="skip")
df_conn = pd.read_csv("data/Famiglie e tipo di connessione - reg. e tipo di comune.csv", sep=",", encoding="utf-8", on_bad_lines="skip")

# Filtro per l'anno 2024
df_pa = df_pa[(df_pa["TIME_PERIOD"] == 2024) & (df_pa["REF_AREA"] != "IT")]
df_conn = df_conn[(df_conn["TIME_PERIOD"] == 2024) & (df_conn["REF_AREA"] != "IT")]

# Estrazione delle variabili
df_subfo = df_pa[df_pa["DATA_TYPE"] == "PA_SUBFO"][["REF_AREA", "Territorio", "Osservazione"]].rename(columns={"Osservazione": "invio_moduli_online"})
df_broad = df_conn[df_conn["DATA_TYPE"] == "FAM_CONN_BROAD_FIX"][["REF_AREA", "Territorio", "Osservazione"]].rename(columns={"Osservazione": "connessione_fissa"})
df_mobi = df_conn[df_conn["DATA_TYPE"] == "FAM_CONN_MOBI"][["REF_AREA", "Territorio", "Osservazione"]].rename(columns={"Osservazione": "connessione_mobile"})

# Merge e conversione
df_cluster = df_subfo.merge(df_broad, on=["REF_AREA", "Territorio"]).merge(df_mobi, on=["REF_AREA", "Territorio"])

for col in ["invio_moduli_online", "connessione_fissa", "connessione_mobile"]:
    if df_cluster[col].dtype == object:
        df_cluster[col] = df_cluster[col].str.replace(",", ".").astype(float)
    else:
        df_cluster[col] = df_cluster[col].astype(float)

# Clustering
X = df_cluster[["invio_moduli_online", "connessione_fissa", "connessione_mobile"]]
X_scaled = MinMaxScaler().fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=0)
df_cluster["cluster"] = kmeans.fit_predict(X_scaled)

# Salva tabella descrittiva
df_cluster.to_csv("data/tabella_cluster_macroaree.csv", index=False)

# Crea legenda tabellare come stringa
descrizioni = []
for c in sorted(df_cluster["cluster"].unique()):
    territori = df_cluster[df_cluster["cluster"] == c]["Territorio"].tolist()
    descrizioni.append(f"Cluster {c}: " + ", ".join(territori))
legenda_descrittiva = "\n".join(descrizioni)

# Grafico scatter pulito con legenda estesa
plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=df_cluster,
    x="connessione_fissa",
    y="invio_moduli_online",
    hue="cluster",
    palette="tab10",
    s=100
)
plt.xlabel("Connessione Fissa (%)")
plt.ylabel("Invio Moduli alla PA (%)")
plt.title("Cluster delle macroaree italiane (ISTAT 2024)")
plt.legend(title="Cluster")
plt.figtext(0.01, -0.15, legenda_descrittiva, wrap=True, horizontalalignment='left', fontsize=8)
plt.tight_layout()
plt.savefig("grafici/cluster_macroaree_istat_2024_clean.png", dpi=300)
plt.close()

# Barplot per medie
cluster_means = df_cluster.groupby("cluster")[["invio_moduli_online", "connessione_fissa", "connessione_mobile"]].mean().reset_index()
cluster_melt = cluster_means.melt(id_vars="cluster", var_name="Indicatore", value_name="Valore")

plt.figure(figsize=(10, 7))
sns.barplot(data=cluster_melt, x="Indicatore", y="Valore", hue="cluster", palette="tab10")
plt.title("Media degli indicatori digitali per cluster (ISTAT 2024)")
plt.ylabel("Valore medio (%)")
plt.xlabel("Indicatore")
plt.legend(title="Cluster")
plt.figtext(0.01, -0.15, legenda_descrittiva, wrap=True, horizontalalignment='left', fontsize=8)
plt.tight_layout()
plt.savefig("grafici/cluster_macroaree_barplot_istat_2024.png", dpi=300)
plt.close()
