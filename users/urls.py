from users.views import UserViewSet, TokenAuthView
from rest_framework.routers import SimpleRouter
from django.urls import path, include

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path("token-auth/", TokenAuthView.as_view(), name="token-auth")
] + router.urls
