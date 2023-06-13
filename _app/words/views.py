from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from words.models import Word
from rest_framework.permissions import IsAuthenticated
from words.serializers import TextsOfWithWordSerializer, \
    WordTranslationSerializer


class TextForWordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            word = Word.objects.get(pk=kwargs['pk'])
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized = TextsOfWithWordSerializer(word,
                                               context={'request': request})
        if not serialized.data:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)


class WordDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            word = Word.objects.get(pk=kwargs['pk'])
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized = WordTranslationSerializer(word)
        return Response(serialized.data, status=status.HTTP_200_OK)


class WordsListAPIView(generics.ListAPIView):
    serializer_class = WordTranslationSerializer
    queryset = Word.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = Word.objects.all()

        topic_ids = self.request.query_params.getlist('topics')

        if topic_ids and topic_ids[0] != '':
            topic_ids = topic_ids[0].split(',')
            queryset = queryset.filter(topics__in=topic_ids)

        return queryset
