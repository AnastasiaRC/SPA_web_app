from django.contrib import admin
from users.models import User


# admin.site.register(User)
@admin.register(User)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_active', 'tg_name', 'chat_id')
