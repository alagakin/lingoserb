from django.urls import path

from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, GetGameAPIView, SuccessRepetitionAPIView, \
    TextForWordAPIView, WordDetailAPIView, WordsListAPIView, \
    SavedWordsIDSAPIView

urlpatterns = [
    path('saved/', SavedWordListAPIView.as_view(),
         name='saved-word-list'),
    path('saved/ids/', SavedWordsIDSAPIView.as_view(), name='saved-words-ids'),
    path('saved/add/', SavedWordCreateAPIView.as_view(),
         name='saved-word-create'),
    path('saved/word/<int:pk>/',
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
]
