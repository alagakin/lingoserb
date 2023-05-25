import os
import uuid

from django.core.management.base import BaseCommand
from gtts import gTTS
import boto3
from django.conf import settings

from words.models import Word


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='How many?')

    def handle(self, *args, **options):
        count = options['count']

        words = Word.objects.filter(s3_id=None)[0:count]
        for word in words:
            tts = gTTS(word.title, lang='sr')
            word_s3_id = self.generate_unique_s3_id()
            tts.save(f'{word_s3_id}.mp3')

            # Upload the file to S3
            s3 = boto3.client('s3', region_name=settings.S3_REGION,
                              aws_access_key_id=settings.S3_ACCESS_KEY,
                              aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY)
            s3.upload_file(f'{word_s3_id}.mp3', settings.S3_BUCKET_NAME,
                           f'audio/{word_s3_id}.mp3')

            # Delete the local file
            word.s3_id = word_s3_id
            word.save(update_fields=['s3_id'])
            os.remove(f'{word_s3_id}.mp3')

    def generate_unique_s3_id(self):
        return str(uuid.uuid4())[:16]
