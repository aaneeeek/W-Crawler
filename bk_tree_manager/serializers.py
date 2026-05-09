from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import URLs, Word, WordURL


class URLSerializer(ModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = WordURL
        fields = ["url"]

    def get_url(self, instance):
        print("  .................  ", instance.url_id)
        return URLs.objects.get(id=instance.url_id).url


class WordSerializer(ModelSerializer):
    urls = SerializerMethodField()

    class Meta:
        model = Word
        fields = ["word", "urls"]

    def get_urls(self, instance):
        return URLSerializer(instance.word_url.all(), many=True).data


