from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from words.models import SavedWord
from rest_framework.permissions import IsAuthenticated
from words.permissions import IsOwnerOfSaved, CanDeleteSaved
from words.serializers import SavedWordListSerializer, SaveWordCreateSerializer, \
    WordsGameSerializer


class SavedWordListAPIView(generics.ListAPIView):
    serializer_class = SavedWordListSerializer
    permission_classes = (IsOwnerOfSaved,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = SavedWord.objects.filter(user_id=user_id)
        return queryset


class SavedWordCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SavedWord.objects.all()
    serializer_class = SaveWordCreateSerializer


class DestroySavedWordAPIView(generics.DestroyAPIView):
    permission_classes = (CanDeleteSaved,)
    queryset = SavedWord.objects.all()


class GetGameAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # todo filters
        saved_words = SavedWord.objects.filter(user_id=request.user.id)[:10]

        serialized = WordsGameSerializer(saved_words, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
