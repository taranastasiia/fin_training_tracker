from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserRole(models.TextChoices):
    ADMIN = 'admin',
    USER = 'user'


class Gender(models.TextChoices):
    MALE = 'male', 'Мужской'
    FEMALE = 'female', 'Женский'

class UserManager(BaseUserManager):
    def create_user(
            self,
            username,
            email,
            password=None,
            first_name="",
            last_name="",
            is_active=False
    ):
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
        )
        user.set_password(password)
        user.role = UserRole.USER.value
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            username,
            email,
            password=None
    ):
        user = self.model(
            username=username,
            email=email,
            password=password
        )
        user.role = UserRole.ADMIN.value
        user.save(using=self._db)
        return user


class User(AbstractUser, models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(choices=UserRole, max_length=10, default='user')
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    date_birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Рост в см")
    weight = models.FloatField(null=True, blank=True, help_text="Вес в кг")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser





