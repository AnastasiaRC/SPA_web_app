from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from habits.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=60, unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=50, verbose_name='имя', **NULLABLE)
    is_active = models.BooleanField(verbose_name='активность', default=True)
    tg_name = models.CharField(max_length=100, unique=True, verbose_name="ID в телеграме", **NULLABLE)
    chat_id = models.IntegerField(unique=True, **NULLABLE, default=None, verbose_name="ID чата в телеграме")
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
