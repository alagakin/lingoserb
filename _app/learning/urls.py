from django.urls import path

from learning.views import GetGameAPIView, SuccessRepetitionAPIView, \
    SavedWordListAPIView, SavedWordsIDSAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, ProgressAPIView

urlpatterns = [
    path('game/', GetGameAPIView.as_view(), name='get-game'),
    path('game/<int:pk>/success/', SuccessRepetitionAPIView.as_view(),
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
]
