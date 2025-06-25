from workouts.views import WorkoutViewSet
from rest_framework.routers import SimpleRouter
from django.urls import path, include

router = SimpleRouter()
router.register('workouts', WorkoutViewSet)


urlpatterns = router.urls
