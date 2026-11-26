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
- **ESC disattivato** (26/11/2026): non chiude le finestre né fa uscire dalla pagina (si perdeva il lavoro); chiude solo
  menu e ingrandimenti. Le finestre si chiudono con Annulla o Salva.
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
- Tempi dei to-do (`SLA_STEP_DEF`, decisi dal titolare il 25/11/2026; modificabili in Impostazioni › Scadenze dei to-do):
  merce in arrivo **8-9 settimane** ("È arrivata la merce?" 60 gg dall'invio o data di arrivo della conferma);
  **conferma d'ordine da ricevere 5 gg** dall'invio (`CONF_RIC_GG`), poi **verifica 2 gg** (`CONF_VER_GG`, data `o.confIl`);
  **schede di montaggio 3 gg**; **richiesta preventivo di montaggio 2 gg** (`log_prev`), **risposta della squadra 5 gg** (`log_off`);
  **sollecito al cliente per risposta o firma 4 gg** (`SLA_CLIENTE`: passaggi di firma e conferme "Con il cliente"). Il resto 3 gg.

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

### Design Pack per appartamento (B2B, accordo quadro Design Pack, deciso il 26/11/2026)
- Commessa B2B con servizio Leve commerciali e formula **`designpack`** (`isDP`): scheda "Design Pack" (`dpView`).
  Primo uso: operazione di uno sviluppatore con 27 unità, arredi del gruppo IMAB / Pensare Casa (ogni brand il suo sconto).
- Ogni appartamento ha il **suo pack** (`u.dp.righe`: categoria `CAT_DP`, brand, q.tà, listino, sconto d'acquisto dal brand,
  flag "Fissi"); due offerte: **Full pack** (`u.dp.off`) e **Arredi fissi** (`u.dp.offFissi`). Importi **IVA inclusa**,
  trasporto e montaggio compresi, come nel Design Pack presentato (`dpK`).
- **Quota dello sviluppatore** per unità (`u.dpQuota`, 2.000–3.000 €) **+ IVA**: BTWN la fattura allo sviluppatore come
  consulenza commerciale strategica (deciso 26/11/2026). **Al cliente = offerta − quota** (come nell'Excel
  "listino / offerta / offerta al cliente"). Unità, tipologie e quote si incollano dall'Excel (`dpImporta`: codice ·
  tipologia · quota · listino · offerta). L'Excel vero resta al titolare: mai nel repository.
- **Adesione** (`dpAdesione`): acquirente, pack scelto, data adesione e preliminare. Con preliminare + adesione matura il
  corrispettivo: rata allo sviluppatore (`dpUnita`). Nasce la personalizzazione (`p.dp`): righe del pack come "capitolato",
  più la riga "prezzo riservato" (al cliente). Il cliente può togliere arredi (**il valore tolto resta nel conteggio**) e
  cambiarli: paga solo il **differenziale di listino** in più; di base puro differenziale (`scDiff` 0), lo sconto si decide dopo.
- **Logica** (titolare 26/11/2026): commessa = cantiere (es. 27 unità); ogni unità ha codice, quota sviluppatore, il suo
  design pack con gli item e il prezzo per l'acquirente. Quando l'acquirente aderisce l'unità diventa **"B27 · ROSSI MARIO"**
  (`unitaNome`) e parte la sua gestione: personalizzazione, nuove revisioni (rev. 2…) sul suo preventivo.
- **Rate dell'acquirente separate per appartamento** (`rateUnita`, piano "Fornitura privati" 20/40/40): all'accettazione
  della personalizzazione ogni acquirente ha le sue rate, legate all'unità e intestate a lui (`dpCliente`, `dpSlot`).
  Eccezione voluta a "un solo piano per commessa". Una revisione accettata aggiorna le rate non fatturate; se una parte è
  già fatturata la differenza va in "(integrazione)". Le rate dello sviluppatore (quota, forfait) restano a parte.
