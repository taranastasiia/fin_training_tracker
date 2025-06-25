from django.urls import path, include
from progress.views import ProgressOverviewView, ProgressOverviewSerializer, WeeklyProgressViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('history', WeeklyProgressViewSet, basename='weeklyprogress')

urlpatterns = [
    path('progress/overview', ProgressOverviewView.as_view(), name='progress-overview'),
    path('progress/', include(router.urls))
]