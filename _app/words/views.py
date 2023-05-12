from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from words.models import SavedWord, Word
from rest_framework.permissions import IsAuthenticated
from words.permissions import IsOwnerOfSaved, UserOwsSavedWord
from words.serializers import SavedWordListSerializer, SaveWordCreateSerializer, \
    WordsGameSerializer, TextSerializer, TextsOfWithWordSerializer


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
    permission_classes = (UserOwsSavedWord,)
    queryset = SavedWord.objects.all()


class GetGameAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # todo filters
        saved_words = SavedWord.objects.filter(user_id=request.user.id)[:10]

        serialized = WordsGameSerializer(saved_words, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class SuccessRepetitionAPIView(APIView):
    permission_classes = (UserOwsSavedWord,)

    def patch(self, request, *args, **kwargs):
        saved_word = SavedWord.objects.get(id=kwargs['pk'])
        saved_word.repetition_count += 1
        saved_word.last_repetition = timezone.now()
        saved_word.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TextForWordAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            word = Word.objects.get(pk=kwargs['pk'])
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized = TextsOfWithWordSerializer(word)
        if not serialized.data:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)