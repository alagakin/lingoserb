import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from meilisearch import Client
from words.models import Word

logger = logging.getLogger('index_logger')


class Command(BaseCommand):

    def handle(self, *args, **options):
        client = Client(settings.MEILISEARCH_URL, settings.MEILI_MASTER_KEY)

        words = Word.objects.all()
        indexed_words = []
        for word in words:
            try:
                indexed_words.append({
                    'id': str(word.id),
                    'title': word.title,
                    'title_ru': word.translations.filter(lang='ru').first().title,
                    'title_end': word.translations.filter(lang='en').first().title,
                })
            except AttributeError as e:
                logger.error(f'Error while indexing word {word.id}: {e}')

        index = client.index('words')
        index.add_documents(indexed_words)
