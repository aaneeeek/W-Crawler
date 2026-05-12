from django.db import models


class URLs(models.Model):
    url = models.URLField(unique=True)
    priority = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)


class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)


class WordURL(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="word_url")
    url_id = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["word"]),
        ]
        unique_together = ("word", "url_id")

