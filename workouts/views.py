from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from workouts.models import Workout
from workouts.serializers import WorkoutSerializer
from workouts.permissions import IsWorkoutOwnerOrAdmin
from workouts.filters import WorkoutFilter


class WorkoutViewSet(ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated, IsWorkoutOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = WorkoutFilter
    search_fields = ['title', 'category']
    ordering = ['-date']


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Workout.objects.all()
        return Workout.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


