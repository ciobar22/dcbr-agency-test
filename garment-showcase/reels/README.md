# Reel verticali (1080×1920, 30 fps)

| File | Durata | Per chi |
| --- | --- | --- |
| `out/lionel-reel-1080x1920.mp4` | 16,6 s | Pitch a Lionel: il sito sul telefono, swipe, scheda prodotto, carrello |
| `out/dcbr-reel-1080x1920.mp4` | 25 s | Profilo DCBR: foto → video AI → fotogrammi → vetrina che si muove |

Sono muti: l'audio di tendenza va aggiunto direttamente su Instagram o TikTok. In basso c'è spazio libero per la UI dell'app.

## Rigenerarli

```sh
cd garment-showcase
node reels/record.mjs lionel     # oppure: dcbr
node reels/record.mjs dcbr --from 14 --to 21   # solo un tratto, per le prove
```

Servono Playwright (con Chromium) e FFmpeg. `CHROMIUM` e `FFMPEG` accettano percorsi espliciti.

`composer.html` contiene scene, testi e gesti. Il sito vero (`lionel.html`) gira dentro un iframe. Il registratore falsifica l'orologio della pagina e avanza di 1/30 di secondo per fotogramma, così rotazioni, swipe e scritte cadono sempre sullo stesso frame. I fotogrammi temporanei vanno in `work/reels/`, che non viene messo in git.
