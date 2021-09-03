import asyncio
import time


async def visit_url(url, response_time):
    """访问 url"""
    print(f"visit: {time.time()} - {url}")
    await asyncio.sleep(response_time)
    print(f"response: {time.time()}")


# async def run_task():
#     await visit_url('http://itest.info', 2)
#     await visit_url('http://www.testpub.cn', 3)


async def run_task():
    url1 = visit_url('http://itest.info', 2)
    url2 = visit_url('http://www.testpub.cn', 3)

    await asyncio.gather(url1, url2)
    # task1 = asyncio.create_task(url1)
    # task2 = asyncio.create_task(url2)
    #
    # await task1
    # await task2


start_time = time.perf_counter()
asyncio.run(run_task())
print(f"消耗时间：{time.perf_counter() - start_time}")
