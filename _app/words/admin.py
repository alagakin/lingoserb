from django.contrib import admin
from words.models import Word


class WordAdmin(admin.ModelAdmin):
    list_display = ['title', 'part']


admin.site.register(Word, WordAdmin)
