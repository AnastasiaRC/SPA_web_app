import datetime
from rest_framework import serializers
from habits.models import Habit


class HabitsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        habit = Habit.objects.create(**validated_data)
        if habit.time_to_complete > datetime.time(minute=2):
            raise serializers.ValidationError("Продолжительность не должна превышать 2 минуты")
        if habit.is_pleasant is False:
            if not habit.award:
                if not habit.pleasant_habit:
                    raise serializers.ValidationError(
                        "Обычная привычка должна иметь награду или признак приятной привычки!")
            else:
                if habit.pleasant_habit:
                    raise serializers.ValidationError(
                        "Обычная привычка не должна иметь награду и признак приятной привычки одновременно!")
            return habit
        else:
            if habit.award:
                raise serializers.ValidationError("Признак приятной привычки не может иметь награды!")
            return habit

    class Meta:
        model = Habit
        fields = "__all__"
