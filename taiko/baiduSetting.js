const { openBrowser, goto, click, alert, closeBrowser } = require('taiko');
(async () => {
    try {
        await openBrowser({headless: false, args:['--window-size=1440, 900']});
        await resizeWindow({width:1280, height:800})
        await goto("https://www.baidu.com");
        await click("设置");
        await click("搜索设置");
        await click("简体中文");
        await alert('已经记录下您的使用偏好', async () => await accept());
        await click("保存设置");
        await waitFor(5000)
    } catch (error) {
        console.error(error);
    } finally {
        await closeBrowser();
    }
})();
