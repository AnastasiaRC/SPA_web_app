from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('author', 'place', 'time', 'action',
                    'pleasant_habit', 'is_pleasant', 'period',
                    'award', 'time_to_complete', 'is_public')
