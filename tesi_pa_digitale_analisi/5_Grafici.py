import matplotlib.pyplot as plt



# === GRAFICO: Competenze Digitali - Italia vs Target UE ===
plt.figure(figsize=(10, 6))
plt.plot([2021, 2023], [45.0, 45.0], marker='o', color='blue', label="Italia", linewidth=2)
plt.axhline(y=80, color='red', linestyle='--', label="Target UE 2030 (80%)")
plt.xticks([2021, 2023])
plt.yticks(range(0, 101, 10))
plt.ylim(0, 100)
plt.title("📊 Competenze Digitali - Italia vs Target UE 80%")
plt.xlabel("Anno")
plt.ylabel("Percentuale")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafici/target_competenze_digitali.png")
plt.close()

# === GRAFICO: Accesso ai Servizi Pubblici Digitali - Italia ===
anni_servizi = [2014, 2016, 2018, 2020, 2022]
italia_servizi = [45, 50, 55, 60, 68]  # valori stimati o da CSV originali

plt.figure(figsize=(10, 6))
plt.plot(anni_servizi, italia_servizi, marker='o', color='green', label="Italia - Servizi PA digitali", linewidth=2)
plt.xticks(anni_servizi)
plt.yticks(range(0, 101, 10))
plt.ylim(0, 100)
plt.title("📊 Accesso ai Servizi Pubblici Digitali (Italia)")
plt.xlabel("Anno")
plt.ylabel("Percentuale di cittadini")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("grafici/accesso_servizi_digitali.png")
plt.close()
