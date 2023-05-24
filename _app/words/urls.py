from django.urls import path

from words.views.achievements import AchievementsAPIView
from words.views.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, GetGameAPIView, SuccessRepetitionAPIView, \
    TextForWordAPIView, WordDetailAPIView, WordsListAPIView, \
    SavedWordsIDSAPIView, TopicsListAPIView, RetrieveTopicsAPIView, \
    TopicWordsAPIView, TopicTextsAPIView, SaveWordsFromTopicAPIView, \
    ProgressAPIView

urlpatterns = [
    path('saved/', SavedWordListAPIView.as_view(),
         name='saved-word-list'),
    path('saved/ids/', SavedWordsIDSAPIView.as_view(), name='saved-words-ids'),
    path('saved/add/', SavedWordCreateAPIView.as_view(),
         name='saved-word-create'),
    path('saved/delete/',
         DestroySavedWordAPIView.as_view(),
         name='saved-word-destroy'),
    path('game/', GetGameAPIView.as_view(), name='get-game'),
    path('game/<int:pk>/success/', SuccessRepetitionAPIView.as_view(),
         name='success-repetition'),
    path('words/', WordsListAPIView.as_view(), name='word-list'),
    path('word/<int:pk>/', WordDetailAPIView.as_view(),
         name='word-detail'),
    path('text/for-word/<int:pk>/', TextForWordAPIView.as_view(),
         name='text-for-word'),

    path('topic/', TopicsListAPIView.as_view(),
         name='topic-list-view'),
    path('topic/<int:pk>/', RetrieveTopicsAPIView.as_view(),
         name='topic-retrieve-view'),
    path('topic/<int:pk>/words/', TopicWordsAPIView.as_view(),
         name='topic-words-view'),

    path('topic/<int:pk>/texts/', TopicTextsAPIView.as_view(),
         name='topic-texts-view'),
    path('saved/from-topic/<int:pk>/',
         SaveWordsFromTopicAPIView.as_view(),
         name='add-to-saved-from-topic'),
    path('saved/progress/',
         ProgressAPIView.as_view(),
         name='saved-progress'),
    path('achievements/', AchievementsAPIView.as_view(), name='achievements')
]
