from django.urls import path

from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, GetGameAPIView, SuccessRepetitionAPIView, \
    TextForWordAPIView, WordDetailAPIView, WordsListAPIView

urlpatterns = [
    path('saved/', SavedWordListAPIView.as_view(),
         name='saved-word-list'),
    path('saved/add/', SavedWordCreateAPIView.as_view(),
         name='saved-word-create'),
    path('saved/word/<int:pk>/',
         DestroySavedWordAPIView.as_view(),
         name='saved-word-destroy'),
    path('game/', GetGameAPIView.as_view()),
    path('game/<int:pk>/success/', SuccessRepetitionAPIView.as_view()),
    path('text/for-word/<int:pk>/', TextForWordAPIView.as_view()),
    path('word/<int:pk>/', WordDetailAPIView.as_view()),
    path('words/', WordsListAPIView.as_view()),

]
