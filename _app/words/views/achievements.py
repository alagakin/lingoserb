from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from words.services.achievements import Achievements


class AchievementsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        achievements = Achievements(request.user)
        return Response(achievements.get(), status=status.HTTP_200_OK)


