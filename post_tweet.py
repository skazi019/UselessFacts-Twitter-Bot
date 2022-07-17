import os
import time
import logging
from random import random
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options

options = Options()
options.page_load_strategy = "normal"
# options.add_argument("--headless")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
    options=options,
)

from facts import Facts

BASE_URL = os.path.abspath(os.getcwd())
PREPEND = "Useless fact #140"
TWEET_LENGTH = 280 - len(PREPEND)

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)
handler = logging.FileHandler("post_tweet.log")
handler.setLevel(logging.ERROR)
logformat = logging.Formatter("%(asctime)s |  %(name)s |  %(levelname)s |  %(message)s")
handler.setFormatter(logformat)
logger.addHandler(handler)


fact = Facts()
random_fact = fact.random_fact()
print(f"Random fact of the day: {random_fact}")

twitter_home = "https://twitter.com/"

driver.get(twitter_home)
time.sleep(5)
login_button = driver.find_element(
    By.XPATH,
    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]',
)
try:
    # Login flow
    login_button.find_element(By.TAG_NAME, "a").click()
    driver.implicitly_wait(10)
    username = driver.find_element(By.NAME, "text")
    username.send_keys(os.environ.get("USERNAME"))
    driver.find_element(
        By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]',
    ).click()
    driver.implicitly_wait(10)
    try:
        driver.find_element(By.NAME, "text").send_keys(os.environ.get("PHONE"))
        driver.find_element(
            By.XPATH,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div',
        ).click()
    except Exception as e:
        pass
    driver.implicitly_wait(10)
    password = driver.find_element(By.NAME, "password")
    password.send_keys(os.environ.get("PASSWORD"))
    driver.find_element(
        By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div',
    ).click()
    time.sleep(30)
except Exception as e:
    print(f"Error: {e}")
fact.save_facts(fact=random_fact)
driver.quit()
