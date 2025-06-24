from enum import Enum
from rest_framework.permissions import BasePermission
from users.models import User


class DjangoViewAction(Enum):
    LIST = 'list'
    CREATE = 'create'
    RETRIEVE = 'retrieve'
    UPDATE = 'update'
    PARTIAL_UPDATE = 'partial_update'
    DELETE = 'destroy'


class CustomBasePermission(BasePermission):
    """
        Базовый permission-класс, разрешающий доступ:
        - админам ко всему,
        - к разрешённым действиям (`allowed_actions`) обычным пользователям,
        - к объектам, которыми владеет пользователь или если это он сам.
        """

    allowed_actions = [
        DjangoViewAction.LIST.value,
        DjangoViewAction.RETRIEVE.value,
        DjangoViewAction.CREATE.value,
        DjangoViewAction.UPDATE.value,
        DjangoViewAction.PARTIAL_UPDATE.value,
        DjangoViewAction.DELETE.value,
    ]

    def has_permission(self, request, view):
        # Разрешить всё админам
        if request.user and request.user.is_staff:
            return True

        # Если действие разрешено (по списку)
        if hasattr(view, 'action') and view.action in self.allowed_actions:
            return request.user and request.user.is_authenticated

        return False

    def has_object_permission(self, request, view, obj):
        # Админ всегда имеет доступ
        if request.user and request.user.is_staff:
            return True

        # Если объект — это сам пользователь
        if isinstance(obj, User) and obj == request.user:
            return True

        # Если у объекта есть поле user, и оно соответствует текущему пользователю
        if hasattr(obj, 'user') and obj.user == request.user:
            return True

        return False
