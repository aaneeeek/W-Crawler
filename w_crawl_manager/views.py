from rest_framework.decorators import api_view
from rest_framework.response import Response
from bk_tree_manager.tasks import crawl, gen_tree


@api_view(["POST"])
def start_crawler(request):
    crawl.delay()
    return Response({"message": "starting Crawler"})


@api_view(["POST"])
def build_tree(request):
    gen_tree.delay()
    return Response({"message": "started Building Tree"})

