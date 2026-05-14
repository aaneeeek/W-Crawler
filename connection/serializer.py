from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "db_name",
            "db_host",
            "db_user",
            "db_password",
            "port",
            "tables",
            "prompt",
            "queries",
            "db_type",
            "constraints",
        ]
        extra_kwargs = {
            "db_password": {"write_only": True}
        }