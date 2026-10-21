const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = '/home/user/Sarcopenia/reicro_loghi/3d';
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 3, viewport: { width: 1000, height: 1100 } });
  await p.goto(`file://${dir}/loghi3d.html`);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  for (const n of [7, 8, 9]) await (await p.$('#logo' + n)).screenshot({ path: `${dir}/reicro_logo${n}_3d.png`, omitBackground: true });
  await p.setViewportSize({ width: 1000, height: 1100 });
  await p.screenshot({ path: `${dir}/anteprima_3d.png`, fullPage: true });
  await b.close();
})();
