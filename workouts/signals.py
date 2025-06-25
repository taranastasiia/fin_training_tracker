from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from workouts.models import Workout
from progress.models import WeeklyProgress
from datetime import timedelta
from django.db.models import Sum


def update_user_weekly_progress(user, workout_date):
    """Агрегирует данные по тренировкам пользователя за неделю"""
    week_start = workout_date - timedelta(days=workout_date.weekday())
    week_end = week_start + timedelta(days=6)

    workouts = Workout.objects.filter(
        user=user,
        date__range=[week_start, week_end]
    )

    total_workouts = workouts.count()
    total_duration = workouts.aggregate(total=Sum('duration_minutes'))['total'] or 0
    total_calories = workouts.aggregate(total=Sum('calories_burned'))['total'] or 0

    WeeklyProgress.objects.update_or_create(
        user=user,
        week_start_date=week_start,
        defaults={
            'week_end_date': week_end,
            'total_workouts': total_workouts,
            'total_duration': total_duration,
            'total_calories': total_calories,
        }
    )


@receiver(post_save, sender=Workout)
def workout_created_or_updated(sender, instance, **kwargs):
    print(">> Обновление WeeklyProgress после сохранения тренировки")
    update_user_weekly_progress(instance.user, instance.date)

@receiver(post_delete, sender=Workout)
def workout_deleted(sender, instance, **kwargs):
    update_user_weekly_progress(instance.user, instance.date)