from rest_framework.decorators import api_view
from rest_framework.response import Response
from bk_tree_manager.tasks import crawl


@api_view(["POST"])
def start_crawler(request):
    crawl.delay()
    return Response({"message": "starting Crawler"})

