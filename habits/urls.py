from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitUpdateAPIView, HabitRetrieveAPIView, HabitListAPIView, \
    HabitDeleteAPIView, HabitListPublicAPIView
from django.urls import path

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habits/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habits/view/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_view'),
    path('habits/list/public', HabitListPublicAPIView.as_view(), name='habit_list_public'),
    path('habits/list/', HabitListAPIView.as_view(), name='habit_list'),
    path('habits/delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habit_delete'),
]
