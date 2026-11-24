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
- `gestionale/flusso-privato-v2.html` – proposta di flusso privato semplificato (da validare).
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
3. Commit (con le righe di attribuzione) e push sul branch di lavoro.
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

### Flusso privato v2 (decisioni del titolare, proposta in `gestionale/flusso-privato-v2.html`)
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
  (paga cliente o sviluppatore); C cantiere con accordo quadro (impianti + finiture di capitolato ed
  extra capitolato, pagatore cliente/sviluppatore/ripartito, eventuale fee proprietà per monitoraggio
  cantiere) → **C va disegnata a parte**, con la parte B2B.

### File e cartelle
- Nomi dei documenti: `CANTIERE_APT_CLIENTE_DOC`.
- Cartella SharePoint/OneDrive della commessa con sottocartelle: BRIEF, DWG, OFFERTA, PRESENTAZIONI,
  CONFERME ORDINE, MONTAGGIO, POST RILIEVO (+ VARIANTI). Dentro Claude il caricamento verso
  SharePoint è limitato a 1 MB.

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

## Da fare (prossimi passi)

- Gestione e configurazione della **nuova commessa B2B / cantiere** (ancora da completare).
- File caricati nel gestionale → automaticamente nella sottocartella SharePoint giusta
  (proposte nuove cartelle CONTRATTI e AMMINISTRAZIONE: da confermare).
- Passaggio a Claude Team (account aziendale) e, più avanti, sgancio da Claude
  (vedi `gestionale/SGANCIO-DA-CLAUDE.md`).
