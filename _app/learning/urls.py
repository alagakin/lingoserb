from django.urls import path

from learning.views import GetGameAPIView, SuccessRepetitionAPIView

urlpatterns = [
    path('game/', GetGameAPIView.as_view(), name='get-game'),
    path('game/<int:pk>/success/', SuccessRepetitionAPIView.as_view(),
         name='success-repetition'),
]
