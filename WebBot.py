import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options


class WebBot:
    def __init__(self, url: str) -> None:
        options = Options()
        options.page_load_strategy = "normal"
        # options.add_argument("--headless")
        options.add_experimental_option("detach", True)

        self._driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
            ),
            options=options,
        )

        self._driver.get(url)

    def close_driver(self) -> None:
        self._driver.quit()

    def twitter_login(self) -> None:
        try:
            self._driver.implicitly_wait(10)
            login_button = self._driver.find_element(
                By.XPATH,
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]',
            )
            login_button.find_element(By.TAG_NAME, "a").click()
            self._driver.implicitly_wait(10)
            username = self._driver.find_element(By.NAME, "text")
            username.send_keys(os.environ.get("USERNAME"))
            self._driver.find_element(
                By.XPATH,
                '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]',
            ).click()
            self._driver.implicitly_wait(10)
            try:
                self._driver.find_element(By.NAME, "text").send_keys(
                    os.environ.get("PHONE")
                )
                self._driver.find_element(
                    By.XPATH,
                    '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div',
                ).click()
            except Exception as e:
                pass
            self._driver.implicitly_wait(10)
            password = self._driver.find_element(By.NAME, "password")
            password.send_keys(os.environ.get("PASSWORD"))
            self._driver.find_element(
                By.XPATH,
                '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div',
            ).click()
        except Exception as e:
            print(f"Error: {e}")

    def tweet_useless_fact(self, fact: dict, PREPEND: str) -> bool:
        pass
