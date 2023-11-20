from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.paginators import PagePagination
from habits.permissions import IsOwner
from habits.serializers import HabitsSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""
    serializer_class = HabitsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.author = self.request.user
        new_habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Обновление привычки"""
    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitListAPIView(generics.ListAPIView):
    """Отображение листа привычек"""
    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
    pagination_class = PagePagination


class HabitListPublicAPIView(generics.ListAPIView):
    """Отображение публичных привычек"""
    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PagePagination

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Отображение отдельной привычки"""
    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitDeleteAPIView(generics.DestroyAPIView):
    """Удаление привычки"""
    serializer_class = HabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
