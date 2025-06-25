from rest_framework.serializers import ModelSerializer
from workouts.models import Workout


class WorkoutSerializer(ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)