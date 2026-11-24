# BTWN · Bussola – regole del progetto

Gestionale interno di BTWN – Between Contract & Design. Questo file lo legge Claude
all'inizio di ogni sessione: contiene le regole decise con il titolare, così non
dipendono dalla memoria di una singola chat. **Aggiornalo ogni volta che il titolare
dà una regola nuova.**

Si parla in italiano. Il titolare scrive spesso a voce (dettatura): interpreta il senso,
non le parole esatte.

## Struttura del repository

- `gestionale/index.html` – tutta l'app (single page, un solo file: HTML, CSS, JS).
- `gestionale/SGANCIO-DA-CLAUDE.md` – cosa fare quando l'app esce da Claude e va su un sito nostro.
- `gestionale/mappa.html`, `gestionale/mappa-b2c.html` – mappe dei flussi.
- `gestionale/flusso-privato-v2.html` – schema del flusso privato v2 (tronco + binari).
- `gestionale/lib/` – pdf.js. `img/` – immagini.

## ⚠️ Riservatezza

- **Il repository è pubblico.** Mai committare dati veri: clienti, indirizzi, importi di
  commesse reali, mail, telefoni. Nel codice solo dati di esempio inventati.
- Mai mettere email o dati personali del titolare in richieste a servizi esterni.
- Niente identificativi del modello AI nei commit.

## Come si lavora (ciclo di ogni modifica)

Il titolare commenta direttamente sulla pagina (commenti sull'artifact) o scrive in chat.
Per ogni richiesta:

1. Leggi il codice interessato, modifica `gestionale/index.html`
   (per modifiche lunghe: script Python con `replace` controllati, `assert count==1`).
2. **Prova sempre con Playwright** (Chromium preinstallato) prima di pubblicare.
   Dentro Claude `confirm()` e `alert()` non funzionano: nei test forza
   `window.confirm=()=>true` per simulare l'ambiente reale.
3. Commit (con le righe di attribuzione) e push **direttamente su `main`** (deciso dal titolare il 24/11/2026).
4. Pubblica le due versioni dell'artifact:
   - **prova** (dati di esempio, per provare);
   - **ufficiale** (archivio condiviso con il team, capability `db`).
   Si prova prima, si pubblica su entrambe.
5. Rispondi **nel thread del commento** (non in chat); in chat una riga sola.
6. Niente pull request se non richieste.

## Regole decise dal titolare (rispettale sempre)

### Interfaccia
- **Nomi dei clienti sempre in MAIUSCOLO.**
- Le opzioni escluse o non pertinenti sono **in grigio o nascoste**, mai cliccabili a vuoto.
- Dopo un'azione **resta sulla stessa pagina** (usa `render.keepScroll=true`), non saltare altrove.
- Testi semplici, da ufficio, non tecnici. Ogni finestra spiega cosa succede dopo.
- Dentro Claude: **niente `alert`/`confirm`/`prompt`** per decisioni importanti
  (sono disattivati e rispondono sempre "sì"). Usa `openForm(...)` con messaggi nella pagina.
  Download di `.eml`/`.ics` e `fetch` di `data:` URL sono bloccati: usa le alternative già presenti
  (`mailOutlook`, conversione base64 manuale, `scaricaStampa`/`dlPronto`).
  Anche le chiamate a siti esterni sono bloccate (es. ricerca indirizzi OpenStreetMap in `wireIndirizzo`):
  dentro Claude l'indirizzo si scrive a mano e resta il link "Vedi su Google Maps" (Street View da lì).
- L'intestazione della commessa resta visibile scorrendo (sticky, senza sfarfallio).
- Le fasi completate si chiudono (`details.fase-chiusa`); i binari arredi/varianti scorrono separati.

### Workflow
- Il workflow è una **catena rigida di to-do con promemoria**: niente deve essere dimenticato.
- Una fase è **verde solo se tutti i passaggi obbligatori sono fatti**, altrimenti rossa.
  Il contatore conta solo i passaggi obbligatori (flag `1` = facoltativo).
- **Tutte le fasi sono vincolate ai pagamenti**: non si va avanti se la rata collegata non è
  incassata (`pagBlocca`, `puoiAvanzare`, `STEP_PAG`, `TRIG_FASE`).
  **Nessun ordine senza acconto all'ordine incassato** (`okOrdinare` blocca, non chiede).
- Un passaggio di pagamento si spunta solo confermando l'incasso in una finestra esplicita:
  mai segnare rate incassate in automatico.
- Fase 15 "Riordino e ripristino" compare **solo se il verbale ha difetti**.
  Verbale senza difetti → firma → Finito. Dopo Finito le segnalazioni sono **ticket post-vendita**
  (garanzia 24 mesi), la commessa non torna indietro.
- Il capitolato si chiede solo se arriva dal cantiere.

### Pagamenti
- **Un solo piano di rate per commessa** (`rateCommessa`): ogni offerta accettata aggiunge la sua
  quota alle rate esistenti; una nuova revisione della stessa offerta sostituisce la precedente.
  Mai due "Saldo". I doppioni vecchi si uniscono all'avvio (`unisciRateDoppie`).
- La rata Home Book ha trigger `hb` (non `firma`): non deve toccare il contratto arredi.
- **Fatture e verifica incassi vanno all'amministratore** (passaggi `hb_fatt`, `hb_pagato`,
  `var_fatt`, `var_pagato` assegnati via `respStep`); si possono passare a un collega.
