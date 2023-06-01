from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from learning.models import SavedWord
from learning.views import SavedWordListAPIView, SavedWordCreateAPIView, \
    DestroySavedWordAPIView
from words.models import Word
from rest_framework.test import APITestCase


class TestEndpointsResoled(TestCase):
    def test_get_saved_words_list_resolved(self):
        url = reverse('saved-word-list')
        self.assertEqual(resolve(url).func.view_class, SavedWordListAPIView)


class TestSavedWordsActions(APITestCase):
    def setUp(self) -> None:
        self.user_1 = get_user_model().objects.create(
            username='user 1',
            password='123'
        )
        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token_user_1.key}')
        self.user_2 = get_user_model().objects.create(
            username='user 2',
            password='123'
        )
        self.token_user_2 = Token.objects.create(user=self.user_2)

        self.word_1 = Word.objects.create(
            title='Test word',
        )

        self.word_2 = Word.objects.create(
            title='Second word'
        )

    def test_user_can_get_saved_words(self):
        SavedWord.objects.create(
            word=self.word_1,
            user=self.user_1
        )
        response = self.client.get(
            reverse('saved-word-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test word')

    def test_user_cant_access_another_users_saved_words(self):
        SavedWord.objects.create(
            word=self.word_2,
            user=self.user_2
        )
        response = self.client.get(
            reverse('saved-word-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, 'Second word')
