from django.contrib import admin
from words.models import Word, Translation, SavedWord, Text, TextTranslation, \
    Category


class TranslationInlineAdmin(admin.TabularInline):
    model = Translation
    extra = 3


class TextTranslationInlineAdmin(admin.TabularInline):
    model = TextTranslation
    extra = 2


class WordAdmin(admin.ModelAdmin):
    list_display = ['title', 'part', 'texts_count']
    inlines = [TranslationInlineAdmin]


class TranslationAdmin(admin.ModelAdmin):
    list_display = ['title', 'lang', 'word']


class SavedWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'last_repetition', 'repetition_count']


class TextAdmin(admin.ModelAdmin):
    list_display = ['content', 'words_count', 'translations_count']
    readonly_fields = ['words_count']
    inlines = [TextTranslationInlineAdmin]


class TextTranslationAdmin(admin.ModelAdmin):
    list_display = ['id', 'preview', 'text', 'lang', 'words_count']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'words_count', 'title']


admin.site.register(Word, WordAdmin)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(SavedWord, SavedWordAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(TextTranslation, TextTranslationAdmin)
admin.site.register(Category, CategoryAdmin)

