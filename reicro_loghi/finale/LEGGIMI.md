# Logo REICRO – kit definitivo (proposta 9, "Spirale in rete")

La spirale è il percorso di cura della persona cronica, che continua e si allarga nel tempo; i tre raggi e i nodi sono la rete dei servizi che la tengono legata alla persona (al centro, in corallo). Il nodo corallo esterno è l'ospedale.

| Uso | File |
|---|---|
| Intestazione slide, sfondo chiaro | `reicro_orizzontale_colori.svg` / `png/…png` |
| Intestazione slide, sfondo scuro | `reicro_orizzontale_negativo.svg` |
| Copertina | `reicro_verticale_colori.svg`, oppure `png/reicro_verticale_3d.png` |
| Su foto o colore pieno | `reicro_*_bianco.svg` |
| Versione 3D (copertina, slide di apertura) | `png/reicro_orizzontale_3d*.png`, `png/reicro_verticale_3d*.png` |
| Solo simbolo / icona | `reicro_simbolo_*.svg`, `reicro_simbolo_3d*.png` |

Gli SVG sono vettoriali, con il testo già convertito in tracciati: non serve installare il font. Per Word e PowerPoint vanno bene sia gli SVG sia i PNG (sfondo trasparente).
Sotto i 32 px di larghezza il simbolo perde dettaglio: in quei casi usare solo la scritta.

Rigenerare: `python3 genera_svg.py manrope600.ttf manrope800.ttf` (vettoriali), poi `node render_kit.js` (PNG e anteprima). I simboli 3D si producono con `../3d/simbolo3d.html?v=9` (`&tema=scuro` per gli sfondi scuri).
Palette: blu-petrolio #0E4F5C · verde acqua #1C9C8C · corallo #E8664A · testo #12303A · font Manrope.
