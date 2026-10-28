"""Genera il kit vettoriale del logo REICRO (proposta 9, Spirale in rete).

Uso: python3 genera_svg.py <manrope600.ttf> <manrope800.ttf>
I file Manrope (Google Fonts, licenza OFL) servono solo a convertire il testo
in tracciati: gli SVG prodotti non dipendono da nessun font installato.
"""
import math, sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = os.path.dirname(os.path.abspath(__file__))
F600, F800 = TTFont(sys.argv[1]), TTFont(sys.argv[2])

TEMI = {
    # spirale (inizio, fine gradiente), raggi, nodi vicini, nodi lontani, persona/ospedale, scritta, sottotitolo
    'colori':   dict(sp=('#1C9C8C', '#0E4F5C'), link=('#0E4F5C', .45), n0='#1C9C8C', n1='#0E4F5C', acc='#E8664A', word='#12303A', sub='#5D7A80'),
    'negativo': dict(sp=('#FFFFFF', '#FFFFFF'), link=('#FFFFFF', .5), n0='#3FC1AE', n1='#FFFFFF', acc='#E8664A', word='#FFFFFF', sub='#BFD9DC'),
    'bianco':   dict(sp=('#FFFFFF', '#FFFFFF'), link=('#FFFFFF', .5), n0='#FFFFFF', n1='#FFFFFF', acc='#FFFFFF', word='#FFFFFF', sub='#FFFFFF'),
}


def P(r, a):
    a = math.radians(a)
    return round(r * math.cos(a), 2), round(r * math.sin(a), 2)


def simbolo(t, gid):
    """Spirale in rete centrata in (0,0), raggio esterno circa 106."""
    th1, r0, r1 = 2.25 * 360, 20, 96
    sp = lambda th: P(r0 + (r1 - r0) * th / th1, th - 90)
    d = 'M' + ' L'.join('%s,%s' % sp(th) for th in range(0, int(th1) + 1, 3))
    lc, lo = t['link']
    out = [f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="-96" y1="-96" x2="96" y2="96">'
           f'<stop offset="0" stop-color="{t["sp"][0]}"/><stop offset="1" stop-color="{t["sp"][1]}"/></linearGradient></defs>']
    nodi = []
    for k, base in enumerate((0, 120, 240)):
        ts = [base + 360 * j for j in range(3) if base + 360 * j <= th1]
        x, y = sp(ts[-1])
        out.append(f'<line x1="0" y1="0" x2="{x}" y2="{y}" stroke="{lc}" stroke-width="3" opacity="{lo}" stroke-linecap="round"/>')
        for j, th in enumerate(ts):
            col = t['acc'] if (j == len(ts) - 1 and k == 0) else (t['n0'] if j == 0 else t['n1'])
            nodi.append('<circle cx="%s" cy="%s" r="%d" fill="%s"/>' % (*sp(th), 7 + 2 * j, col))
    out.append(f'<path d="{d}" fill="none" stroke="url(#{gid})" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    out += nodi
    out.append(f'<circle cx="0" cy="0" r="14" fill="{t["acc"]}"/>')
    return out


def testo(font, s, size, tracking, x, y, fill):
    """Testo convertito in tracciati; restituisce (svg, larghezza)."""
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font['hmtx']
    k = size / font['head'].unitsPerEm
    pen, cx = SVGPathPen(gs), 0.0
    for ch in s:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x + cx, y)))
        cx += hmtx[g][0] * k + tracking
    w = cx - tracking
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>', w


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.1f} {h:.1f}">\n'
            + '\n'.join(body) + '\n</svg>\n')


WORD, SUB = 'REICRO', 'RETE INTEGRATA CRONICITÀ'
for nome, t in TEMI.items():
    # orizzontale: simbolo a sinistra, scritta a destra
    w1, ww = testo(F800, WORD, 92, 2, 250, 118, t['word'])
    s1, sw = testo(F600, SUB, 19, 3.4, 254, 160, t['sub'])
    body = ['<g transform="translate(112,110)">'] + simbolo(t, 'gs') + ['</g>', w1, s1]
    open(f'{OUT}/reicro_orizzontale_{nome}.svg', 'w').write(svg(max(250 + ww, 254 + sw) + 20, 220, body))

    # verticale: simbolo sopra, scritta centrata sotto
    _, ww = testo(F800, WORD, 92, 2, 0, 0, '')
    _, sw = testo(F600, SUB, 19, 3.4, 0, 0, '')
    W = max(ww, sw, 230) + 40
    w1, _ = testo(F800, WORD, 92, 2, (W - ww) / 2, 330, t['word'])
    s1, _ = testo(F600, SUB, 19, 3.4, (W - sw) / 2, 374, t['sub'])
    body = [f'<g transform="translate({W / 2:.1f},126)">'] + simbolo(t, 'gs') + ['</g>', w1, s1]
    open(f'{OUT}/reicro_verticale_{nome}.svg', 'w').write(svg(W, 400, body))

    # solo simbolo (icona quadrata)
    body = ['<g transform="translate(115,115)">'] + simbolo(t, 'gs') + ['</g>']
    open(f'{OUT}/reicro_simbolo_{nome}.svg', 'w').write(svg(230, 230, body))
print('ok')
