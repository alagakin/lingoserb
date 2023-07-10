import os

import openai
from django.core.management.base import BaseCommand
import json

from learn_serbian.utils import transliterate
from words.models import Word, Text, TextTranslation
import logging

logger = logging.getLogger('openai')


class Command(BaseCommand):
    help = "Imports base 3000 words with English and Russian translations"
    prompt = """Your response for next prompt should only contain JSON string.
    For the following Serbian words make Serbian one or two sentences
    with it's usage: %s.
    Translate each text to Russian. Use this as example: {
        "sentences": [
        {
        "word": "Serbian word",
        "text": "text in Serbian",
        "translation_ru": "translation to Russian",
        "translation_en": "translation to English"
        }, ]}"""

    def add_arguments(self, parser):
        parser.add_argument('--iter', type=int, help='How many?', default=10)
        parser.add_argument('--words_per_iter', type=int, help='How many?', default=5)


    def handle(self, *args, **options):
        openai.api_key = os.getenv('OPENAI_KEY')
        for i in range(0, options['iter']):
            words = Word.objects.order_by('-texts')[0:options['words_per_iter']]

            titles = ['"' + word.title + '"' for word in words]
            titles = ", ".join(titles)
            prompt = self.prompt % titles

            try:
                chat_completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=[
                        {"role": "user",
                         "content": prompt}]
                )
                sentences = chat_completion['choices'][0]['message']['content']
                sentences = json.loads(sentences)
                sentences = sentences['sentences']

                for sentence in sentences:
                    try:
                        word = Word.objects.get(title=sentence['word'])
                    except Word.DoesNotExist:
                        return

                    try:
                        text = Text.objects.get(content=sentence['text'])
                    except Text.DoesNotExist:
                        text = Text(
                            content=sentence['text']
                        )
                        text.save()

                    try:
                        TextTranslation.objects.get(
                            content=sentence['translation_ru'],
                            lang='ru',
                            text=text
                        )
                    except TextTranslation.DoesNotExist:
                        translation = TextTranslation(
                            content=sentence['translation_ru'],
                            lang='ru',
                            text=text
                        )
                        translation.save()

                    try:
                        TextTranslation.objects.get(
                            content=sentence['translation_en'],
                            lang='en',
                            text=text
                        )
                    except TextTranslation.DoesNotExist:
                        translation = TextTranslation(
                            content=sentence['translation_en'],
                            lang='en',
                            text=text
                        )
                        translation.save()

                    if text not in word.texts.all():
                        word.texts.add(text)

                logger.info(sentences)
            except KeyError as key_error:
                logger.error(key_error)
            except ValueError as value_error:
                logger.error(value_error)
