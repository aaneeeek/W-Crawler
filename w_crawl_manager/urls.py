from django.urls import path
from .views import start_crawler, build_tree

urlpatterns = [
    path('start/', start_crawler, name="start_crawler"),
    path('build/tree/', build_tree, name="build_tree")
]


