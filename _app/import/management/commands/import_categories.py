import csv
import os

import openai
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from learn_serbian.utils import transliterate
from words.models import Word, Translation


class Command(BaseCommand):
    help = "Imports base 3000 words with English and Russian translations"

    def handle(self, *args, **options):
        openai.api_key = os.getenv('OPENAI_KEY')

        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[
                {"role": "user",
                 "content": f"Напиши 20 самых используемых сербских слов"}]
        )
        print(chat_completion.choices[0])