- La fee varianti è legata al binario varianti, l'Home Book alla fase Home Book.

### Chi segue la commessa
- **Capo commessa** (`c.capo`): primo contatto con il cliente, fase 1.
- **Binario arredi e Home Book** (`c.respArr`): tutti i to-do delle fasi arredo.
- **Binario varianti** (`c.respVarB`): solo i to-do della gestione varianti.
- Il capo commessa può essere uno dei due operativi. Una singola fase si può assegnare a parte (`c.respFase`).
- Ruoli utente: Amministratore, Collaboratore.

### Offerte, preventivi, ordini
- Al cliente **non si mostra il prezzo per singola voce**.
- Revisioni: l'ordine segue sempre l'**ultima revisione accettata** (`syncOrdini`), una riga per brand,
  i riordini a parte.
- Dopo il rilievo: cruscotto semplice (`#/postrilievo/<id>`), differenziale calcolato dal preventivo,
  non avanti e indietro con il workflow.
- Campo "Oggetto" con menu (cucina, mobile bagno, armadio, tavolo, sedie, madia, mobile TV, letto,
  comodino, scrivania) e testo libero.
- Riordini: Binova dal portale, Lema via mail. Nessuna trattenuta al cliente.

### Verbale di fine lavori
- Squadre con smartphone: pagina verbale digitale con foto; anche versione cartacea.
- "Nessun difetto" è sempre possibile.
- Due parti separate: **chi compila** (Squadra di montaggio / BTWN / Cliente + nome) e
  **chi firma per accettazione** (Cliente / Impresa / Proprietà + nome + firma).
- Al cliente resta la copia firmata.

### Varianti
- Modifiche del cliente tra invio e firma: ping-pong di conferme ("Con il cliente").
- Coordinamento con il cantiere prima della verifica; difformità dopo la verifica, con ticket
  al cantiere (scheda Difformità: aggiungi/modifica/elimina). "Cantiere ha sistemato" non si spunta
  se ci sono difformità aperte.

### Flusso privato v2 (in uso dal 24/11/2026; schema in `gestionale/flusso-privato-v2.html`)
- Nel codice: fasi `contatto`, `homebook` (= Incarico BTWN), `dwg` (= Documenti della casa) sono il
  **tronco** (`TRONCO`); punti d'incontro in `INCONTRI` (+ `c.insieme`); fonte documenti `c.docFonte`;
  righe di pagamento = `STEP_PAG` (`hb_pagato` copre rate `hb` e `varianti`), dettaglio in `stepExtra`.
  Migrazione delle commesse vecchie con `c.wfp4` (le nuove nascono con `wfp2/wfp3/wfp4`).
