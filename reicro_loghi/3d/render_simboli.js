const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const dir = '/home/user/Sarcopenia/reicro_loghi/3d';
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1200, height: 1200 } });
  p.on('console', m => m.type() === 'error' && console.log(m.text()));
  p.on('pageerror', e => console.log('ERR', e.message));
  for (const v of (process.argv[2] || '7,8,9').split(',')) {
    await p.goto(`file://${dir}/simbolo3d.html?v=${v}`);
    await p.waitForFunction(() => document.title === 'ready');
    await (await p.$('canvas')).screenshot({ path: `${dir}/simbolo${v}_3d.png`, omitBackground: true });
  }
  await b.close();
})();
