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

from facts import Facts

twitter_home = "https://twitter.com/i/flow/login/"


class WebBot:
    def __init__(self, logger) -> None:
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

        self._facts = Facts()
        self._logger = logger

    def close_driver(self) -> None:
        self._driver.quit()

    def twitter_login(self) -> None:
        try:
            self._driver.get(twitter_home)
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
            self._logger.error(f"Error in twitter login: {e}")

    def tweet_useless_fact(self) -> bool:
        try:
            post_day = self._facts.get_post_day()
            PREPEND = f"Useless fact #{post_day}\n"
            TWEET_LENGTH = 280 - len(PREPEND)
            fact = self._facts.random_fact()
            while len(fact["fact"]) > TWEET_LENGTH:
                fact = self._facts.random_fact()
            tweet = PREPEND + fact["fact"]
            print(f"Tweet is: {tweet}")

            tweetbox = self._driver.find_element(
                By.XPATH,
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div',
            )
            tweetbox.send_keys(tweet)
            post_button = self._driver.find_element(
                By.XPATH,
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]',
            )
            post_button.click()
            self._facts.save_facts(fact=fact)
            return True
        except Exception as e:
            print(f"Error in posting tweet: {e}")
            self._logger.error(f"Error in posting tweet: {e}")
