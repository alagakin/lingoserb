import json

import meilisearch.errors

from django.conf import settings
from meilisearch import Client
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


class WordsSearchAPIView(APIView):
    serializer_class = WordTranslationSerializer
    permission_classes = (IsAuthenticated,)

    def get_all_words(self, request):
        words = Word.objects.all()

        topic_ids = request.query_params.getlist('topics')
        if topic_ids and topic_ids[0] != '':
            topic_ids = topic_ids[0].split(',')
            words = words.filter(topics__in=topic_ids)

        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 10))
        words = words[offset:offset + limit]

        serialized = WordTranslationSerializer(words, many=True,
                                               context={'request': request})

        return Response(serialized.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)
        try:
            if not query:
                return self.get_all_words(request)

            limit = int(request.query_params.get('limit', 10))
            offset = int(request.query_params.get('offset', 0))

            client = Client(settings.MEILISEARCH_URL, settings.MEILISEARCH_KEY)
            index = client.index('words')
            search_results = index.search(query, {'limit': limit, 'offset': offset})

            ids = [int(result['id']) for result in search_results['hits']]

            words = Word.objects.filter(pk__in=ids)

            topic_ids = request.query_params.getlist('topics')
            if topic_ids and topic_ids[0] != '':
                topic_ids = topic_ids[0].split(',')
                words = words.filter(topics__in=topic_ids)

            serialized = WordTranslationSerializer(words, many=True, context={'request': request})

            return Response(serialized.data, status=status.HTTP_200_OK)

        except meilisearch.errors.MeilisearchError as e:
            return Response({
                'error': e.message,
            }, status=status.HTTP_400_BAD_REQUEST)