- **Tronco comune** (capo commessa): primo contatto → **incarico unico** (un contratto con i servizi
  scelti: Home Book, varianti o entrambi; una fattura con le righe; se una parte la paga un altro,
  fattura separata a lui) → **documenti della casa richiesti una volta sola**.
- **DWG nel privato**: spesso non c'è sviluppatore né impresa. Fonte da scegliere: cliente, architetto
  del cliente, impresa, studio di progettazione, oppure **non esiste → rilievo dello stato di fatto**.
- **Punti d'incontro flessibili** (brief, presentazione, sopralluogo): insieme di default se entrambi
  i binari sono attivi, ma sempre separabili. Mai rigidi.
- Lo schema impianti dipende dal layout arredo, ma alcune richieste sono sganciate (es. presa
  aspirapolvere): **avviso, non blocco**.
- **Responsabili**: ognuno fa il suo binario (non tutto al capo commessa); assegnazione automatica
  per binario, sempre modificabile anche per singolo passaggio.
- **Preventivo di montaggio**: richiesto a fine rev. 1 a squadra esterna, risponde in 3–6 giorni →
  attesa esterna con sollecito, non blocca il resto; serve prima della firma del contratto arredi.
- I controlli automatici restano visibili: non perdere mai il controllo della commessa.
- Pagamenti come **una riga per rata**: da provare e far validare al titolare.
- **Varianti, tre situazioni**: A privato senza cantiere (paga il cliente); B cliente in un cantiere
  (paga cliente o sviluppatore); C cantiere con accordo quadro (impianti elettrico/idrico, architettonico = modifica pareti,
  finiture di capitolato: pavimenti, rivestimenti, sanitari, rubinetterie; extra capitolato: rubinetterie
  o pavimenti diversi/superiori, pagatore cliente/sviluppatore/ripartito, eventuale fee proprietà per monitoraggio
  cantiere) → **C va disegnata a parte**, con la parte B2B.

### Rilievo
- Si fa solo quando la casa è **rilevabile**: lo conferma l'impresa o l'architetto del cliente (a volte il
  cliente o la direzione lavori). Passaggio `ril_pronto` + riquadro "Casa rilevabile" (`c.rilevabile`:
  chi, referente, data, confermata, sollecito, storico). Finché non è confermato c'è un to-do di sollecito;
  "Rispondi al cliente" prepara la mail su quando si fa il rilievo. Con le varianti e il sopralluogo
  insieme, "cantiere pronto" (`var_pronto`) e casa rilevabile si spuntano a vicenda.

