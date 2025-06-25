from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsWorkoutOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_staff or obj.user == request.user
        return obj.user == request.user