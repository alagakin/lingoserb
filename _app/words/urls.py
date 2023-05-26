from django.urls import path

from words.views.achievements import AchievementsAPIView
from words.views.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, \
    TextForWordAPIView, WordDetailAPIView, WordsListAPIView, \
    SavedWordsIDSAPIView, ProgressAPIView

urlpatterns = [
    path('saved/', SavedWordListAPIView.as_view(),
         name='saved-word-list'),
    path('saved/ids/', SavedWordsIDSAPIView.as_view(), name='saved-words-ids'),
    path('saved/add/', SavedWordCreateAPIView.as_view(),
         name='saved-word-create'),
    path('saved/delete/',
         DestroySavedWordAPIView.as_view(),
         name='saved-word-destroy'),
    path('words/', WordsListAPIView.as_view(), name='word-list'),
    path('word/<int:pk>/', WordDetailAPIView.as_view(),
         name='word-detail'),
    path('text/for-word/<int:pk>/', TextForWordAPIView.as_view(),
         name='text-for-word'),
    path('saved/progress/',
         ProgressAPIView.as_view(),
         name='saved-progress'),
    path('achievements/', AchievementsAPIView.as_view(), name='achievements')
]
