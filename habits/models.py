import datetime
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    PERIOD = (
        ('DAILY', 'каждый день'),
        ('WEEKLY', 'раз в неделю')
    )

    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создатель привычки', **NULLABLE)
    place = models.CharField(max_length=100, verbose_name='место')
    time = models.TimeField(verbose_name='время', **NULLABLE)
    action = models.TextField(verbose_name='действие')
    pleasant_habit = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='приятная привычка', **NULLABLE)
    is_pleasant = models.BooleanField(verbose_name='признак приятной привычки', default=False)
    period = models.CharField(max_length=15, verbose_name='периодичность', choices=PERIOD, default='DAILY')
    award = models.TextField(verbose_name='вознаграждение', **NULLABLE)
    time_to_complete = models.TimeField(verbose_name='время на выполнение', default=datetime.time(minute=2))
    is_public = models.BooleanField(verbose_name='признак публичности', default=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.action}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
