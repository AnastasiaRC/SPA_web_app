from celery import shared_task
from habits.services import telegram_check, send_telegram_message


@shared_task
def habits_bot():
    telegram_check()
    send_telegram_message()
