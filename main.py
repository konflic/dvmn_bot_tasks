import os
import time

import requests
import telegram

from dotenv import load_dotenv

DVMN_TOKEN = os.getenv("DVMN_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def get_work_checks(timestamp):
    response = requests.get(
        url="https://dvmn.org/api/long_polling/",
        headers={"Authorization": f"Token {DVMN_TOKEN}"},
        params={"timestamp": timestamp},
    )
    response.raise_for_status()
    return response.json()


def wait_for_checked_works(delay=5):
    timestamp = None

    while True:
        try:
            check_result = get_work_checks(timestamp)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(delay)

        if check_result["status"] == "timeout":
            timestamp = check_result["timestamp_to_request"]
            continue

        if check_result["status"] == "found":
            timestamp = check_result["last_attempt_timestamp"]
            notify(check_result)


def notify(check_result):
    bot = telegram.Bot(token=BOT_TOKEN)
    attempts = check_result["new_attempts"]

    for attempt in attempts:
        msg = f"У вас проверили работу {attempt['lesson_title']}.\n\n"
        if attempt["is_negative"]:
            msg += f"К сожалению, в работе нашлись ошибки. Бегом туда {attempt['lesson_url']}"
        else:
            msg += "Преподавателю всё понравилось, можно приступать к следующему!"

        bot.send_message(chat_id=CHAT_ID, text=msg, disable_web_page_preview=True)


if __name__ == "__main__":
    load_dotenv()

    wait_for_checked_works()
