import os

import openai
from django.core.management.base import BaseCommand, CommandError
import json

from learn_serbian.utils import transliterate
from words.models import Word, Category, Translation
import logging

logger = logging.getLogger('openai')


class Command(BaseCommand):
    help = "Imports base 3000 words with English and Russian translations"
    prompt = """Provide 50 Serbian words for category '%s' with translation 
        to Russian. Use JSON only, like this {
    "Topic": [
        {
            "serbian": "serbian word",
            "russian": "русское слово"
        }, ]"""

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Topic')

    def handle(self, *args, **options):
        prompt = self.prompt % (options['category'])
        openai.api_key = os.getenv('OPENAI_KEY')
        try:
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[
                    {"role": "user",
                     "content": prompt}]
            )
            result = chat_completion['choices'][0]['message']['content']
            result = json.loads(result)
            category_name = options['category']
            pairs = result[category_name]

            try:
                category = Category.objects.get(title=category_name.lower())
            except Category.DoesNotExist:
                category = Category(
                    title=category_name.lower()
                )
                category.save()

            for pair in pairs:
                sr_word = transliterate(pair['serbian'].lower())
                ru_word = pair['russian'].lower()
                try:
                    word = Word.objects.get(title=sr_word)
                except Word.DoesNotExist:
                    word = Word(
                        title=sr_word
                    )
                    word.save()
                try:
                    Translation.objects.get(lang='ru', word=word,
                                                          title=ru_word)
                except Translation.DoesNotExist:
                    translation = Translation(lang='ru', word=word,
                                              title=ru_word)
                    translation.save()
                word.categories.add(category)

            logger.info(pairs)
        except KeyError as key_error:
            logger.error(key_error)
        except ValueError as value_error:
            logger.error(value_error)
