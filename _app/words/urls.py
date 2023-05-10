from django.urls import path

from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView

urlpatterns = [
    path('saved/user/<int:user_id>/', SavedWordListAPIView.as_view()),
    path('saved/add/', SavedWordCreateAPIView.as_view()),
    path('saved/user/<int:user_id>/word/<int:pk>/',
         DestroySavedWordAPIView.as_view()),
]
