const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({headless: false, slowMo: 50 });
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();
  await page.goto('https://pypi.org/project/selenium/#files');
  const [ download ] = await Promise.all([
    page.waitForEvent('download'), 
    page.click('#files > table > tbody > tr:nth-child(2) > th > a')
  ]);
  const path = await download.path();
  console.log("path", path);
  await browser.close();
})();



                    