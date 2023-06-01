from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from learning.models import SavedWord


class AchievementsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        achievements = Achievements(request.user)
        return Response(achievements.get(), status=status.HTTP_200_OK)


class Achievements:
    def __init__(self, user):
        self.user = user

    def get(self):
        saved = SavedWord.objects.filter(user=self.user)
        achievements = [
            {
                'id': 1,
                'title': '5 words',
                'achieved': self.calc_n_words(saved, 5)
            },
            {
                'id': 2,
                'title': '10 words',
                'achieved': self.calc_n_words(saved, 10)
            },
            {
                'id': 3,
                'title': '50 words',
                'achieved': self.calc_n_words(saved, 50)
            },
            {
                'id': 4,
                'title': '250 words',
                'achieved': self.calc_n_words(saved, 250)
            },
            {
                'id': 5,
                'title': '1000 words',
                'achieved': self.calc_n_words(saved, 1000)
            },
            {
                'id': 6,
                'title': '5000 words',
                'achieved': self.calc_n_words(saved, 5000)
            },
        ]

        return achievements

    def calc_n_words(self, saved, n):
        studies = 0
        for s in saved:
            if s.repetition_count > 0:
                studies += 1
        if studies > n:
            return True
        return False
