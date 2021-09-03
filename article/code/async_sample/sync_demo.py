import time


def visit_url(url, response_time):
    """
    访问url
    """
    print(f"visit: {time.time()} - {url}")
    time.sleep(response_time)
    print(f"response: {time.time()}")


def run_task():
    visit_url('http://itest.info', 2)
    visit_url('http://www.testpub.cn', 3)


start_time = time.perf_counter()
run_task()
print(f"消耗时间：{time.perf_counter() - start_time}")
