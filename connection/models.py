from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models


class Client(models.Model):
    db_name = models.CharField(max_length=255)
    db_host = models.CharField(max_length=255)
    db_user = models.CharField(max_length=255)
    db_password = models.CharField(max_length=255)
    port = models.IntegerField()
    tables = JSONField(default=list)  # [table1: {attr1: "INT PRIMARY KEY", ...}, table2: {...} ]
    prompt = models.TextField()
    queries = JSONField(default=list)  # [query1: {table1.attrib_i}]
    db_type = models.CharField(max_length=255, choices=[
        ('mysql', 'MySQL DB'),
        ('postgres', 'PostgresQL DB')
    ])
    constraints = ArrayField(models.CharField(max_length=255))


