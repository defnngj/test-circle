import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.log import Log
from selenium.webdriver.support import expected_conditions as EC


async def demo():
    driver = webdriver.Chrome()
    session = driver.bidi_connection()
    log = Log(driver, session)

    async with log.mutation_events() as event:
        driver.get("https://www.google.com")
        driver.find_element(By.ID, "reveal").click()
        WebDriverWait(driver, 5)\
            .until(EC.visibility_of(driver.find_element(By.ID, "revealed")))

    assert event["attribute_name"] == "style"
    assert event["current_value"] == ""
    assert event["old_value"] == "display:none;"

asyncio.run(demo())

