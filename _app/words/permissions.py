from rest_framework.permissions import BasePermission

from words.models import SavedWord


class IsOwnerOfSaved(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id')
        return request.user.id == user_id


class CanDeleteSaved(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id')
        pk = view.kwargs.get('pk')
        try:
            instance = SavedWord.objects.get(pk=pk)
            if instance.user.id == user_id and user_id == request.user.id:
                return True
        except SavedWord.DoesNotExist:
            return False

        return False
