// Registra l'animazione fotogramma per fotogramma (30 fps) e la codifica in MP4 con ffmpeg.
// Uso: node record.js <file.html> <output.mp4>   — richiede playwright (Chromium) e ffmpeg.
const path = require('path');
const { spawn } = require('child_process');
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }

(async () => {
  const [html, out] = process.argv.slice(2), FPS = 30;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.resolve(html) + '?record');
  await p.evaluate(() => document.fonts.ready);
  const dur = await p.evaluate(() => DURATION);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f <= dur * FPS; f++) {
    const b64 = await p.evaluate(t => { renderAt(t); return document.getElementById('stage').toDataURL('image/png').split(',')[1]; }, f / FPS);
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
})();
