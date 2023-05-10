from django.urls import path

from words.views import SavedWordListAPIView, SavedWordCreateAPIView

urlpatterns = [
    path('saved/<int:user_id>/', SavedWordListAPIView.as_view()),
    path('saved/add/', SavedWordCreateAPIView.as_view())

]
