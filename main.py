import os
import time

import requests
import telegram

from dotenv import load_dotenv

load_dotenv()

DVMN_TOKEN = os.getenv("DVMN_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def get_work_checks(timestamp=None):
    try:
        response = requests.get(
            url="https://dvmn.org/api/long_polling/",
            headers={"Authorization": "Token " + DVMN_TOKEN},
            params={"timestamp": timestamp}
        )
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        return {"status": "read_timeout"}
    response.raise_for_status()
    return response.json()


def wait_for_checked_works(delay=1):
    timestamp = None
    while True:
        time.sleep(delay)

        check_result = get_work_checks(timestamp)

        if check_result["status"] == "read_timeout":
            continue

        if check_result["status"] == "timeout":
            timestamp = check_result["timestamp_to_request"]
            continue

        notify_with_bot(check_result)


def notify_with_bot(check_result):
    bot = telegram.Bot(token=BOT_TOKEN)
    attempts = check_result["new_attempts"]

    for attempt in attempts:
        msg = f"У вас проверили работу {attempt['lesson_title']}.\n\n"
        if attempt["is_negative"]:
            msg += f"К сожалению, в работе нашлись ошибки. Бегом туда {attempt['lesson_url']}"
        else:
            msg += "Преподавателю всё понравилось, можно приступать к следующему!"

        bot.send_message(chat_id="156109367", text=msg, disable_web_page_preview=True)


if __name__ == "__main__":
    wait_for_checked_works()
