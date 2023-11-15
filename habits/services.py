from datetime import datetime
import requests
from django.core.exceptions import ObjectDoesNotExist
from config.settings import TELEGRAM_TOKEN
from habits.models import Habit
from users.models import User


def telegram_check():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    response = requests.get(url)
    if response.status_code == 200:
        for tg_user in response.json()["result"]:
            tg_chat_id = tg_user["message"]["from"]["id"]
            tg_name = tg_user["message"]["from"]["username"]
            try:
                user = User.objects.get(tg_name=tg_name)
                if user.chat_id is None:
                    user.chat_id = tg_chat_id
                    user.save()
            except ObjectDoesNotExist:
                print("Не найдено")


def send_telegram_message():
    today_time = datetime.now()
    for habit in Habit.objects.filter(is_pleasant=False):
        if habit.period == "DAILY":
            if habit.time.strftime("%H:%M") == today_time.strftime("%H:%M"):
                chat_id = habit.author.chat_id
                if habit.award:
                    message = (f"Место: {habit.place}\n"
                               f"Действие: {habit.action}\n"
                               f"Вознаграждение: {habit.award}\n"
                               f"Время на выполнение: {habit.time_to_complete}")
                else:
                    message = (f"Место: {habit.place}\n"
                               f"Действие: {habit.action}\n"
                               f"Заведите приятную привычку: {habit.pleasant_habit.action}\n"
                               f"Время на выполнение:: {habit.time_to_complete}")
                url = f"https://api.telegram.org/bot{'TELEGRAM_TOKEN'}/sendMessage?chat_id={chat_id}&text={message}"
                response = requests.get(url)
                print(response.json())
            if habit.period == 'WEEKLY':
                if habit.time.strftime("%H:%M") == today_time.strftime("%H:%M"):
                    chat_id = habit.author.chat_id
                    if habit.award:
                        message = (f"Место: {habit.place}\n"
                                   f"Действие: {habit.action}\n"
                                   f"Вознаграждение: {habit.award}\n"
                                   f"Время на выполнение: {habit.time_to_complete}")
                    else:
                        message = (f"Место: {habit.place}\n"
                                   f"Действие: {habit.action}\n"
                                   f"Заведите приятную привычку: {habit.pleasant_habit.action}\n"
                                   f"Время на выполнение:: {habit.time_to_complete}")
                    url = f"https://api.telegram.org/bot{'TELEGRAM_TOKEN'}/sendMessage?chat_id={chat_id}&text={message}"
                    response = requests.get(url)
                    print(response.json())
