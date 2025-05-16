import os
import subprocess
import webbrowser
import platform

# Determina il comando corretto da usare: 'python' su Windows, 'python3' altrove
python_cmd = "python" if platform.system() == "Windows" else "python3"

moduli = [
    "1_caricamento_dataset.py",
    "2_adozione_pnrr.py",
    "3_correlazione_digitale.py",
    "4_confronto_europeo.py",
    "5_Grafici.py",
    "6_modelli_predittivi.py",
    "8_report_automatico.py"
]

print("🚀 Avvio dei moduli di analisi...\n")

for script in moduli:
    print(f"▶️ Eseguo: {script}")
    subprocess.run([python_cmd, script])

print("\n📄 Report PDF generato.")
print("🌐 Avvio della dashboard Streamlit...")

# Avvio della dashboard
subprocess.Popen([python_cmd, "-m", "streamlit", "run", "app_dashboard_digitalizzazione.py"])
webbrowser.open("http://localhost:8501")
