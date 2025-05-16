from fpdf import FPDF
import os
import unicodedata

def latinize(text):
    text = unicodedata.normalize("NFKD", text)
    return text.encode("latin-1", "ignore").decode("latin-1")

testo_descrittivo = """Nel contesto della trasformazione digitale della Pubblica Amministrazione italiana, i dati analizzati evidenziano progressi significativi ma anche criticità da affrontare.

L'accesso ai servizi pubblici digitali da parte dei cittadini è in crescita, come mostra il grafico sottostante. Tuttavia, il gap tra le regioni resta marcato, con alcune aree che mostrano ancora bassa adozione tecnologica.

Il Programma PNRR ha raggiunto una copertura pressoché totale, con la quasi totalità dei comuni italiani coinvolti in almeno una misura di digitalizzazione.

A livello europeo, il confronto tra Italia, Francia, Germania e Spagna evidenzia una posizione arretrata per l’Italia, sia sul fronte delle competenze digitali di base che nell'utilizzo dei servizi pubblici online.

Anche la classificazione delle regioni italiane in termini di digitalizzazione mostra un divario significativo tra Nord e Sud, con la Lombardia e il Piemonte tra le regioni più avanzate.

"""

testo_predizione = """Secondo le analisi predittive effettuate, la crescita delle competenze digitali in Italia procede a un ritmo troppo lento per consentire il raggiungimento del target europeo dell'80% entro il 2030.

I dati reali degli ultimi anni indicano che l’Italia si attesta intorno al 45-46% della popolazione con competenze digitali di base. Il modello previsionale, basato su regressione lineare, proietta il raggiungimento del target solo intorno all’anno 2365, evidenziando una grave discrepanza rispetto agli obiettivi dell’agenda digitale europea.

Pertanto, appare urgente implementare politiche mirate e interventi strutturali per:
- accelerare la diffusione delle competenze digitali tra giovani, adulti e lavoratori,
- rafforzare l'accesso alla formazione continua,
- collegare i finanziamenti del PNRR a indicatori di impatto reali sulla popolazione.

Segue il grafico con la proiezione temporale della traiettoria italiana verso il target UE del 2030.
"""

grafici = [
    "grafici/accesso_servizi_digitali.png",
    "grafici/adozione_pnrr_regioni.png",
    "grafici/confronto_barre_I_DSK2_AB.png",
    "grafici/confronto_barre_I_IGOV12FM.png",
    "grafici/distribuzione_classi_adozione.png",
    "grafici/indice_digitalizzazione_regioni.png",
    "grafici/indice_digitalizzazione_zone.png",
    "grafici/target_competenze_digitali.png",
    "grafici/previsione_target_80.png"
]

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Analisi Finale Digitalizzazione PA Italiana", ln=True, align='C')
pdf.ln(8)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 8, latinize(testo_descrittivo + testo_predizione))

for g in grafici:
    if os.path.exists(g):
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Figura: " + os.path.basename(g).replace("_", " ").replace(".png", "").capitalize(), ln=True)
        pdf.image(g, x=25, y=30, w=160)

pdf.output("report_digitalizzazione_con_previsioni.pdf")
print("✅ Report PDF generato: report_digitalizzazione_con_previsioni.pdf")
