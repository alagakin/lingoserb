from django.urls import path
from words.views.achievements import AchievementsAPIView
from words.views.views import TextForWordAPIView, WordDetailAPIView, \
    WordsListAPIView

urlpatterns = [

    path('words/', WordsListAPIView.as_view(), name='word-list'),
    path('word/<int:pk>/', WordDetailAPIView.as_view(),
         name='word-detail'),
    path('text/for-word/<int:pk>/', TextForWordAPIView.as_view(),
         name='text-for-word'),

    path('achievements/', AchievementsAPIView.as_view(), name='achievements')
]
