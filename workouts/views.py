from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from workouts.models import Workout
from workouts.serializers import WorkoutSerializer
from workouts.permissions import IsWorkoutOwnerOrAdmin
from workouts.filters import WorkoutFilter
from drf_yasg.utils import swagger_auto_schema


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


    @swagger_auto_schema(
        operation_description="Получить список тренировок пользователя с фильтрацией, поиском и сортировкой",
        responses={200: WorkoutSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить детали тренировки",
        responses={200: WorkoutSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую тренировку",
        request_body=WorkoutSerializer,
        responses={201: WorkoutSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить тренировку (полное обновление)",
        request_body=WorkoutSerializer,
        responses={200: WorkoutSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление тренировки",
        request_body=WorkoutSerializer,
        responses={200: WorkoutSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить тренировку",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
