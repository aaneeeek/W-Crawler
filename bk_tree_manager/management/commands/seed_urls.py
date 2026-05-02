from django.core.management.base import BaseCommand
from bk_tree_manager.models import URLs


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        urls = [
            "https://google.com",
            "https://youtube.com",
            "https://facebook.com",
            "https://twitter.com",
            "https://instagram.com",
            "https://linkedin.com",
            "https://wikipedia.org",
            "https://amazon.com",
            "https://netflix.com",
            "https://reddit.com",
            "https://nytimes.com",
            "https://bbc.com",
            "https://cnn.com",
            "https://yahoo.com",
            "https://bing.com",
            "https://microsoft.com",
            "https://apple.com",
            "https://openai.com",
            "https://github.com",
            "https://stackoverflow.com",
        ]
        try:
            URLs.objects.get(id=1)
        except:
            for url in urls:
                URLs.objects.get_or_create(url=url)

            self.stdout.write("Seeded URLs successfully")

