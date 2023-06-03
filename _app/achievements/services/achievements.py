from learning.models import SavedWord, Lesson


def calc_n_words(saved, n):
    studies = 0
    for s in saved:
        if s.repetition_count > 0:
            studies += 1
    if studies > n:
        return True
    return False


def calc_n_lessons(lessons, n):
    if len(lessons) > n:
        return True
    return False


class Achievements:
    def __init__(self, user):
        self.user = user

    def get(self):
        saved = SavedWord.objects.filter(user=self.user)
        lessons = Lesson.objects.filter(user=self.user)
        achievements = [
            {
                'id': 1,
                'title': '5 words',
                'achieved': calc_n_words(saved, 5)
            },
            {
                'id': 2,
                'title': '10 words',
                'achieved': calc_n_words(saved, 10)
            },
            {
                'id': 3,
                'title': '50 words',
                'achieved': calc_n_words(saved, 50)
            },
            {
                'id': 4,
                'title': '250 words',
                'achieved': calc_n_words(saved, 250)
            },
            {
                'id': 5,
                'title': '1000 words',
                'achieved': calc_n_words(saved, 1000)
            },
            {
                'id': 6,
                'title': '5000 words',
                'achieved': calc_n_words(saved, 5000)
            },
            {
                'id': 7,
                'title': '1 lesson',
                'achieved': calc_n_lessons(lessons, 1)
            },
            {
                'id': 8,
                'title': '5 lessons',
                'achieved': calc_n_lessons(lessons, 5)
            },
            {
                'id': 9,
                'title': '10 lessons',
                'achieved': calc_n_lessons(lessons, 10)
            },
            {
                'id': 10,
                'title': '50 lessons',
                'achieved': calc_n_lessons(lessons, 50)
            },
            {
                'id': 11,
                'title': '100 lessons',
                'achieved': calc_n_lessons(lessons, 100)
            },
            {
                'id': 12,
                'title': '500 lessons',
                'achieved': calc_n_lessons(lessons, 500)
            },
            {
                'id': 13,
                'title': '1000 lessons',
                'achieved': calc_n_lessons(lessons, 1000)
            },
            {
                'id': 14,
                'title': '5000 lessons',
                'achieved': calc_n_lessons(lessons, 5000)
            },
            {
                'id': 15,
                'title': '10000 lessons',
                'achieved': calc_n_lessons(lessons, 10000)
            }
        ]

        return achievements
