from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from words.models import Word, Category, SavedWord
from words.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView, SuccessRepetitionAPIView, GetGameAPIView
from rest_framework.test import APITestCase


class TestEndpointsResoled(TestCase):
    def test_get_game_resolved(self):
        url = reverse('get-game')
        self.assertEqual(resolve(url).func.view_class, GetGameAPIView)

    def test_success_repetition_resolved(self):
        url = reverse('success-repetition', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, SuccessRepetitionAPIView)


class TestGameActions(APITestCase):
    def setUp(self) -> None:
        pass
