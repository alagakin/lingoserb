from django.urls import path

from learning.views import SavedWordListAPIView, SavedWordsIDSAPIView, \
    DestroySavedWordAPIView, ProgressAPIView, SkipWordAPIView, \
    LearnTopicAPIView, CompleteLessonAPIView, GetGraphAPIView

urlpatterns = [
    path('saved/', SavedWordListAPIView.as_view(),
         name='saved-word-list'),
    path('saved/ids/', SavedWordsIDSAPIView.as_view(), name='saved-words-ids'),
    path('saved/delete/',
         DestroySavedWordAPIView.as_view(),
         name='saved-word-destroy'),
    path('saved/progress/',
         ProgressAPIView.as_view(),
         name='saved-progress'),
    path('learning/<int:word_id>/skip/', SkipWordAPIView.as_view(),
         name='skip-word'),
    path('learning/<int:topic_id>/start/', LearnTopicAPIView.as_view(),
         name='learn-topic'),
    path('learning/<int:topic_id>/complete/', CompleteLessonAPIView.as_view(),
         name='complete-lesson'),
    path('learning/graph/', GetGraphAPIView.as_view(),
         name='graph'),

]
