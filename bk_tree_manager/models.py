from django.db import models


class URLs(models.Model):
    url = models.URLField(unique=True)


