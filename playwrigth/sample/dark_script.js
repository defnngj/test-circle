const { webkit, devices, chromium } = require('playwright');
const pixel2 = devices['Pixel 2'];

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    ...pixel2,
    colorScheme: 'dark'
  });
  const page = await context.newPage();
  await page.goto('https://m.baidu.com');
  await page.screenshot({ path: 'colosseum-iphone-dark.png' });
  await browser.close();
})();