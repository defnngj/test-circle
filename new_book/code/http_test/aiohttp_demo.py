import aiohttp
import asyncio


async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:

            print(f"状态码: {response.status}")

            html = await response.text()
            print("HTML页面:", html[:15], "...")

# asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
