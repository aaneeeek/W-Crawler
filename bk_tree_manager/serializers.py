from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import URLs, Word, WordURL


class URLSerializer(ModelSerializer):
    url_obj = SerializerMethodField()

    class Meta:
        model = WordURL
        fields = ["url_obj"]

    def get_url_obj(self, instance):
        obj = URLs.objects.get(id=instance.url_id)
        return {"url": obj.url, "priority": obj.priority}


class WordSerializer(ModelSerializer):
    url_list = SerializerMethodField()

    class Meta:
        model = Word
        fields = ["word", "url_list"]

    def get_url_list(self, instance):
        return URLSerializer(instance.word_url.all(), many=True).data


