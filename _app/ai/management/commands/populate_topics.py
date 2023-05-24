import os

import openai
from django.core.management.base import BaseCommand, CommandError
import json

from learn_serbian.utils import transliterate
from topics.models import Topic
from words.models import Word, Translation
import logging

logger = logging.getLogger('openai')


class Command(BaseCommand):
    help = "Imports base 3000 words with English and Russian translations"
    prompt = """Provide 50 Serbian words for topic '%s' with translation 
        to Russian. Use JSON only, like this {
    "Topic": [
        {
            "serbian": "serbian word",
            "russian": "русское слово"
        }, ]"""

    def choose_topic(self):
        topic = Topic.objects.filter(parent_id__gt=0).order_by('-words').first()
        title_en = topic.translations.filter(lang='en').first().title
        return title_en

    def handle(self, *args, **options):
        openai.api_key = os.getenv('OPENAI_KEY')
        prompt = self.prompt % (self.choose_topic())

        try:
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[
                    {"role": "user",
                     "content": prompt}]
            )
            result = chat_completion['choices'][0]['message']['content']
            result = json.loads(result)
            topic_name = options['topic']
            pairs = result[topic_name]

            try:
                topic = Topic.objects.get(title=topic_name.lower())
            except Topic.DoesNotExist:
                topic = Topic(
                    title=topic_name.lower()
                )
                topic.save()

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
                word.topics.add(topic)

            logger.info(pairs)
        except KeyError as key_error:
            logger.error(key_error)
        except ValueError as value_error:
            logger.error(value_error)
