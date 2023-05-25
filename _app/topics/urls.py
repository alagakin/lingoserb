from django.urls import path

from topics.views import TopicsListAPIView, RetrieveTopicsAPIView, \
    TopicWordsAPIView, TopicTextsAPIView, SaveWordsFromTopicAPIView

urlpatterns = [
    path('topic/', TopicsListAPIView.as_view(),
         name='topic-list-view'),
    path('topic/<int:pk>/', RetrieveTopicsAPIView.as_view(),
         name='topic-retrieve-view'),
    path('topic/<int:pk>/words/', TopicWordsAPIView.as_view(),
         name='topic-words-view'),

    path('topic/<int:pk>/texts/', TopicTextsAPIView.as_view(),
         name='topic-texts-view'),
    path('topic/<int:pk>/save/',
         SaveWordsFromTopicAPIView.as_view(),
         name='add-to-saved-from-topic'),
]
