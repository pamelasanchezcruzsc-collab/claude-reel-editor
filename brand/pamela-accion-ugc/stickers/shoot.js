const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1 });
  await p.goto('file://' + process.argv[2] + '/stickers.html'); await p.waitForTimeout(800);
  for (const id of ['phone','scissors','point','sparkles','chat','film','heart','noapp','listo','descarga','tres','strip','igtext','p1','p2','p3'])
    await (await p.$('#' + id)).screenshot({ path: process.argv[2] + '/' + id + '.png', omitBackground: true });
  await b.close();
})();
