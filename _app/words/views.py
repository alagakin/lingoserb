from rest_framework import generics
from words.models import SavedWord
from rest_framework.permissions import IsAuthenticated
from words.permissions import IsOwnerOfSaved
from words.serializers import SavedWordListSerializer, SaveWordCreateSerializer


class SavedWordListAPIView(generics.ListAPIView):
    serializer_class = SavedWordListSerializer
    permission_classes = (IsOwnerOfSaved, )

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = SavedWord.objects.filter(user_id=user_id)
        return queryset


class SavedWordCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = SavedWord.objects.all()
    serializer_class = SaveWordCreateSerializer
