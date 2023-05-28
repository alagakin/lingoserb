from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime, timedelta

from learning.models import SavedWord
from learning.utils import topic_to_saved
from topics.models import Topic

now = datetime.now()

one_day_ago = now - timedelta(days=1)
three_days_ago = now - timedelta(days=3)
week_ago = now - timedelta(days=7)
month_ago = now - timedelta(days=30)


class CardsGame():
    def __init__(self, user_id: int, topic: Topic):
        self.user = get_user_model().objects.get(id=user_id)
        self.topic = topic
        topic_to_saved(user=self.user, topic=self.topic)

    def get_words(self):
        return SavedWord.objects.filter(user=self.user,
                                        skipped=False,
                                        word__topics__exact=self.topic).filter(
            Q(repetition_count__in=[1, 2], last_repetition__lte=one_day_ago) |
            Q(repetition_count__in=[3], last_repetition__lte=three_days_ago) |
            Q(repetition_count__in=[4], last_repetition__lte=week_ago) |
            Q(repetition_count__gte=5, last_repetition__lte=month_ago) |
            Q(last_repetition=None)
        ).order_by('repetition_count')[:settings.WORDS_PER_ITERATION]
