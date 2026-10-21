# Sarcopenia: animazione "Dentro il muscolo"

Animazione didattica (40 s, 16:9, 1920×1080) per una presentazione PowerPoint sulla sarcopenia.
Tre muscoli fusiformi (bambino, adulto, anziano) vengono tagliati a metà del ventre; le sezioni
ruotano verso lo spettatore e mostrano fibre muscolari (tipo I e tipo II), connettivo e tessuto
adiposo, con barre di tessuto muscolare / tessuto adiposo e fonti. Senza titolo né didascalie:
il testo lo dice chi presenta.

## File

| File | Cosa è |
|---|---|
| `sarcopenia.html` | **Sorgente principale.** Pagina senza doctype (formato Artifact di claude.ai). Modifica questo. |
| `sarcopenia_standalone.html` | Stessa pagina con doctype, da aprire nel browser. Rigenerata da `build.sh`. |
| `record.js` | Registra l'animazione in MP4 (Playwright + ffmpeg), fotogramma per fotogramma. |
| `build.sh` | Rigenera la standalone e l'MP4. |
| `sarcopenia.mp4` | Ultimo video renderizzato. |

Requisiti per il rendering: Node.js, `playwright` con Chromium, `ffmpeg`.
`./build.sh` impiega circa 1,5 minuti.

## Come è costruito il codice (tutto in `sarcopenia.html`)

- Canvas 2D a risoluzione fissa 1920×1080. Tutto è disegnato via codice; nessuna immagine esterna.
- **Rendering deterministico**: `render(t)` disegna il fotogramma al tempo `t` (secondi). È esposto come
  `window.renderAt(t)`; `window.DURATION = 40`. Con `?record` nell'URL i controlli sono nascosti.
- **Colori e font**: token CSS in `:root` (`--muscle`, `--muscle-deep`, `--fat`, `--conn`, ...), letti dal JS
  nell'oggetto `C`. Font Google: Familjen Grotesk (titoli), IBM Plex Sans (testo), IBM Plex Mono (numeri).
- **Sezioni istologiche** (`makeSection`, `paintSection`): punti Poisson-disk nel disco unitario →
  celle poligonali (Voronoi per clipping di semipiani) → fibre ristrette verso il centroide.
  Fascicoli/setti: punti vicini al confine tra centri-fascicolo diventano connettivo.
  Parametri per età in `AGES[].sec`: `d` (dimensione fibre), `fat` (frazione di celle adipose),
  `clusters` (nuclei di infiltrazione adiposa), `loss` (fibre perse), `shrink1/shrink2` (atrofia tipo I/II), `seed`.
  Ogni sezione è pre-renderizzata su un canvas offscreen e poi disegnata con `drawImage` (anche deformata
  in ellisse durante la rotazione).
- **Muscolo 3D** (`prof`, `musclePath`, `drawMuscle`): profilo fusiforme tendine→ventre→tendine,
  parametro `u` 0..1 lungo la lunghezza; si può disegnare un tratto `[ua, ub]` (il taglio è a `u = 0.5`).
- **Dati mostrati**: `AGES[]` → `fat` (% tessuto adiposo), `fatTxt`, `fib` (riga descrittiva fibre).
  Tessuto muscolare = 100 − fat. Barra adiposo in scala 0–10%.
- **Testi**: `SOURCES` (due righe di fonti in basso),
  legenda nel blocco `// legend`.

## Timeline (secondi)

| t | Evento |
|---|---|
| 0.3–2.2 | Entrata dei tre muscoli con etichette |
| 2.4–3.9 | Lama che taglia |
| 3.9–5.5 | Metà destre si allontanano; appaiono le facce di taglio |
| 5.5–9.5 | Le facce ruotano e diventano tre cerchi (bambino → adulto → anziano) |
| 9.3–12.0 | Etichette, barre tessuto muscolare/adiposo, legenda, fonti |
| 12.0–23.0 | Fase bambino/adulto: anziano attenuato (dissolvenza di 2 s) |
| 23.2–34.0 | Fase anziano: bambino e adulto attenuati, tessuto adiposo evidenziato con anelli pulsanti |
| 34.0–40 | Tutte e tre le sezioni in piena luce |

## Dati e fonti

- Tessuto adiposo intramuscolare (coscia, MRI/MRS): giovani adulti 1,7 ± 0,7%, anziani sarcopenici
  (~80 anni) 6,0 ± 3,8% — Grimm A et al., J Frailty Aging 2018, doi:10.14283/jfa.2018.16.
- Bambini sani (controlli, vasto laterale) 2,3 ± 1,9% — AJR Am J Roentgenol 2019, doi:10.2214/AJR.18.20354
  (autori da verificare; altri studi con tecniche diverse riportano valori più alti).
- ~25% di fibre in meno a ~72 anni — Lexell J et al., Muscle Nerve 1983;6:588–95.
  Perdita di fibre + atrofia soprattutto tipo II — Lexell J et al., J Neurol Sci 1988;84:275–94.
- Tessuto adiposo intermuscolare +29% (donne) / +48,5% (uomini) in 5 anni — Delmonico MJ et al., Am J Clin Nutr 2009;90:1579–85.
- A ~75 anni: massa −0,64–0,98%/anno, forza −2,5–4%/anno — Mitchell WK et al., Front Physiol 2012;3:260.
- Definizione di sarcopenia — Cruz-Jentoft AJ et al. (EWGSOP2), Age Ageing 2019;48:16–31.

Le sezioni sono schematiche e non in scala. I riferimenti sono stati verificati tramite abstract, non sui testi completi.

## Uso in PowerPoint

Inserisci › Video › Questo dispositivo › `sarcopenia.mp4`; in Riproduzione: "Avvia automaticamente".
