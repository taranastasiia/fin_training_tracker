from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer
from rest_framework.views import APIView
from users.service import UserService
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


class TokenAuthView(APIView):

    def post(self, request):
        user = UserService(request)

        data = user.authenticate_user(request.data)
        return Response(data, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        user = UserService(request)
        data =