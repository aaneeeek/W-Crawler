from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import ClientSerializer
from searcher.tasks import search


@api_view(['POST'])
def create_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        print("saving")
        serializer.save()
        client = serializer.data
        search.delay(client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)