# Servizio DCBR — AI Clone Video (storyline-first)

Video in cui recita il **clone AI del cliente**: il founder non deve più registrare, il team DCBR produce i contenuti al posto suo.

Nell'app il servizio è l'agente **#17 🎥 AI Clone Video Director** (`route.ts`). Gira nella modalità completa, dopo Script & Storyboard e Visual Producer, e consegna per ogni cliente: concept, script, subject map, reference map con nomi file, storyline da regista, piano delle generazioni, prompt Seedance 2.5 pronti da incollare, brief delle Character Sheet e checklist QC. Questo documento spiega al team come trasformare quell'output nel video finale.

---

## 1. Il principio

Il vecchio metodo era **image-first**: ogni inquadratura richiedeva un'immagine generata a mano, poi animata, poi montata. Con 20–30 immagini per video aumentavano gli errori: volti che cambiano, stanze che cambiano architettura, oggetti che cambiano dimensione. Il montaggio finiva per tenere insieme pezzi nati frammentati.

Il nuovo metodo è **storyline-first**: l'unità di lavoro non è più l'immagine ma la **scena diretta**, supportata da poche reference controllate. Seedance costruisce la sequenza (azioni, cambi d'angolo, tagli) dentro un'unica generazione.

## 2. La pipeline

| # | Livello | Cosa produce | Chi |
|---|---------|--------------|-----|
| 1 | Idea | Scopo di business + idea in una frase (situazione → trasformazione) | Account + agente 17 |
| 2 | Script | Battute / voiceover con tempi | Agente 14 + agente 17 |
| 3 | Storyline | Cosa si vede: azioni, emozioni, luoghi, oggetti, camera | Agente 17, approvata dal team |
| 4 | Reference | Character Sheet, location, oggetti numerati | Team (GPT Image 2.5) |
| 5 | Traduzione | Prompt Seedance strutturato | Agente 17 / Claude |
| 6 | Generazione | Clip da max 30 s | Team (Seedance 2.5 su Higgsfield) |
| 7 | Montaggio | Clip + audio + sottotitoli | Editor |

**Regola:** non si passa al livello successivo finché il precedente non è stabile. Generare mentre la storia cambia ancora significa buttare lavoro.

## 3. Cosa chiedere al cliente

- 3–5 foto nitide del volto (frontale, ¾, profilo), luce uniforme, niente filtri.
- 1 foto a figura intera per le proporzioni.
- Outfit ricorrenti (foto dei capi o riferimenti).
- Luoghi reali da riprodurre (ufficio, negozio), solo se il pubblico deve riconoscerli.
- Prodotti / oggetti di brand da tenere identici.
- Script o messaggi chiave, se esistono già.

## 4. Scrivere la storyline

Ogni storyline deve rispondere a sette domande: **chi** c'è, **cosa fa** ognuno, **come si sente**, **dove** succede, **quali oggetti** contano, **cosa fa la camera**, **come progredisce** la scena dall'inizio alla fine.

- **Verbi visibili, non concetti.** ✗ "Si rende conto di non avere tempo." ✓ "L'assistente gli porge il telefono; lui lo guarda, scuote la testa, lo spinge indietro e torna al laptop."
- **Movimento + atteggiamento + intensità.** "Si allunga verso la sveglia, lento e irritato; stanco ma realistico, non teatrale."
- **Interazioni con un ordine preciso:** chi inizia, come risponde l'altro.
- **Camera solo quando serve:** statica, zoom rapido, leggero shake, hard cut, tracking, cambio d'angolo.
- **Test di approvazione:** un estraneo che legge la storyline deve vedere il video inquadratura per inquadratura.

## 5. Le reference: controlla ciò che conta

**La domanda decisiva:** *il video sarebbe peggiore se l'AI cambiasse questo elemento?* Sì → reference. No → descrivilo e basta.

| Elemento | Quando si referenzia | Esempio |
|----------|----------------------|---------|
| Soggetto principale | Sempre, **una Character Sheet per ogni outfit/stato** | Founder in pigiama, founder in giacca |
| Soggetto secondario | Se ricorre o ha un ruolo narrativo | Assistente |
| Comparsa | Mai, si descrive | Moglie che dorme, volto non visibile |
| Location | Un'immagine se basta un angolo; Location Sheet multi-vista se la camera esplora lo spazio | Camera da letto vista da letto, porta e lato |
| Oggetto | Se causa l'azione, ricorre o è di brand | Sveglia, dossier, prodotto |
| Oggetto generico | Mai | Bicchiere d'acqua |

### Character Sheet

1. Foto sorgente nitida, identità leggibile.
2. Prompt standard del team (sempre lo stesso, per ridurre la varianza tra operatori).
3. GPT Image 2.5, formato 16:9, multi-angolo.
4. Se serve un outfit preciso, caricalo come reference aggiuntiva e chiedi esplicitamente di vestire il soggetto.
5. Approvazione: volto riconoscibile, attaccatura e texture dei capelli, barba, età, proporzioni, outfit, accessori, niente aggiunto o tolto.
6. Una volta approvata è **canonica**: non si cambia durante la produzione.

> Si approva la somiglianza, non la bellezza. Una sheet sbagliata contamina ogni generazione successiva.

### Numerazione e nomi file

Il numero della reference è lo stesso in storyline, prompt e upload.

```
01_SUBJECT_OWNER_PAJAMAS.png
02_LOCATION_BEDROOM.png
03_OBJECT_ALARM_CLOCK.png
04_SUBJECT_OWNER_SUIT.png
05_SUBJECT_ASSISTANT.png
06_LOCATION_OFFICE.png
```

Prima dell'upload: rileggi la storyline e confronta ogni "Reference N" con la lista file. Chi non ha creato i file deve poterli caricare senza errori.

## 6. Dividere in generazioni

Seedance 2.5 genera fino a **30 secondi** per volta.

- **Metodo A:** l'agente divide l'intera storyline nel numero di generazioni richiesto. Veloce.
- **Metodo B:** il team divide a mano prima (es. Gen 1: 10 s risveglio · Gen 2: 5 s bagno · Gen 3: 20 s ufficio). Da usare quando dialogo e tempi devono essere precisi.
- Taglia sui **confini naturali**: hard cut, cambio di luogo, cambio di outfit.
- Troppe azioni in una generazione → beat saltati o affrettati. Si divide per controllo, non per risparmiare generazioni.

## 7. Esecuzione su Seedance 2.5

1. Apri Seedance 2.5 su Higgsfield.
2. Incolla il prompt completo prodotto dall'agente 17.
3. Carica **solo** le reference usate in quella generazione.
4. Verifica la mappatura: Image 1 = quello che il prompt chiama Reference/Image 1.
5. Imposta la durata uguale a quella del prompt.
6. Genera.
7. Valuta rispetto alla storyline (sezione 8), non rispetto a quanto è bello.
8. Se fallisce, **diagnostica prima di riscrivere** e cambia una sola variabile.

Se il prompt va rigenerato fuori dall'app, passa a Claude: storyline del segmento, reference nell'ordine esatto, durata, energia del montaggio (high-energy / cinematic). Poi rileggi: il prompt è approvato solo se codifica fedelmente la storyline (identità, numerazione, ordine delle azioni, atteggiamento, camera, tagli, durata).

## 8. Controllo qualità (8 check per ogni clip)

| Check | Domanda |
|-------|---------|
| Identità | Il soggetto è uguale alla Character Sheet approvata? |
| Location | Architettura, arredi e luce sono coerenti? |
| Oggetti | Forma, dimensione, colore e materiale invariati? |
| Azioni | Sono avvenute tutte, nell'ordine giusto? |
| Atteggiamento | L'emozione si capisce anche senza audio? |
| Camera | Inquadratura e movimenti servono la scena? |
| Narrazione | La clip racconta il beat previsto? |
| Continuità | Si collega alla clip prima e dopo (outfit, oggetti, posizione)? |

Si approva solo quando qualità visiva **e** accuratezza narrativa sono entrambe ok.

## 9. Troubleshooting

| Sintomo | Causa probabile | Prima correzione |
|---------|-----------------|------------------|
| Il volto cambia | Sheet debole, mapping sbagliato, reference in conflitto | Ricontrolla sheet canonica e ordine di upload |
| Outfit sbagliato | Sheet dello stato sbagliato | Usa la sheet dedicata a quell'outfit |
| La location cambia troppo | Un'immagine non basta per i movimenti richiesti | Location Sheet multi-vista |
| L'oggetto si deforma | Oggetto non referenziato o poco definito | Reference oggetto più pulita |
| Un'azione viene saltata | Generazione sovraccarica o azioni vaghe | Semplifica o scrivi l'azione a passi espliciti |
| Camera casuale | Nessuna direzione camera | Specifica zoom / hard cut / tracking dove conta |
| Bella ma "sbagliata" | Il beat narrativo non torna | Confronta con la storyline riga per riga |
| Le clip non si collegano | Taglio nel punto sbagliato o stati diversi | Taglia su transizioni naturali, stesse reference |
| Prompt troppo complicato | Troppe decisioni aperte nell'input | Semplifica la storyline prima di rigenerare |
| La produzione rallenta di nuovo | Si sta ricostruendo l'image-first | Ogni asset è davvero una reference necessaria? |

## 10. Checklist dei quattro cancelli

**Prima delle reference** — idea chiara · script stabile · storyline scritta · soggetti, stati/outfit, location e oggetti chiave identificati · camera descritta dove conta.

**Prima del prompt** — Character Sheet approvate per ogni soggetto controllato · location e oggetti approvati · numeri definitivi · nomi file coerenti · segmento di storyline finale · durata ed energia decise.

**Prima di Seedance** — prompt rivisto · ordine di upload = numerazione del prompt · durata = piano · solo le reference necessarie · inizio e fine della clip chiari.

**Prima della consegna** — identità, outfit, location e oggetti coerenti · azioni nell'ordine giusto · atteggiamento corretto · camera al servizio della scena · la clip fa avanzare la storia · transizioni ok · qualità adatta alla pubblicazione.

## 11. Esempio: il founder troppo impegnato

**Idea:** un imprenditore lavora dall'alba e non ha né tempo né energie per registrare. L'assistente gli chiede un video per Instagram, lui rifiuta. Entra il clone AI: il team produce i contenuti senza di lui.

**Reference:** 1 founder in pigiama · 2 camera da letto · 3 sveglia · 4 founder in giacca · 5 assistente · 6 ufficio. La moglie che dorme accanto è una comparsa: descritta, non referenziata.

**Storyline (apertura):** Subject 1 (Ref 1) dorme nel letto (Ref 2); l'inquadratura comunica stanchezza, non relax. La sveglia (Ref 3) suona: zoom rapido sul comodino con leggero shake. Lui allunga la mano senza svegliarsi, la manca e rovescia un bicchiere d'acqua (naturale, non comico); riprova, la afferra e la spegne, già irritato. Hard cut: doccia. Hard cut: denti allo specchio. Hard cut: si veste → da qui si usa la Ref 4. In ufficio (Ref 6) l'assistente (Ref 5) gli porge il telefono; lui guarda, rifiuta subito e torna al lavoro, come chi davvero non ha più tempo. Poi la storia passa dal problema al meccanismo: il clone AI.

**Generazioni:** Gen 1 ≈ 10 s risveglio · Gen 2 ≈ 5 s bagno/preparazione · Gen 3 ≈ 20 s ufficio + rifiuto.

## 12. Le 14 regole operative

1. Storyline prima di tutto.
2. Controlla il DNA visivo importante, delega il resto.
3. Un soggetto importante = una Character Sheet per outfit/stato.
4. Un'immagine di location se basta, una Location Sheet se serve continuità spaziale.
5. Referenzia un oggetto solo se la sua coerenza conta.
6. Stessa numerazione in storyline, prompt e upload.
7. Azioni osservabili, non idee astratte.
8. Descrivi l'atteggiamento oltre al movimento.
9. Camera intenzionale, mai decorativa.
10. Dividi sui confini naturali della storia.
11. Claude traduce, il team dirige.
12. Seedance genera, il team giudica.
13. Si valuta rispetto alla storyline, non alla bellezza.
14. Quando qualcosa si rompe, individua il livello esatto prima di cambiare tutto.

## Glossario

| Termine | Significato |
|---------|-------------|
| Storyline | La sequenza visiva dettagliata del video |
| Soggetto | Persona o personaggio in scena |
| Stato visivo | Versione di un soggetto definita da outfit o aspetto |
| Character Sheet | Reference multi-vista canonica di un soggetto/stato |
| Location Reference / Sheet | Immagine (o multi-vista) che definisce l'ambiente |
| Object Reference | Immagine che definisce un oggetto chiave |
| Numero di reference | Il numero che lega lo stesso asset in storyline, prompt e upload |
| Generazione | Un segmento video generato (max 30 s) |
| Energia del montaggio | Ritmo e stile richiesti al segmento |
| Hard cut | Salto immediato a un'altra inquadratura/azione |
| Asset canonico | La versione approvata di una reference, riusata sempre uguale |
