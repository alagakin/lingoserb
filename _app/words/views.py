from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from words.models import SavedWord
from words.serializers import SavedWordListSerializer


class SavedWordListAPIView(generics.ListAPIView):
    serializer_class = SavedWordListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = SavedWord.objects.filter(user_id=user_id)
        return queryset

