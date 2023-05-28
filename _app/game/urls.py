from django.urls import path

from game.views import GetGameAPIView, SuccessRepetitionAPIView

urlpatterns = [
    path('game/', GetGameAPIView.as_view(), name='get-game'),
    path('game/<int:word_id>/success/', SuccessRepetitionAPIView.as_view(),
         name='success-repetition'),
]
