from django.contrib.auth import get_user_model
from django.db import models
from words.models import Word


class SavedWordsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class SavedWordsManagerAll(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class SavedWord(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='saved',
                             on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    last_repetition = models.DateTimeField(null=True, blank=True)
    repetition_count = models.PositiveSmallIntegerField(default=0)
    deleted = models.BooleanField(default=False)
    skipped = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save(update_fields=['deleted'])

    def __str__(self):
        return str(self.word) + ' - ' + str(self.user)

    class Meta:
        unique_together = ['user', 'word']

    objects = SavedWordsManager()
    all_objects = SavedWordsManagerAll()

    def save(self, *args, **kwargs):
        max_value = 5
        if self.repetition_count > max_value:
            self.repetition_count = max_value
        super().save(*args, **kwargs)
