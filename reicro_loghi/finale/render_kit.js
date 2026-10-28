// Esporta i PNG del kit: node render_kit.js (richiede Playwright)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 4, viewport: { width: 1500, height: 1000 } });
  // versioni piatte: ogni SVG in PNG trasparente
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
    await p.setContent(`<body style="margin:0;background:transparent"><img id="i" src="file://${dir}/${f}"></body>`);
    await p.waitForFunction(() => document.getElementById('i').complete);
    await (await p.$('#i')).screenshot({ path: `${dir}/png/${f.replace('.svg', '.png')}`, omitBackground: true });
  }
  await p.goto(`file://${dir}/kit.html`);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  const nomi = { h3d: 'orizzontale_3d', h3d_scuro: 'orizzontale_3d_scuro', v3d: 'verticale_3d', v3d_scuro: 'verticale_3d_scuro' };
  for (const [id, n] of Object.entries(nomi)) await (await p.$('#' + id)).screenshot({ path: `${dir}/png/reicro_${n}.png`, omitBackground: true });
  await p.setViewportSize({ width: 1500, height: 1000 });
  const p2 = await b.newPage({ deviceScaleFactor: 1.5, viewport: { width: 1500, height: 1000 } });
  await p2.goto(`file://${dir}/kit.html`); await p2.evaluate(() => document.fonts.ready); await p2.waitForTimeout(600);
  await p2.screenshot({ path: `${dir}/kit_anteprima.png`, fullPage: true });
  await b.close();
})();
