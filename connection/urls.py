from django.urls import path
from .views import create_client

urlpatterns = [
    path("create/", create_client, name="search_view")
]

