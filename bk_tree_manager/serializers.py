from rest_framework.serializers import ModelSerializer
from .models import URLs


class URLSerializer(ModelSerializer):
    class Meta:
        model = URLs
        fields = ["url", "id"]


