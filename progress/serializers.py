from rest_framework.serializers import ModelSerializer, Serializer, IntegerField, ValidationError
from progress.models import WeeklyProgress


class WeeklyProgressSerializer(ModelSerializer):
    class Meta:
        model = WeeklyProgress
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_week_start_date(self, value):
        if value.weekday() != 0:
            raise ValidationError("Week start date must be a Monday")
        return value

    def validate_week_end_date(self, value):
        if value.weekday() != 6:
            raise ValidationError("Week end date must be a Sunday")
        return value



class ProgressOverviewSerializer(Serializer):
    current_week = WeeklyProgressSerializer()
    last_week = WeeklyProgressSerializer(allow_null=True)
    total_workouts = IntegerField()
    total_duration = IntegerField()
    total_calories = IntegerField()
