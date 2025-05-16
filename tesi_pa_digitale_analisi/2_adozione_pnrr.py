
import pandas as pd
import matplotlib.pyplot as plt
import os

data_dir = "data"
grafici_dir = "grafici"
os.makedirs(data_dir, exist_ok=True)
os.makedirs(grafici_dir, exist_ok=True)

try:
    # === Carica elenco comuni ISTAT ===
    df_elenco = pd.read_csv(os.path.join(data_dir, "Elenco-comuni-italiani.csv"), encoding="latin1", sep=";")
    df_elenco["cod_comune"] = df_elenco["Codice Comune formato numerico"].astype(str).str.zfill(6)

    # === Carica candidature finanziate ===
    df_candidature = pd.read_csv(os.path.join(data_dir, "candidature_comuni_finanziate.csv"))
    df_candidature["cod_comune"] = df_candidature["cod_comune"].astype(str).str.zfill(6)
    df_candidature["importo_finanziamento"] = pd.to_numeric(df_candidature["importo_finanziamento"], errors="coerce")
    df_candidature_filtrate = df_candidature[df_candidature["importo_finanziamento"] > 0]

    # === Conteggio comuni totali per regione ===
    df_comuni_totali = df_elenco.groupby("Denominazione Regione")["cod_comune"].nunique().reset_index()
    df_comuni_totali.columns = ["Denominazione Regione", "Totale_Comuni"]

    # === Conteggio comuni finanziati univoci ===
    df_finanziati_unici = df_candidature_filtrate.drop_duplicates(subset=["cod_comune"])
    df_finanziati_count = df_finanziati_unici.groupby("regione")["cod_comune"].nunique().reset_index()
    df_finanziati_count.columns = ["Denominazione Regione", "Comuni_Finanziati"]

    # === Merge e calcolo percentuali ===
    df_finale = df_comuni_totali.merge(df_finanziati_count, on="Denominazione Regione", how="left")
    df_finale["Comuni_Finanziati"] = df_finale["Comuni_Finanziati"].fillna(0).astype(int)
    df_finale["Percentuale_Adozione"] = (df_finale["Comuni_Finanziati"] / df_finale["Totale_Comuni"]) * 100
    df_finale["Percentuale_Adozione"] = df_finale["Percentuale_Adozione"].clip(upper=100)

    # === Salva file CSV ===
    df_finale.to_csv(os.path.join(data_dir, "adozione_pnrr_regioni.csv"), index=False)

    # === Genera grafico ===
    df_sorted = df_finale.sort_values("Percentuale_Adozione", ascending=False)
    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted["Denominazione Regione"], df_sorted["Percentuale_Adozione"], color="steelblue")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Percentuale Comuni Finanziati (%)")
    plt.title("Adozione PNRR per Regione (Comuni Finanziati su Totale)")
    plt.tight_layout()
    plt.savefig(os.path.join(grafici_dir, "adozione_pnrr_regioni.png"))
    plt.close()

    print("✅ File CSV e grafico salvati correttamente in /data e /grafici")

except Exception as e:
    print(f"❌ Errore: {e}")
