from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from progress.models import WeeklyProgress
from progress.serializers import ProgressOverviewSerializer
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from progress.serializers import WeeklyProgressSerializer


class ProgressOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get_default_week_data(self, week_start):
        return {
            'week_start_date': week_start,
            'week_end_date': week_start + timedelta(days=6),
            'total_workouts': 0,
            'total_duration': 0,
            'total_calories': 0,
        }

    @swagger_auto_schema(
        operation_description="Получить сводку прогресса по неделям",
        responses={200: ProgressOverviewSerializer}
    )

    def get(self, request):
        user = request.user
        today = now().date()
        current_week_start = today - timedelta(days=today.weekday())
        last_week_start = current_week_start - timedelta(days=7)

        current_week = WeeklyProgress.objects.filter(
            user=user,
            week_start_date=current_week_start
        ).first()
        last_week = WeeklyProgress.objects.filter(
            user=user,
            week_start_date=last_week_start
        ).first()

        totals = WeeklyProgress.objects.filter(user=user).aggregate(
            total_workouts=Sum('total_workouts', default=0),
            total_duration=Sum('total_duration', default=0),
            total_calories=Sum('total_calories', default=0)
        )

        data = {
            'current_week': current_week or self.get_default_week_data(current_week_start),
            'last_week': last_week,
            'total_workouts': totals['total_workouts'] or 0,
            'total_duration': totals['total_duration'] or 0,
            'total_calories': totals['total_calories'] or 0,
        }

        serializer = ProgressOverviewSerializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeeklyProgressPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class WeeklyProgressViewSet(ReadOnlyModelViewSet):
    serializer_class = WeeklyProgressSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = WeeklyProgressPagination


    def get_queryset(self):
        return WeeklyProgress.objects.filter(user=self.request.user).order_by('-week_start_date')

    @swagger_auto_schema(
        operation_description="Список истории прогресса с пагинацией",
        responses={200: WeeklyProgressSerializer(many=True)}
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)