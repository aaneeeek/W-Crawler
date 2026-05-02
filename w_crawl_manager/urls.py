from django.urls import path
from .views import start_crawler

urlpatterns = [
    path('start/', start_crawler, name="start_crawler")
]


