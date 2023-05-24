import os
from django.core.management.base import BaseCommand
import json
import topics
from topics.models import Topic, TopicTranslation


class Command(BaseCommand):
    def handle(self, *args, **options):
        pth = os.path.dirname(topics.__file__)
        f = open(pth + '/topics.json')
        result = json.load(f)

        for raw_topic in result:
            title = raw_topic['title']
            title_ru = raw_topic['title_ru']
            title_en = raw_topic['title_en']

            topic = self.create_topic(title, title_ru, title_en)
            for raw_subtopic in raw_topic['subtopics']:
                title = raw_subtopic['title']
                title_ru = raw_subtopic['title_ru']
                title_en = raw_subtopic['title_en']
                self.create_topic(title, title_ru, title_en, topic)

    def create_topic(self, title, title_ru, title_en, parent=None):
        try:
            topic = Topic.objects.get(title=title, parent=parent)
        except Topic.DoesNotExist:
            topic = Topic(
                title=title,
                parent=parent
            )
            topic.save()

        try:
            topic.translations.get(lang='ru')
        except TopicTranslation.DoesNotExist:
            translation_ru = TopicTranslation(
                title=title_ru,
                lang='ru',
                topic=topic
            )
            translation_ru.save()

        try:
            topic.translations.get(lang='en')
        except TopicTranslation.DoesNotExist:
            translation_ru = TopicTranslation(
                title=title_en,
                lang='en',
                topic=topic
            )
            translation_ru.save()

        return topic