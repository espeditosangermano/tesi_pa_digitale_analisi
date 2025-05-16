
import pandas as pd
import matplotlib.pyplot as plt
import os

# === Percorsi ===
data_dir = "data"
os.makedirs("grafici", exist_ok=True)

try:
    # === Caricamento dati principali ===
    df_fin = pd.read_csv(os.path.join(data_dir, "clean_comuni_finanziati.csv"), dtype=str)
    df_comp = pd.read_csv(os.path.join(data_dir, "clean_competenze_digitali.csv"))
    df_serv = pd.read_csv(os.path.join(data_dir, "clean_e_government.csv"))
    df_pc = pd.read_csv(os.path.join(data_dir, "clean_uso_pc.csv"))
    df_candidature = pd.read_csv(os.path.join(data_dir, "candidature_comuni_finanziate.csv"))

    # === Adozione PNRR per Regione ===
    df_fin["Codice Regione"] = df_fin["cod_regione"]
    df_fin["Regione"] = df_fin["regione"]
    df_pc = df_pc.rename(columns={"Territorio": "Regione"})

    df = df_fin.groupby("Regione").agg({"comune": "count"}).rename(columns={"comune": "Totale Comuni"})
    df["Comuni Finanziati"] = df_fin[df_fin["importo_finanziamento"].astype(float) > 0].groupby("Regione")["comune"].count()
    df["Percentuale Adozione"] = (df["Comuni Finanziati"] / df["Totale Comuni"]) * 100
    df = df.reset_index()
    df["Classe_Adozione"] = pd.cut(df["Percentuale Adozione"], bins=[0, 40, 70, 100],
                                   labels=["Bassa", "Media", "Alta"], include_lowest=True)

    # === Competenze e Servizi digitali: media nazionale fissa ===
    df["Competenze Digitali"] = 45
    df["Uso Servizi Digitali"] = 55

    # === Candidature identità digitale ===
    df_candidature["avviso"] = df_candidature["avviso"].astype(str)
    df_id = df_candidature[df_candidature["avviso"].str.contains("1.4.1|1.4.3|1.4.4", regex=True)]
    df_id_count = df_id.groupby("regione").size().reset_index(name="Candidature Identità Digitale")
    df_id_count = df_id_count.rename(columns={"regione": "Regione"})

    df_finale = df.merge(df_id_count, on="Regione", how="left")
    df_finale["Candidature Identità Digitale"] = df_finale["Candidature Identità Digitale"].fillna(0).astype(int)

    # === Calcolo indice aggregato e classe digitale ===
    df_finale["Indice Digitale Medio"] = (
        df_finale["Competenze Digitali"] +
        df_finale["Uso Servizi Digitali"] +
        df_finale["Candidature Identità Digitale"].apply(lambda x: min(x / 100, 100))
    ) / 3

    df_finale["Classe_Digitalizzazione"] = pd.cut(
        df_finale["Indice Digitale Medio"],
        bins=[0, 40, 70, 100],
        labels=["Bassa", "Media", "Alta"],
        include_lowest=True
    )

    # === Zona geografica ===
    nord = ["Piemonte", "Valle d'Aosta/Vallée d'Aoste", "Lombardia", "Trentino-Alto Adige/Südtirol", 
            "Veneto", "Friuli-Venezia Giulia", "Liguria", "Emilia-Romagna"]
    centro = ["Toscana", "Umbria", "Marche", "Lazio"]
    sud = ["Abruzzo", "Molise", "Campania", "Puglia", "Basilicata", "Calabria", "Sicilia", "Sardegna"]

    def zona(regione):
        if regione in nord:
            return "Nord"
        elif regione in centro:
            return "Centro"
        elif regione in sud:
            return "Sud"
        return "Altro"

    df_finale["Zona"] = df_finale["Regione"].apply(zona)

    # === Salvataggio dati ===
    df_finale.to_csv(os.path.join(data_dir, "correlazione_digitale_pnrr.csv"), index=False)
    print("✅ Correlazione digitale estesa salvata in /data")

    # === Grafico 1: Distribuzione Classi Adozione ===
    if "Classe_Adozione" in df_finale.columns:
        classe_counts = df_finale["Classe_Adozione"].value_counts()
        if not classe_counts.empty:
            plt.figure(figsize=(6, 5))
            classe_counts = classe_counts.reindex(["Bassa", "Media", "Alta"])
            classe_counts.plot(kind="bar", color="skyblue")
            plt.title("Distribuzione Classi di Adozione Digitale")
            plt.xlabel("Classe")
            plt.ylabel("Numero di Regioni")
            plt.tight_layout()
            plt.savefig("grafici/distribuzione_classi_adozione.png")
            plt.close()

    # === Grafico 2: Indice Digitalizzazione per Regione ===
    df_sorted = df_finale.sort_values("Indice Digitale Medio", ascending=False)
    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted["Regione"], df_sorted["Indice Digitale Medio"], color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Indice Digitale Medio")
    plt.title("Indice di Digitalizzazione per Regione")
    plt.tight_layout()
    plt.savefig("grafici/indice_digitalizzazione_regioni.png")
    plt.close()

    # === Grafico 3: Indice Digitalizzazione per Zona ===
    df_zona = df_finale.groupby("Zona")["Indice Digitale Medio"].mean().reindex(["Nord", "Centro", "Sud"])
    plt.figure(figsize=(6, 5))
    df_zona.plot(kind="bar", color="coral")
    plt.title("Indice di Digitalizzazione per Zona")
    plt.ylabel("Indice Medio")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("grafici/indice_digitalizzazione_zone.png")
    plt.close()

except Exception as e:
    print(f"❌ Errore: {e}")
