from django.db.models import Q
from datetime import datetime, timedelta
from words.models import SavedWord

now = datetime.now()

one_day_ago = now - timedelta(days=1)
three_days_ago = now - timedelta(days=3)
week_ago = now - timedelta(days=7)
month_ago = now - timedelta(days=30)


class CardsGame():
    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_saved_words(self):
        return SavedWord.objects.filter(user_id=self.user_id).filter(
            Q(repetition_count__in=[1, 2], last_repetition__lte=one_day_ago) |
            Q(repetition_count__in=[3], last_repetition__lte=three_days_ago) |
            Q(repetition_count__in=[4], last_repetition__lte=week_ago) |
            Q(repetition_count__gte=5, last_repetition__lte=month_ago) |
            Q(last_repetition=None)
        ).order_by('repetition_count')[:10]