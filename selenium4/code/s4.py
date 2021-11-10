from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.log import Log




# driver = webdriver.Chrome()
# session = driver.bidi_connection()
# log = Log(driver, session)
#
# with log.mutation_events() as event:
#     driver.get("dynamic.html")
#     driver.find_element(By.ID, "reveal").click()
#     WebDriverWait(driver, 5).until(EC.visibility_of(driver.find_element(By.ID, "revealed")))
#
# assert event["attribute_name"] == "style"
# assert event["current_value"] == ""
# assert event["old_value"] == "display:none;"
#
import asyncio

async def printConsoleLogs():
    driver = webdriver.Chrome()
    driver.get("http://www.google.com")

    async with driver.bidi_connection() as session:
        log = Log(driver, session)
        from selenium.webdriver.common.bidi.console import Console
        async with log.add_listener(Console.ALL) as messages:
            driver.execute_script("console.log('I love cheese')")
        print(messages["message"])

    driver.quit()


asyncio.run(printConsoleLogs())

