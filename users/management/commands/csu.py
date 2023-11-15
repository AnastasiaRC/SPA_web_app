import os
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создание суперпользователя и обычного пользователя"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@habit.ru',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password(os.getenv('ADMIN_PASSWORD'))
        user.save()

        user = User.objects.create(
            email="nastia.riabtseva18@yandex.by",
            first_name="test",
            last_name="test",
            tg_name="Anastasia86543",
            is_superuser=False,
            is_staff=False,
            is_active=True
        )

        user.set_password("1234")
        user.save()
