const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({headless: false, slowMo: 50 });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('http://127.0.0.1:8000/');
  await page.fill("#inputUsername", 'admin');
  await page.fill("#inputPassword", 'admin123456');
  await page.click("body > div > form > button");
  await page.close();

  const page2 = await context.newPage();
  await page2.goto("http://127.0.0.1:8000/guest_manage/")
  await browser.close();

})();