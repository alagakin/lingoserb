from rest_framework.permissions import BasePermission

from learning.models import SavedWord


class UserOwsSavedWord(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        try:
            instance = SavedWord.objects.get(pk=pk)
            if instance.user.id == request.user.id:
                return True
        except SavedWord.DoesNotExist:
            return False

        return False
