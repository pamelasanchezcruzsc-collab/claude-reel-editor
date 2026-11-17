const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1 });
  await p.goto('file://' + process.argv[2] + '/stickers4.html'); await p.waitForTimeout(800);
  for (const id of ['comunidad','recurso','escribe','ritmo','hands','raise','phonewa','seed'])
    await (await p.$('#' + id)).screenshot({ path: process.argv[2] + '/' + id + '.png', omitBackground: true });
  await b.close(); })();
