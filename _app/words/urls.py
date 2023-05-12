from django.urls import path

from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, GetGameAPIView, SuccessRepetitionAPIView, \
    TextForWordAPIView

urlpatterns = [
    path('saved/<int:user_id>/', SavedWordListAPIView.as_view()),
    path('saved/add/', SavedWordCreateAPIView.as_view()),
    path('saved/word/<int:pk>/',
         DestroySavedWordAPIView.as_view()),
    path('game/', GetGameAPIView.as_view()),
    path('game/<int:pk>/success/', SuccessRepetitionAPIView.as_view()),
    path('text/for-word/<int:pk>/', TextForWordAPIView.as_view())
]
