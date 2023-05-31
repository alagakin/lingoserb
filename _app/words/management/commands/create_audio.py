import os
import uuid

from django.core.management.base import BaseCommand
from gtts import gTTS
import boto3
from django.conf import settings

from words.models import Word, Text


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='How many?', default=10)
        parser.add_argument('--text', type=int, help='Texts?', default=0)

    def handle(self, *args, **options):
        count = options['count']

        items = self.get_items(options)

        for item in items:
            if options['text'] != 0:
                tts = gTTS(item.content, lang='sr')
            else:
                tts = gTTS(item.title, lang='sr')

            item_s3_id = self.generate_unique_s3_id()
            tts.save(f'{item_s3_id}.mp3')

            # Upload the file to S3
            s3 = boto3.client('s3', region_name=settings.S3_REGION,
                              aws_access_key_id=settings.S3_ACCESS_KEY,
                              aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY)
            s3.upload_file(f'{item_s3_id}.mp3', settings.S3_BUCKET_NAME,
                           f'audio/{item_s3_id}.mp3')

            # Delete the local file
            item.s3_id = item_s3_id
            item.save(update_fields=['s3_id'])
            os.remove(f'{item_s3_id}.mp3')

    def get_items(self, options):
        if options['text'] != 0:
            return Text.objects.filter(s3_id=None)[0:options['count']]
        else:
            return Word.objects.filter(s3_id=None)[0:options['count']]

    def generate_unique_s3_id(self):
        return str(uuid.uuid4())[:16]
