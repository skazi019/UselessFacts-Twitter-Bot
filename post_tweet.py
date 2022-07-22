import os
import schedule
from dotenv import load_dotenv, find_dotenv

from WebBot import WebBot
from facts import Facts
from logger import Logger


logger = Logger(filename="post_tweet.log")
logger = logger.get_logger()

BASE_URL = os.path.abspath(os.getcwd())

load_dotenv(find_dotenv())


def twitter_bot_activate():
    try:
        webbot = WebBot(logger=logger)
        webbot.twitter_login()
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Error: {e}")
        webbot.close_driver()
    else:
        webbot.tweet_useless_fact()
    finally:
        logger.info(f"Posted tweet successfully")
        print(f"Posted tweet successfully")
        webbot.close_driver()


schedule.every().day.at("11:00").do(twitter_bot_activate)

while True:
    schedule.run_pending()
