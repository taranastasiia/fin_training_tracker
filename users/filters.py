from django_filters import FilterSet, ChoiceFilter
from users.models import User, Gender, UserRole


class UserFilter(FilterSet, ChoiceFilter):
    gender = ChoiceFilter(choices=Gender.choices, label='Gender')
    role = ChoiceFilter(choices=UserRole.choices, label='Role')

    class Meta:
        model = User
        fields = ['gender', 'role']