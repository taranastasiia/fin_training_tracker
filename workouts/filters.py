from datetime import timezone, timedelta
from django_filters import FilterSet, DateFilter, CharFilter, BooleanFilter
from workouts.models import Workout


class WorkoutFilter(FilterSet):
    date_from = DateFilter(flavor='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')
    category = CharFilter(field_name='category')
    last_week = BooleanFilter(method='filter_last_week')

    class Meta:
        model = Workout
        fields = ['category', 'date_from', 'date_to', 'title']

    def filter_last_week(self, queryset, name, value):
        if value:
            today = timezone.now().date()
            start_date = today - timedelta(days=7)
            return queryset.filter(date__gte=start_date)
        return queryset