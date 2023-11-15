import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User(
            email="nastia.riabtseva18@yandex.by",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            tg_name='Anastasia86543',
            chat_id=849038215,
        )
        self.user.set_password("test")
        self.user.save()

        token = RefreshToken.for_user(self.user)
        self.access_token = str(token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.habit = Habit.objects.create(
            place="Дом",
            time="22:00:00",
            action="Уборка",
            is_pleasant=False,
            pleasant_habit=None,
            period="DAILY",
            award="Ванна",
            time_to_complete="00:02:00",
            is_public=True,
            author=self.user
        )

    def test_get_habits(self):
        """Проверка отображения информации о привычках"""
        response = self.client.get(reverse("habits:habit_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['results'],
                         [{
                             'id': self.habit.id,
                             'place': self.habit.place,
                             'time': self.habit.time,
                             'action': self.habit.action,
                             'is_pleasant': self.habit.is_pleasant,
                             'period': self.habit.period,
                             'award': self.habit.award,
                             'time_to_complete': self.habit.time_to_complete,
                             'is_public': self.habit.is_public,
                             'author': self.habit.author_id,
                             'pleasant_habit': self.habit.pleasant_habit
                         }])

    def test_create_habit(self):
        """Проверка создания привычки"""
        data = {
            "id": 1,
            "place": "Дом",
            "time": "19:20:48",
            "action": "Попить воды",
            "is_pleasant": False,
            "period": "DAILY",
            "award": "Яблоко",
            "time_to_complete": "00:02:00",
            "is_public": False,
        }

        response = self.client.post(reverse("habits:habit_create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Habit.objects.all().count())
        self.assertTrue(Habit.objects.all().exists())

    def test_get_public_habits(self):
        """Проверка отображения публичных привычек"""
        response = self.client.get(reverse("habits:habit_list_public"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['results'],
                         [{
                             'id': self.habit.id,
                             'place': self.habit.place,
                             'time': self.habit.time,
                             'action': self.habit.action,
                             'is_pleasant': self.habit.is_pleasant,
                             'period': self.habit.period,
                             'award': self.habit.award,
                             'time_to_complete': self.habit.time_to_complete,
                             'is_public': self.habit.is_public,
                             'author': self.habit.author_id,
                             'pleasant_habit': self.habit.pleasant_habit
                         }])

    def test_get_habit_view_pk(self):
        """Проверка отображения отдельно выбраной привычки"""
        response = self.client.get(reverse("habits:habit_view", args=(self.habit.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {'id': self.habit.id,
                          'place': self.habit.place,
                          'time': self.habit.time,
                          'action': self.habit.action,
                          'is_pleasant': self.habit.is_pleasant,
                          'period': self.habit.period,
                          'award': self.habit.award,
                          'time_to_complete': self.habit.time_to_complete,
                          'is_public': self.habit.is_public,
                          'author': self.habit.author_id,
                          'pleasant_habit': self.habit.pleasant_habit})

    def test_update_habit(self):
        """Проверка обновления привычки"""
        data = {
            "place": self.habit.place,
            "time": self.habit.time,
            "action": "Упражняться",
            "is_pleasant": self.habit.is_pleasant,
            "period": self.habit.period,
            "award": self.habit.award,
            "time_to_complete": self.habit.time_to_complete,
            "is_public": self.habit.is_public,
        }

        response = self.client.put(reverse("habits:habit_update", args=(self.habit.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, data['action'])

    def test_check_duration_create_habit(self):
        """Проверка на создание привычки не более 2 минут"""
        data = {
            "place": self.habit.place,
            "time": self.habit.time,
            "action": self.habit.action,
            "is_pleasant": self.habit.is_pleasant,
            "period": self.habit.period,
            "award": self.habit.award,
            "time_to_complete": "00:04:00",
            "is_public": self.habit.is_public,
        }

        response = self.client.post(reverse("habits:habit_create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_pleasant_create_habit(self):
        """Проверка,что признак приятной привычки не имеет награды"""
        data = {
            "place": self.habit.place,
            "time": self.habit.time,
            "action": self.habit.action,
            "is_pleasant": True,
            "period": self.habit.period,
            "award": self.habit.award,
            "time_to_complete": self.habit.time_to_complete,
            "is_public": self.habit.is_public,
        }

        response = self.client.post(reverse("habits:habit_create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_normal_create_habit(self):
        """Проверка, что обычная привычка должна иметь награду или признак приятной привычки"""
        data = {
            "place": self.habit.place,
            "time": self.habit.time,
            "action": self.habit.action,
            "is_pleasant": self.habit.is_pleasant,
            "period": self.habit.period,
            "time_to_complete": self.habit.time_to_complete,
            "is_public": self.habit.is_public,
        }

        response = self.client.post(reverse("habits:habit_create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_habit(self):
        """Проверка удаления привычки"""
        response = self.client.delete(reverse("habits:habit_delete", args=(self.habit.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, Habit.objects.all().count())
