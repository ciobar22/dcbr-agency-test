# Lionel Studio: concept DCBR

Una vetrina dove le T-shirt sono appese a una stanga e si girano verso di te quando ci passi sopra (o le scorri col dito). Si basa sul [interactive garment starter](https://github.com/amirmushichge/interactive-garment-starter) di Amir Mušić (MIT), installato in `garment-showcase/`.

## Aprirlo

```sh
cd garment-showcase
node scripts/serve.mjs
# http://127.0.0.1:5264/lionel.html   (la demo originale resta su /)
```

## Cosa c'è

| File | Cosa fa |
| --- | --- |
| `lionel.html`, `src/lionel.css`, `src/lionel.js` | La pagina: una sola barra spedizione, menu corto, prezzi in euro, taglie, carrello demo |
| `config/lionel.json` | I 4 capi, testi e prezzi |
| `public/fixtures/lionel-*` | Le 4 rotazioni (30 fotogrammi ciascuna) |
| `concepts/lionel/prints.py` | Disegna le stampe (Anton e Archivo Black, OFL) |
| `pipeline/restyle.py` | Ricolora una rotazione già approvata e ci mette sopra una stampa nuova |
| `reels/out/*.mp4` | I due reel verticali (vedi `reels/README.md`) |

La pagina risolve alcuni problemi della Fase 5 (ispezione visiva): banner spedizione ripetuto sei volte, menu tagliato, prezzi non in euro, prezzo e "Aggiungi al carrello" fuori schermo.

## Cosa è vero e cosa è concept

- **LET'S GOOO!!! Tee nera, € 68**: il capo e il prezzo esistono nel catalogo di lionelstudio.com. L'immagine invece è un concept, non la foto del capo vero.
- **Sabbia, Panna, Verde oliva**: capi inventati per la demo, non sono in catalogo.
- Le rotazioni non sono state generate da zero. Sono la ripresa LTX-2.5 della maglietta bianca dello starter (MIT), ricolorata e ristampata fotogramma per fotogramma con `pipeline/restyle.py`. Costo di generazione: 0 €.
- Nessuna foto, logo o file di Lionel Studio è incluso. Le stampe scrivono solo il nome del negozio.

## Prossimo passo: i capi veri

Per far girare i prodotti veri (per esempio un abito doppiopetto o una giacca Levi's customizzata) servono:

1. foto fronte e retro del capo, che Lionel ci autorizza a usare;
2. due immagini di partenza da approvare: il capo di fronte e di profilo stretto, su fondo verde o magenta;
3. una generazione video a pagamento (Higgsfield, LTX o Kling), da approvare prima con un budget e un numero massimo di tentativi;
4. scontorno con `pipeline/prepare.py`, una voce nuova in `config/lionel.json`, test su telefono vero.

La procedura completa è in `docs/agent-workflow.md`.

## Uso pubblico

È materiale per il pitch. Il nome Lionel Studio si pubblica solo con l'ok di Lionel. Quando si presenta il lavoro, va citata l'interazione originale di [@cambreedesigns](https://x.com/cambreedesigns/status/2104999693113766152) e lo starter di Amir Mušić.
