from django.db import models
from users.models import User


class CategoryType(models.TextChoices):
    CARDIO = 'cardio', 'Кардио'
    STRENGTH = 'strength', 'Силовая'
    FLEXIBILITY = 'flexibility', 'Растяжка'
    YOGA = 'yoga', 'Йога'
    OTHER = 'other', 'Другое'


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_user')
    category = models.CharField(max_length=20, choices=CategoryType.choices, default=CategoryType.OTHER)
    title = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.user.username})"
