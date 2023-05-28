from django.urls import path

from learning.views import GetGameAPIView, SuccessRepetitionAPIView, \
    SavedWordListAPIView, SavedWordsIDSAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, ProgressAPIView, SkipWordAPIView, \
    StartLearningAPIView, WatchedWordAPIView

urlpatterns = [
    path('game/', GetGameAPIView.as_view(), name='get-game'),
    path('game/<int:word_id>/success/', SuccessRepetitionAPIView.as_view(),
         name='success-repetition'),
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
    path('learning/<int:subtopic_id>/', StartLearningAPIView.as_view(),
         name='start-learning'),
    path('learning/<int:word_id>/watched/', WatchedWordAPIView.as_view(),
         name='watched-word'),
]
