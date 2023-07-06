from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Dump specific tables to a file'

    def handle(self, *args, **options):
        call_command(
            'dumpdata',
            'words.TextTranslation',
            'words.Text',
            'words.Tag',
            'words.Word',
            'words.Translation',
            'topics.Topic',
            'topics.TopicTranslation',
            '--output=db.json'
        )


