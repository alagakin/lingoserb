from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from words.models import SavedWord
from rest_framework.permissions import IsAuthenticated
from words.permissions import UserOwsSavedWord
from learning.serializers import WordsGameSerializer
from words.services.games import CardsGame


class GetGameAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        game = CardsGame(request.user.id)
        saved_words = game.get_saved_words()

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