### Banca
- Estratto conto (PDF Banco BPM o CSV dell'home banking) caricato in **Economia** → `movimentiDaTesto` /
  `movimentiDaCsv` → `candidatiRata` (importo con/senza IVA o totale fattura, nome cliente, n. fattura) →
  `formBanca`: **propone, l'amministratore conferma** (mai incassi automatici). Movimenti in `S.banca`
  (abbinato / ignorato / da abbinare). Mai committare estratti conto o dati bancari veri.

### Fatture (Fattura SMART – Wolters Kluwer, sme.genya.it)
- Nessuna API pubblica: si caricano in **Economia → Fatture emesse → "Da Fattura SMART"** gli XML FatturaPA
  (anche firmati `.p7m`), l'export Excel/CSV (con lo stato SdI) → `caricaFattureSmart` → `formFattureSmart`.
- Emesse (`S.fatture`, cedente = P.IVA BTWN): cliente per CF/P.IVA (`clienteDaFattura`), rata proposta
  (`rateCandFatt`); confermando la rata passa a Fatturata con numero/data/`fatturaId`. Stato SdI scartata/
  mancata consegna/rifiutata → to-do all'amministratore (`avvisiSdi`).
- Ricevute (`S.fattureRic`): fornitore per P.IVA/nome, collegate a ordine o commessa (`ordiniCandFatt`);
  il costo reale entra in `costiCommessa`; se diverso dalla conferma d'ordine → to-do di verifica.
- **Verificato:** Fattura SMART NON accetta XML di fatture attive da inviare (l'import XML è solo storico,
  non va allo SdI). Quindi "Dati fattura" sulla rata (`formFatturaXml`) prepara i dati da copiare in
  Fattura SMART (Nuova fattura); l'XML si scarica solo come archivio. Fattura SMART importa anche
  anagrafiche clienti/fornitori/prodotti. Dentro il programma non c'è un canale per l'assistenza:
  la richiesta API a Wolters Kluwer va via mail (bozza in Outlook).
- Sempre: propone, l'amministratore conferma. Mai fatture vere nel repository (test con XML sintetici).

### To-do ripetuti
- "+ To-do" → "Ripeti" ogni settimana (giorno) o ogni mese (1-28); modelli in `S.ricorrenti`, generati da
  `generaRicorrenti` all'apertura e nel promemoria del mattino (un to-do per occorrenza, `ricId`+`dataRic`).
  Gestione da "↻ Ripetuti" nella lista to-do. Di base (`S.ricDefault`): ogni **lunedì** all'amministratore
  "carica l'Excel delle fatture da Fattura SMART" e "carica il CSV della banca".

### File e cartelle
- Contratto del tronco: tipo documento **CONTRATTO INCARICO** (firmato: CONTRATTO INCARICO FIRMATO); comprende i servizi scelti.
- Nomi dei documenti: `CANTIERE_APT_CLIENTE_DOC`.
- **Formato cartelle BTWN** (lavori nuovi, deciso il 24/11/2026), in SharePoint › General › LAVORO:
  cartella `VIA E CIVICO_COGNOME CLIENTE` (cantieri: `CANTIERE/APT_COGNOME`), sottocartelle `SP_SOTTO`:
  00_INCARICO · 01_DOCUMENTI CASA · 02_BRIEF · 03_PROGETTO (per brand) · 04_OFFERTA · 05_PRESENTAZIONI ·
  06_VARIANTI (solo con varianti) · 07_RILIEVO · 08_ORDINI (per brand) · 09_MONTAGGIO · 10_AMMINISTRAZIONE · _ARCHIVIO.
- Ogni documento caricato in un passaggio del workflow viene copiato da solo nella sottocartella giusta
  (`cartellaPerTipo` / `CARTELLA_DOC`, `spCopiaDoc`), con il nome standard. I lavori vecchi non si toccano:
  `ALIAS_CARTELLE` riconosce BRIEF, DWG, OFFERTA, CONFERME ORDINE, POST RILIEVO… Dentro Claude il caricamento
  è limitato a 1 MB: i file più grandi si trascinano a mano nella cartella indicata.

## Pubblicare il gestionale in un nuovo account (es. Claude Team BTWN)

1. Nell'account vecchio, dalla versione **ufficiale**: "Esporta backup" (file JSON, resta al titolare: mai nel repo).
2. `python3 gestionale/tools/build_artifact.py <cartella>` → crea `ufficiale/index.html` e `prova/index.html`
   (pdf.js incorporato, immagini, nessun dato).
3. Pubblica `ufficiale/index.html` (+ `img/`) come artifact "BTWN · Bussola – ufficiale" e dichiara le capability:
   - `db` con regola `{path:"", read:"interact", write:"interact"}` (archivio condiviso del team);
   - connettori **Microsoft 365** (outlook_create_draft, outlook_send_mail, outlook_email_search,
     outlook_create_event, outlook_calendar_search, get_me, read_resource, sharepoint_folder_search,
     sharepoint_create_folder, sharepoint_upload_file) e **Fireflies** (fireflies_get_transcripts);
   - download di file.
   Poi la versione **prova** allo stesso modo, senza `db`.
4. Il titolare apre l'ufficiale, fa "Importa backup" e la condivide con l'organizzazione (lo fa lui dal menu
   di condivisione). Ognuno collega il proprio Microsoft 365 in Impostazioni → Connettori.
5. Ricaricare nel nuovo account le skill (profilo BTWN, prontuari Lema/Flou/Gervasoni).

## Architettura (riferimento rapido)

- Stato globale `S` in `localStorage` (`btwn-bussola-v1`); file in IndexedDB (`putFile`, mappa `FILES`).
  Versione ufficiale: dati nell'archivio condiviso `claude.use('db')` (`cloudAvvio`).
- Migrazioni dati in `load()`: devono essere idempotenti (girano a ogni apertura).
- Form: `openForm({title,intro,fields,values,okLabel,onSave})`; campo HTML libero = `{type:'html',html:...}`.
- Azioni: mappa `A{}` con `data-act`; i cambi con `data-change`. Nei dialog i click `data-act` sono
  ignorati: usa listener diretti.
- Workflow privato `WF_PRIVATO` (contatto, homebook, dwg, raccolta, progettazione, presentazione,
  esito, firma, impianti, rilievo, ordine, magazzino, consegna, verbale, ripristino, finito) +
  binario `WF_VAR_PRIV` (id `varianti`). B2B: `WF_B2B` (fasi `op_*`), servizi: `WF_SERVIZIO` (`sv_*`).
- Passaggi: `wfSteps`, `STEP_DOPO` (catena), `STEP_AZIONE` (pulsante), `STEP_PAG`, `STEP_DOC`,
  `autoPassi` (spunte automatiche da rate, documenti, ordini), `avanzaAuto`.
- Microsoft 365 (Outlook, calendario, Teams, SharePoint) e Fireflies via connettori di Claude (`m365(...)`).

## Dove vive il gestionale (dal 24/11/2026)

- Il gestionale in uso è nell'account **Claude Team "Btwn"**: artifact "BTWN · Bussola – ufficiale" (archivio
  condiviso, Matteo e Alberto come Contributori) e "BTWN · Bussola – prova", pubblicati dalla sessione Team.
  Le modifiche si pubblicano **lì**. I vecchi artifact dell'account personale non si usano più.
