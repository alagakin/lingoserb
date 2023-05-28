from django.urls import path

from game.views import GetGameAPIView, SuccessRepetitionAPIView

urlpatterns = [
    path('game/topic/<int:topic_id>/', GetGameAPIView.as_view(), name='get-game'),
    path('game/word/<int:word_id>/success/', SuccessRepetitionAPIView.as_view(),
         name='success-repetition'),
]
