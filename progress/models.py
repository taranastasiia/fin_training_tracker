from datetime import timedelta
from django.db import models
from users.models import User



class WeeklyProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start_date = models.DateField()
    week_end_date = models.DateField()
    total_workouts = models.PositiveIntegerField(default=0)
    total_duration = models.PositiveIntegerField(default=0)
    total_calories = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'week_start_date')
        ordering = ['-week_start_date']

    def save(self, *args, **kwargs):
        if self.week_start_date and not self.week_end_date:
            self.week_end_date = self.week_start_date + timedelta(days=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Progress {self.user} for week starting {self.week_start_date}"

