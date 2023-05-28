from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from game.serializers import WordsGameSerializer
from game.services.games import CardsGame
from learning.models import SavedWord
from topics.models import Topic


class GetGameAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            topic = Topic.objects.get(id=kwargs['topic_id'])
            game = CardsGame(request.user.id, topic)
            words = game.get_words()

            serialized = WordsGameSerializer(words, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Topic.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


class SuccessRepetitionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            saved_word = SavedWord.objects.get(word_id=kwargs['word_id'],
                                               user=request.user)
        except SavedWord.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        saved_word.repetition_count += 1
        saved_word.last_repetition = timezone.now()
        saved_word.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
