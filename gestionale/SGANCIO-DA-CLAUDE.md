# Promemoria: quando il gestionale si sgancia da Claude (Strada B)

Oggi il gestionale gira come pagina dentro Claude e usa i servizi di Claude
(archivio condiviso, collegamento Microsoft 365). Quando lo porteremo su un sito
nostro con un'app registrata nel Microsoft 365 aziendale, ricordarsi di:

## Mail (priorità)
- **Allegati veri nelle mail**: il connettore Microsoft 365 di Claude non può
  allegare file (né in invio diretto né inviando una bozza). Oggi con allegati il
  gestionale crea solo la bozza in Outlook e l'utente trascina il file.
  Con Microsoft Graph diretto (`/me/sendMail` con `attachments`, o upload session
  per file > 3 MB) la mail deve partire subito con l'allegato: scegli il file,
  destinatario, Invia.
- Firma Outlook: le bozze create via Graph non hanno la firma, aggiungerla dal
  profilo utente.
- Lettura delle risposte dei clienti e dei fornitori (mail collegate alle
  commesse, conferme d'ordine allegate lette in automatico).

## File e SharePoint
- Upload dal gestionale oggi limitato a 1 MB: con Graph usare le upload session
  (file grandi: presentazioni, DWG).
- Link condivisibili per i clienti esterni (`createLink`), oggi non disponibili.
- Riconoscimento automatico dei documenti nelle cartelle del lavoro per spuntare
  i passaggi del workflow.

## Dati
- Esportare tutto l'archivio condiviso (commesse, clienti, preventivi, ordini,
  rate, to-do) e importarlo nel nuovo database.
- Accesso con l'account Microsoft aziendale (niente account Claude per i colleghi).

## Comportamenti da ripristinare fuori da Claude
- Finestre di conferma ("Sei sicuro?") prima delle eliminazioni: dentro Claude
  sono disattivate.
- Download di file .eml e .ics (mail per Outlook, appuntamenti), oggi bloccati
  dentro Claude.
- Calendario Outlook: appuntamenti del gestionale scritti direttamente nel
  calendario.
