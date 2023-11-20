import datetime
from rest_framework import serializers
from habits.models import Habit


class HabitsSerializer(serializers.ModelSerializer):
    pleasant_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.filter(is_pleasant=True),
                                                        allow_null=True, required=False)

    def validate(self, validated_data):
        is_pleasant = validated_data.get('is_pleasant')
        time_to_complete = validated_data.get('time_to_complete')
        pleasant_habit = validated_data.get('pleasant_habit')
        award = validated_data.get('award')
        if time_to_complete > datetime.time(minute=2):
            raise serializers.ValidationError("Продолжительность не должна превышать 2 минуты")
        elif is_pleasant is False:
            if not award:
                if not pleasant_habit:
                    raise serializers.ValidationError(
                        "Обычная привычка должна иметь награду или признак приятной привычки!")
            elif pleasant_habit:
                raise serializers.ValidationError(
                    "Обычная привычка не должна иметь награду и признак приятной привычки одновременно!")
            return validated_data
        elif award:
            raise serializers.ValidationError("Признак приятной привычки не может иметь награды!")
        return validated_data

    class Meta:
        model = Habit
        fields = "__all__"
