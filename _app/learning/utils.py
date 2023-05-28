from django.db import IntegrityError
from learning.models import SavedWord
from topics.models import Topic


def topic_to_saved(user, topic: Topic):
    for word in topic.words.all():
        try:
            saved_word = SavedWord(
                user=user,
                word_id=word.id
            )
            saved_word.save()
        except IntegrityError:
            pass
