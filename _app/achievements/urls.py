from django.urls import path
from achievements.views import AchievementsAPIView

urlpatterns = [
    path('achievements/', AchievementsAPIView.as_view(), name='achievements')
]