- **Garanzia minima / forfait** (art. 6.3): interruttore "C'è un forfait" (`c.dpForfaitOn`) e una **frase da completare**
  come nel contratto (`dpFrase`): "Se entro [8] mesi dalla consegna dei materiali ([data]) non ci sono almeno [4] appartamenti
  con preliminare e adesione, lo sviluppatore paga [6.000] € + IVA" + riga "Quindi: scadenza…". Promemoria all'amministratore
  30 giorni prima se la soglia non è raggiunta; scaduto → to-do e "Crea la rata del forfait".

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
- **Preventivo di montaggio** (deciso il 25/11/2026): si chiede alla squadra **solo quando il cliente ha detto sì
  all'offerta arredi senza modifiche** (`accetta`) → primo passaggio della fase Contratto arredi (`log_prev`, entro 2 gg),
  la squadra risponde entro 5 gg (`log_off`, attesa esterna con sollecito), poi offerta con montaggio e firma (`firma` dopo `log_off`).
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
- **Data master del cantiere** (25/11/2026): per i clienti di un cantiere (stessa sigla, `siglaCantiere`) la data in cui è
  rilevabile si registra una volta per tutto il cantiere (`S.rilCantiere[sigla]`, "Vale per: Tutto il cantiere") e scende
  su tutti gli appartamenti, anche quelli creati dopo (`rilDaMaster`). Un appartamento può avere una data propria
  (`c.rilevabile.proprio`, "Solo questo appartamento") e tornare alla data del cantiere. Il to-do "casa rilevabile?"
  non scade prima della data prevista. Primo uso: cantiere Blossom (rilevabile dal 10/01/2027).

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
- Nomi dei documenti (`prefissoDoc`, deciso il 25/11/2026): privato **`COGNOME_TIPO`** (mai la città o la via
  dell'anagrafica); cliente di un cantiere **`SIGLA CANTIERE_UNITÀ_COGNOME_TIPO`** (`c.siglaCantiere`, `c.unitaApt`,
  nella sezione "Cantiere di provenienza" della commessa). B2B: codice commessa_TIPO.
- **Formato cartelle BTWN** (lavori nuovi, deciso il 24/11/2026), in SharePoint › General › LAVORO:
  cartella `VIA E CIVICO_COGNOME CLIENTE` (cantieri: `CANTIERE/APT_COGNOME`), sottocartelle `SP_SOTTO`:
  00_INCARICO · 01_DOCUMENTI CASA · 02_BRIEF · 03_PROGETTO (per brand) · 04_OFFERTA · 05_PRESENTAZIONI ·
  06_VARIANTI (solo con varianti) · 07_RILIEVO · 08_ORDINI (per brand) · 09_MONTAGGIO · 10_AMMINISTRAZIONE · _ARCHIVIO.
- Ogni documento caricato in un passaggio del workflow viene copiato da solo nella sottocartella giusta
  (`cartellaPerTipo` / `CARTELLA_DOC`, `spCopiaDoc`), con il nome standard. I lavori vecchi non si toccano:
  `ALIAS_CARTELLE` riconosce BRIEF, DWG, OFFERTA, CONFERME ORDINE, POST RILIEVO… Dentro Claude il caricamento
  è limitato a 1 MB: i file più grandi si trascinano a mano nella cartella indicata.
- Nell'interfaccia si dice **OneDrive** (non SharePoint): riquadro "Cartella del lavoro (OneDrive)". I file già nella
  cartella si portano nei Documenti con "+ Documenti" (`spDocAgg`: collegamento, nessuna copia, spunta il passaggio del tipo).

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

- Gestione e configurazione della **nuova commessa B2B / cantiere**: Design Pack per appartamento fatto (26/11/2026);
  rate per acquirente fatte. Da capire con l'uso come gestire le revisioni della personalizzazione (rev. 2).
- File messi a mano su OneDrive → riconosciuti dal gestionale per spuntare i passaggi (da fare).
- Pagamenti "una riga per rata": far validare al titolare dopo qualche settimana d'uso.
- Varianti in cantiere (situazione C) da disegnare insieme alla parte B2B.
- Ricaricare nel Team le skill (profilo BTWN, prontuari Lema/Flou/Gervasoni) se non ancora fatto.
- Più avanti, sgancio da Claude
  (vedi `gestionale/SGANCIO-DA-CLAUDE.md`).
