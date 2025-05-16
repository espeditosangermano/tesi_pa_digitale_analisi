import pandas as pd
import matplotlib.pyplot as plt
import os

# === Percorsi ===
data_dir = "data"
grafici_dir = "grafici"
os.makedirs(grafici_dir, exist_ok=True)

try:
    # === Caricamento file ===
    df_comp = pd.read_csv(os.path.join(data_dir, "clean_competenze_digitali.csv"))
    df_servizi = pd.read_csv(os.path.join(data_dir, "clean_e_government.csv"))
    df_istruzione = pd.read_csv(os.path.join(data_dir, "clean_sdg_istruzione.csv"))
    df_servizi_cittadini = pd.read_csv(os.path.join(data_dir, "clean_indicatori_territoriali.csv"))

    # === Unione indicatori principali ===
    df_comp["Indicatore"] = "I_DSK2_AB"
    df_servizi["Indicatore"] = "I_IGOV12FM"

    df_comp = df_comp.rename(columns={"geo": "Paese", "TIME_PERIOD": "Anno", "OBS_VALUE": "Valore"})
    df_servizi = df_servizi.rename(columns={"geo": "Paese", "TIME_PERIOD": "Anno", "OBS_VALUE": "Valore"})

    df_all = pd.concat([df_comp, df_servizi], ignore_index=True)

    # === Filtra solo i principali paesi europei ===
    paesi_da_confrontare = ["IT", "FR", "DE", "ES"]
    df_all = df_all[df_all["Paese"].isin(paesi_da_confrontare)]

    # === Salvataggio dati consolidati ===
    df_all.to_csv(os.path.join(data_dir, "confronto_digitale_europa.csv"), index=False)

    

    print("✅ File confronto_digitale_europa.csv e grafico salvati.")



    # === Filtra anni dal 2021 al 2024 ===
    df_all = df_all[df_all["Anno"].between(2021, 2024)]

    # === Grafici a barre per ciascun indicatore ===
    for indicatore in df_all["Indicatore"].unique():
        df_indic = df_all[df_all["Indicatore"] == indicatore]
        pivot_df = df_indic.pivot_table(index="Anno", columns="Paese", values="Valore", aggfunc="mean")

        ax = pivot_df.plot(kind="bar", figsize=(10, 6))
        ax.set_title(f"Confronto Europeo (2021–2024) - Indicatore: {indicatore}")
        ax.set_ylabel("Percentuale")
        ax.set_xlabel("Anno")
        ax.legend(title="Paese")
        ax.grid(True, axis="y")
        plt.tight_layout()
        plt.savefig(os.path.join(grafici_dir, f"confronto_barre_{indicatore}.png"))
        plt.close()

    print("✅ File confronto_digitale_europa.csv e grafici a barre salvati.")

except Exception as e:
    print(f"❌ Errore: {e}")
    print(f"❌ Errore: {e}")


    # === Grafici separati per indicatore ===
    for indicatore in df_all["Indicatore"].unique():
        plt.figure(figsize=(10, 6))
        df_indic = df_all[df_all["Indicatore"] == indicatore]
        for paese, group in df_indic.groupby("Paese"):
            plt.plot(group["Anno"], group["Valore"], label=paese, marker="o")

        plt.title(f"Confronto Europeo - Indicatore: {indicatore}")
        plt.xlabel("Anno")
        plt.ylabel("Percentuale")
        plt.grid(True)
        plt.legend(title="Paese", fontsize=8)
        plt.tight_layout()
        plt.savefig(os.path.join(grafici_dir, f"confronto_{indicatore}.png"))
        plt.close()
