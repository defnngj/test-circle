import time
import asyncio
from pyppeteer import launch

async def hello_world():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://www.baidu.com')
    await page.type("#kw", "pyppeteer")
    await page.click("#su")
    # await page.screenshot({'path': 'example.png'})
    await browser.close()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello_world())


if __name__ == '__main__':
    start = time.time()
    main()
    print("running time:", time.time() - start)
