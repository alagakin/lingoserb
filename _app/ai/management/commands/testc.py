import os

import openai
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import json

from learn_serbian.utils import transliterate
from words.models import Word, Text, TextTranslation
import logging
from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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
logger = logging.getLogger('openai')


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        one_day_ago = now - timedelta(days=1)
        three_days_ago = now - timedelta(days=3)
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        topic = Topic.objects.get(id=16)
        sv = SavedWord.objects.filter(user=get_user_model().objects.first(), skipped=False,
                                 word__topics__exact=topic) \
            .filter(
            Q(repetition_count__in=[1, 2], last_repetition__lte=one_day_ago) |
            Q(repetition_count__in=[3], last_repetition__lte=three_days_ago) |
            Q(repetition_count__in=[4], last_repetition__lte=week_ago) |
            Q(repetition_count__gte=5, last_repetition__lte=month_ago) |
            Q(last_repetition=None) | Q(repetition_count=0)
        ).order_by('repetition_count')

        already_saved_words_ids = [
            saved_word.word.id for saved_word in sv
        ]

        yet_not_saved_words = Word.objects.filter(
            topics__exact=topic,
        ).exclude(
            id__in=already_saved_words_ids
        )
        # print(already_saved_words_ids)