- Importati nel Team: rubrica clienti (anche The Green One) e parametri/sconti dei brand. Le commesse si
  ricreano a mano. Cartella dei lavori collegata: SharePoint › General › LAVORO.
- Sessione "Programma delle fatture" (sul Mac del titolare, browser): ha esplorato Fattura SMART
  (vedi sezione Fatture). Struttura export Excel ridotto: intestazioni in riga 4, 20 colonne
  (Numero, Suffisso, Anno, Data, Tipo Documento, Soggetto, Codice Fiscale, Partita IVA, Imponibile, …,
  Totale, Ritenuta, Netto a pagare, Note piede, Stato, Stato esito).

## Da fare (prossimi passi)

- **Fattura SMART**: richiesta API/integrazione inviata al commercialista il 24/11/2026 (da girare a
  Wolters Kluwer). In attesa di risposta: se c'è un accesso, collegamento automatico dopo lo sgancio.

- Gestione e configurazione della **nuova commessa B2B / cantiere** (ancora da completare).
- File messi a mano su OneDrive → riconosciuti dal gestionale per spuntare i passaggi (da fare).
- Pagamenti "una riga per rata": far validare al titolare dopo qualche settimana d'uso.
- Varianti in cantiere (situazione C) da disegnare insieme alla parte B2B.
- Ricaricare nel Team le skill (profilo BTWN, prontuari Lema/Flou/Gervasoni) se non ancora fatto.
- Più avanti, sgancio da Claude
  (vedi `gestionale/SGANCIO-DA-CLAUDE.md`).
