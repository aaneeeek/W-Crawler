from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import search


@api_view(["POST"])
def search_view(request, sentence: str):
    print(sentence)
    search.delay(sentence)
    return Response({"message": "Started search"})


