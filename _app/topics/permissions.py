from rest_framework.permissions import BasePermission
from learning.models import SavedWord
from topics.models import Topic


class TopicIsSubtopic(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('subtopic_id')
        try:
            instance = Topic.objects.get(pk=pk)
            if instance.parent is not None:
                return True
        except Topic.DoesNotExist:
            return False

        return False
