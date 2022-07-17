import os
import time
from dotenv import load_dotenv, find_dotenv

from WebBot import WebBot
from facts import Facts
from logger import Logger

twitter_home = "https://twitter.com/"

webbot = WebBot(url=twitter_home)
fact = Facts()
logger = Logger(filename="post_tweet.log")
post_day = fact.get_post_day()

BASE_URL = os.path.abspath(os.getcwd())
PREPEND = f"Useless fact #{post_day}"
TWEET_LENGTH = 280 - len(PREPEND)

load_dotenv(find_dotenv())

random_fact = fact.random_fact()
print(f"Random fact of the day: {random_fact}")

try:
    webbot.twitter_login()
except Exception as e:
    print(f"Error: {e}")
    webbot.close_driver()
finally:
    time.sleep(30)
    webbot.close_driver()
fact.save_facts(fact=random_fact)
