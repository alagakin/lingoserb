from django.urls import path
from words.views import TextForWordAPIView, WordDetailAPIView, WordsSearchAPIView

urlpatterns = [
    path('word/<int:pk>/', WordDetailAPIView.as_view(),
         name='word-detail'),
    path('text/for-word/<int:pk>/', TextForWordAPIView.as_view(),
         name='text-for-word'),
    path('words/search/', WordsSearchAPIView.as_view(), name='word-search')
]
