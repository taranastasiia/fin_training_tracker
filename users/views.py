from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer, ChangePasswordSerializer, RegisterSerializer
from rest_framework.views import APIView
from users.service import UserService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import UserPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.filters import UserFilter
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = UserFilter
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class TokenAuthView(APIView):
    @swagger_auto_schema(
        operation_description="Аутентификация пользователя и получение токена",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response('Токен успешно получен', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'token': openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            401: 'Ошибка аутентификации'
        }
    )
    def post(self, request):
        user = UserService(request)
        data = user.authenticate_user(request.data)
        if 'error' in data:
            return Response({'error': data['error'], 'details': data.get('details')},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response(data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        request_body=UserSerializer,
        responses={
            201: openapi.Response('Пользователь успешно зарегистрирован', UserSerializer),
            400: 'Ошибка валидации данных'
        }
    )
    def post(self, request):
        user = UserService(request)
        data = user.register_user(request.data)

        if 'error' in data:
            return Response({'error': data['error'], 'details': data.get('details')},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Смена пароля пользователя",
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response('Пароль успешно изменён', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                    'new_token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )),
            400: 'Ошибка валидации или неправильный старый пароль'
        }
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            Token.objects.filter(user=user).delete()
            new_token = Token.objects.create(user=user)

            return Response({'status': 'Password successfully updated', 'new_token': new_token.key},
                            status=status.HTTP_200_OK )
        return Response(serializer.errors, status=400)
