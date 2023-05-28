from django.urls import path

from learning.views import SavedWordListAPIView, SavedWordsIDSAPIView, \
    SavedWordCreateAPIView, \
    DestroySavedWordAPIView, ProgressAPIView, SkipWordAPIView, \
    WatchedWordAPIView, LearnTopicAPIView

urlpatterns = [
    path('saved/', SavedWordListAPIView.as_view(),
         name='saved-word-list'),
    path('saved/ids/', SavedWordsIDSAPIView.as_view(), name='saved-words-ids'),
    path('saved/add/', SavedWordCreateAPIView.as_view(),
         name='saved-word-create'),
    path('saved/delete/',
         DestroySavedWordAPIView.as_view(),
         name='saved-word-destroy'),
    path('saved/progress/',
         ProgressAPIView.as_view(),
         name='saved-progress'),
    path('learning/<int:word_id>/skip/', SkipWordAPIView.as_view(),
         name='skip-word'),
    path('learning/<int:word_id>/watched/', WatchedWordAPIView.as_view(),
         name='watched-word'),
    path('learning/<int:topic_id>/start/', LearnTopicAPIView.as_view(),
         name='learn-topic')
]
