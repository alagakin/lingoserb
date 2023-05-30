from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from learning.exceptions import EmptyLessonException
from words.models import Word
from datetime import datetime, timedelta

from learning.models import Lesson, SavedWord
from learning.utils import topic_to_saved
from topics.models import Topic
from topics.permissions import TopicIsSubtopic
from learning.serializers import (
    SavedWordListSerializer,
    SaveWordCreateSerializer,
    SavedWordsIds,
    ProgressSerializer, LessonSerializer,
)
from words.serializers import WordsWithTexts, WordSerializer


class SavedWordListAPIView(generics.ListAPIView):
    serializer_class = SavedWordListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = SavedWord.objects.filter(user_id=user_id)
        return queryset


class SavedWordCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = SavedWord.objects.all()
    serializer_class = SaveWordCreateSerializer

    def post(self, request, *args, **kwargs):
        if "word" not in request.data:
            return Response("word is required",
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            saved_word = SavedWord(user=request.user,
                                   word_id=request.data["word"])
            saved_word.save()
            return Response(None, status=status.HTTP_201_CREATED)
        except IntegrityError:
            saved_word = SavedWord.all_objects.get(
                user=request.user, word_id=request.data["word"]
            )
            saved_word.deleted = False
            saved_word.save(update_fields=["deleted"])
            return Response(None, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class DestroySavedWordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        # todo use serializers
        try:
            saved_word = SavedWord.objects.get(
                user_id=request.user.id, word_id=request.data.get("word")
            )
            saved_word.delete()
        except SavedWord.DoesNotExist:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SavedWordsIDSAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        saved_words = SavedWord.objects.filter(user=request.user.id)
        serialized = SavedWordsIds(saved_words, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class ProgressAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        cache_key = "progress-" + str(request.user.id)
        data = cache.get(cache_key)
        if data is None:
            progress = SavedWord.objects.all()
            serialized = ProgressSerializer(progress, many=True)
            data = serialized.data
            cache.set(cache_key, data, 60)

        return Response(data, status=status.HTTP_200_OK)


class WatchedWordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            saved_word = SavedWord.objects.get(
                word_id=kwargs["word_id"], user=request.user
            )
        except SavedWord.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        saved_word.watched_count += 1
        saved_word.watched_at = timezone.now()
        saved_word.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SkipWordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            saved_word = SavedWord.objects.get(
                user=request.user, word_id=kwargs["word_id"]
            )
            if saved_word.skipped:
                saved_word.skipped = False
                saved_word.save()
                return Response(False, status=status.HTTP_204_NO_CONTENT)

            else:
                saved_word.skipped = True
                saved_word.save()
                return Response(True, status=status.HTTP_204_NO_CONTENT)

        except SavedWord.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


class LearnTopicAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            topic = Topic.objects.get(id=kwargs["topic_id"])
        except Topic.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

        try:
            lesson = Lesson.objects.get(user=request.user, topic=topic,
                                        finished_at=None)
            if lesson.saved_words.count() == 0:
                lesson.delete()
                raise EmptyLessonException

            serialized = LessonSerializer(lesson)
            return Response(serialized.data,
                            status=status.HTTP_200_OK)
        except (Lesson.DoesNotExist, EmptyLessonException):
            lesson = Lesson(
                user=request.user,
                topic=topic
            )
            lesson.save()

            saved_words = self.get_saved_words(request.user, topic)

            already_saved_words_ids = self.get_already_saved_words_ids(topic,
                                                                       request.user)

            yet_not_saved_words = Word.objects.filter(
                topics__exact=topic,
            ).exclude(
                id__in=already_saved_words_ids
            )

            if yet_not_saved_words.count() > settings.WORDS_PER_ITERATION:
                self.attach_from_words(yet_not_saved_words, lesson,
                                       request.user)
            elif yet_not_saved_words.count() == 0:
                self.attach_from_saved(saved_words, lesson)
            else:
                self.attach_from_words_and_saved(yet_not_saved_words,
                                                 saved_words, lesson,
                                                 request.user)

            serialized = LessonSerializer(lesson)

            return Response(serialized.data,
                            status=status.HTTP_200_OK)

    def get_already_saved_words_ids(self, topic, user):
        saved_words = SavedWord.objects.filter(user=user,
                                               word__topics__exact=topic)

        return [saved_word.word.id for saved_word in saved_words]

    def get_saved_words(self, user, topic):
        now = timezone.make_aware(datetime.now(),
                                  timezone.get_current_timezone())

        one_day_ago = now - timedelta(days=1)
        three_days_ago = now - timedelta(days=3)
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        return SavedWord.objects.filter(user=user, skipped=False,
                                        word__topics__exact=topic) \
            .filter(
            Q(repetition_count__in=[1, 2], last_repetition__lte=one_day_ago) |
            Q(repetition_count__in=[3], last_repetition__lte=three_days_ago) |
            Q(repetition_count__in=[4], last_repetition__lte=week_ago) |
            Q(repetition_count__gte=5, last_repetition__lte=month_ago) |
            Q(last_repetition=None) | Q(repetition_count=0)
        ).order_by('repetition_count')[0:settings.WORDS_PER_ITERATION]

    def attach_from_words(self, words, lesson, user):
        for word in words[0:settings.WORDS_PER_ITERATION]:
            try:
                saved_word = SavedWord(
                    word=word,
                    user=user
                )
                saved_word.save()
            except IntegrityError:
                saved_word = SavedWord.objects.get(word=word, user=user)

            lesson.saved_words.add(saved_word)

        lesson.save()

    def attach_from_words_and_saved(self, words, saved_words, lesson, user):
        count = 0
        for word in words:
            try:
                saved_word = SavedWord(
                    word=word,
                    user=user
                )
                saved_word.save()
            except IntegrityError:
                saved_word = SavedWord.objects.get(word=word, user=user)

            lesson.saved_words.add(saved_word)
            count += 1

        remaining_count = settings.WORDS_PER_ITERATION - count
        for saved in saved_words[0:remaining_count]:
            lesson.saved_words.add(saved)
        lesson.save()

    def attach_from_saved(self, saved_words, lesson):
        for saved in saved_words:
            lesson.saved_words.add(saved)
        lesson.save()
