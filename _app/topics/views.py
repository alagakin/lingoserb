from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from topics.models import Topic
from topics.serializers import TopicSerializer, TopicWordsSerializer, \
    TopicTextsSerializer
from words.models import SavedWord, Word
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class TopicsListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Topic.objects.filter(parent_id=None)
    serializer_class = TopicSerializer

    @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RetrieveTopicsAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicWordsAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Topic.objects.all()
    serializer_class = TopicWordsSerializer


class TopicTextsAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Topic.objects.all()
    serializer_class = TopicTextsSerializer


class SaveWordsFromTopicAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            topic = Topic.objects.get(pk=kwargs['pk'])
            saved_words = [saved_word.word for saved_word in
                           SavedWord.objects.filter(user=request.user)]

            topic_words = Word.objects.filter(topics=topic)

            for word in topic_words:
                if word not in saved_words:
                    try:
                        SavedWord.objects.create(user=request.user, word=word)
                    except IntegrityError:
                        existing_saved_word = SavedWord.all_objects.get(
                            user=request.user, word=word)
                        existing_saved_word.deleted = False
                        existing_saved_word.save(update_fields=['deleted'])

            return Response(None, status=status.HTTP_201_CREATED)

        except Topic.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
