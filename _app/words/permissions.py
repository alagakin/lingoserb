from rest_framework.permissions import BasePermission


class IsOwnerOfSaved(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id')
        return request.user.id == user_id
