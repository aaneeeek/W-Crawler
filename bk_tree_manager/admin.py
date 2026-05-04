from django.contrib import admin
from .models import URLs, WordURL, Word


admin.site.register(URLs)
admin.site.register(Word)
admin.site.register(WordURL)

