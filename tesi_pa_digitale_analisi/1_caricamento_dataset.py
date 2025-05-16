import pandas as pd
import csv
import os

# Percorso base per input/output
BASE_DIR = "data"

def rileva_delimitatore(file_path, encoding='utf-8'):
    with open(file_path, encoding=encoding) as f:
        sample = f.read(2048)
        return csv.Sniffer().sniff(sample).delimiter

def salva_csv_pulito(nome_file_input, nome_file_output, encoding='utf-8'):
    try:
        percorso_input = os.path.join(BASE_DIR, nome_file_input)
        percorso_output = os.path.join(BASE_DIR, nome_file_output)
        sep = rileva_delimitatore(percorso_input, encoding)
        df = pd.read_csv(percorso_input, sep=sep, encoding=encoding, on_bad_lines='skip')
        df.columns = df.columns.str.strip()
        df.to_csv(percorso_output, index=False)
        print(f"✅ Salvato: {percorso_output} - Righe: {len(df)}, Colonne: {len(df.columns)} - Delimitatore: '{sep}'")
    except Exception as e:
        print(f"❌ Errore su {nome_file_input}: {e}")

# === Dataset da pulire ===
salva_csv_pulito("candidature_comuni_finanziate.csv", "clean_comuni_finanziati.csv")
salva_csv_pulito("Elenco-comuni-italiani.csv", "clean_elenco_comuni.csv", encoding='latin-1')
salva_csv_pulito("isoc_sk_dskl_i21.csv", "clean_competenze_digitali.csv")
salva_csv_pulito("isoc_ciegi_ac.csv", "clean_e_government.csv")
salva_csv_pulito("PC - reg. e tipo di comune (IT1,83_63_DF_DCCV_AVQ_PERSONE_243,1.0).csv", "clean_uso_pc.csv")
salva_csv_pulito("sdg_04_70.csv", "clean_sdg_istruzione.csv")
salva_csv_pulito("tepsr_sp410.csv", "clean_indicatori_territoriali.csv")

print("✅ Tutti i dataset sono stati puliti e salvati nella cartella /data.")
