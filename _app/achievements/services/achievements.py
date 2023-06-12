from django.conf import settings

from learning.models import SavedWord, Lesson
from django.utils.translation import gettext as _

def calc_n_words(saved, n):
    studies = 0
    for s in saved:
        if s.repetition_count >= settings.REPETITIONS_TO_COMPLETE:
            studies += 1
    if studies >= n:
        return True
    return False


def calc_n_lessons(lessons, n):
    if len(lessons) >= n:
        return True
    return False


def calc_words_percent(saved, n):
    summ = 0
    saved = saved.order_by('-repetition_count')[0:n]
    for s in saved:
        summ += s.repetition_count

    max_repetitions = n * settings.REPETITIONS_TO_COMPLETE

    if summ >= max_repetitions:
        return 100
    else:
        return round(summ / max_repetitions * 100)


def calc_lessons_percent(lessons, n):
    summ = lessons.count()
    if summ >= n:
        return 100
    else:
        return round(summ / n * 100)


class Achievements:
    def __init__(self, user):
        self.user = user

    def get(self):
        saved = SavedWord.objects.filter(user=self.user, skipped=False)
        lessons = Lesson.objects.filter(user=self.user,
                                        finished_at__isnull=False)
        achievements = [
            {
                'id': 1,
                'title': _('5_words'),
                'achieved': calc_n_words(saved, 5)
            },
            {
                'id': 2,
                'title': _('10_words'),
                'achieved': calc_n_words(saved, 10),
                'percent': calc_words_percent(saved, 10)
            },
            {
                'id': 3,
                'title': _('50_words'),
                'achieved': calc_n_words(saved, 50),
                'percent': calc_words_percent(saved, 50),
            },
            {
                'id': 4,
                'title': _('250_words'),
                'achieved': calc_n_words(saved, 250),
                'percent': calc_words_percent(saved, 250),

            },
            {
                'id': 5,
                'title': _('1000_words'),
                'achieved': calc_n_words(saved, 1000),
                'percent': calc_words_percent(saved, 1000),
            },
            {
                'id': 6,
                'title': _('5000_words'),
                'achieved': calc_n_words(saved, 5000),
                'percent': calc_words_percent(saved, 5000),
            },
            {
                'id': 7,
                'title': _('1_lessons'),
                'achieved': calc_n_lessons(lessons, 1),
                'percent': calc_lessons_percent(lessons, 1),
            },
            {
                'id': 8,
                'title': _('5_lessons'),
                'achieved': calc_n_lessons(lessons, 5),
                'percent': calc_lessons_percent(lessons, 5),
            },
            {
                'id': 9,
                'title': _('10_lessons'),
                'achieved': calc_n_lessons(lessons, 10),
                'percent': calc_lessons_percent(lessons, 10),
            },
            {
                'id': 10,
                'title': _('50_lessons'),
                'achieved': calc_n_lessons(lessons, 50),
                'percent': calc_lessons_percent(lessons, 50),
            },
            {
                'id': 11,
                'title': _('100_lessons'),
                'achieved': calc_n_lessons(lessons, 100),
                'percent': calc_lessons_percent(lessons, 100),
            },
            {
                'id': 12,
                'title': _('500_lessons'),
                'achieved': calc_n_lessons(lessons, 500),
                'percent': calc_lessons_percent(lessons, 500),
            },
            {
                'id': 13,
                'title': _('1000_lessons'),
                'achieved': calc_n_lessons(lessons, 1000),
                'percent': calc_lessons_percent(lessons, 1000),
            },
            {
                'id': 14,
                'title': _('5000_lessons'),
                'achieved': calc_n_lessons(lessons, 5000),
                'percent': calc_lessons_percent(lessons, 5000),
            },
            {
                'id': 15,
                'title': _('10000_lessons'),
                'achieved': calc_n_lessons(lessons, 10000),
                'percent': calc_lessons_percent(lessons, 10000),
            }
        ]

        return achievements
