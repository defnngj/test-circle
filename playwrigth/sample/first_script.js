const { chromium, webkit, firefox } = require('playwright');

(async () => {
  const browser = await chromium.launch({headless: false, slowMo: 50 });
  // const browser = await webkit.launch();
  // const browser = await firefox.launch();

  const page = await browser.newPage();
  await page.goto('http://www.baidu.com/');
  await page.screenshot({ path: `example.png` });
  await browser.close();
})();