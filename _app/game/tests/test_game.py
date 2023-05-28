from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from game.views import GetGameAPIView, SuccessRepetitionAPIView
from learning.models import SavedWord
from words.models import Word, Translation
from rest_framework.test import APITestCase
import json


class TestEndpointsResoled(TestCase):
    def test_get_game_resolved(self):
        url = reverse('get-game')
        self.assertEqual(resolve(url).func.view_class, GetGameAPIView)

    def test_success_repetition_resolved(self):
        url = reverse('success-repetition', kwargs={'word_id': 1})
        self.assertEqual(resolve(url).func.view_class, SuccessRepetitionAPIView)


class TestGameActions(APITestCase):
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
        self.saved_word_user_1 = SavedWord.objects.create(
            word=self.word_1,
            user=self.user_1
        )
        self.saved_word_user_2 = SavedWord.objects.create(
            word=self.word_2,
            user=self.user_2
        )
        self.translation_1 = Translation.objects.create(
            lang='ru',
            title='First word translation',
            word=self.word_1
        )
        self.translation_2 = Translation.objects.create(
            lang='ru',
            title='Second word translation',
            word=self.word_2
        )

    def test_user_can_get_game(self):
        response = self.client.get(reverse('get-game'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_game_structure(self):
        response = self.client.get(reverse('get-game'))
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['word'], 'Test word')
        self.assertEqual(len(response_json[0]['options']), 2)
        self.assertTrue(
            any(option['correct'] for option in response_json[0]['options']))

    def test_user_can_interact_with_game(self):
        self.assertEqual(self.saved_word_user_1.repetition_count, 0)
        self.assertIsNone(self.saved_word_user_1.last_repetition)
        response = self.client.post(reverse('success-repetition', kwargs={
            'word_id': self.word_1.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user_1.saved.first().repetition_count, 1)
        self.assertIsNotNone(self.user_1.saved.first().last_repetition)
