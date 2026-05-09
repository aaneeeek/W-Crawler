from .views import search_view
from django.urls import path

urlpatterns = [
    path("search/<str:sentence>/", search_view, name="search_view")
]

