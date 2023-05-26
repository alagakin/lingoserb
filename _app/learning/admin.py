from django.contrib import admin
from learning.models import SavedWord


class SavedWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'last_repetition', 'repetition_count']


admin.site.register(SavedWord, SavedWordAdmin)
