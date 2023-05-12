import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from learn_serbian.utils import transliterate
from words.models import Word, Translation


class Command(BaseCommand):
    help = "Imports base 3000 words with English and Russian translations"

    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/base3000.csv', newline='') as csvfile:
            document = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in document:
                save_word(row)


def save_word(row: list[str]) -> None:
    serbian = transliterate(row[0].strip())
    english = row[1].strip()
    russian = row[2].strip()
    try:
        word = Word.objects.get(title=serbian)
    except Word.DoesNotExist:
        word = Word(
            title=serbian
        )
        word.save()
    try:
        word.translations.get(title=english, word=word, lang='en')
    except Translation.DoesNotExist:
        trans_en = Translation(
            title=english,
            lang='en',
            word=word
        )
        trans_en.save()

    try:
        word.translations.get(title=russian, word=word, lang='ru')
    except Translation.DoesNotExist:
        trans_ru = Translation(
            title=russian,
            lang='ru',
            word=word
        )
        trans_ru.save()
