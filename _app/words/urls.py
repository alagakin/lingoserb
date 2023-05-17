from django.urls import path

from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, GetGameAPIView, SuccessRepetitionAPIView, \
    TextForWordAPIView, WordDetailAPIView, WordsListAPIView, \
    SavedWordsIDSAPIView, CategoriesListAPIView, RetrieveCategoriesAPIView, \
    CategoryWordsAPIView, CategoryTextsAPIView

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

    path('category/', CategoriesListAPIView.as_view(), name='category-list-view'),
    path('category/<int:pk>/', RetrieveCategoriesAPIView.as_view(),
         name='category-retrieve-view'),
    path('category/<int:pk>/words/', CategoryWordsAPIView.as_view(),
         name='category-words-view'),

    path('category/<int:pk>/texts/', CategoryTextsAPIView.as_view(),
         name='category-texts-view')

]
