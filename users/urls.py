from users.views import UserViewSet, TokenAuthView, RegisterView, ChangePasswordView
from rest_framework.routers import SimpleRouter
from django.urls import path, include

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path("token-auth/", TokenAuthView.as_view(), name="token-auth"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
] + router.urls
