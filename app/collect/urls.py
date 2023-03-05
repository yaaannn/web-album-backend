from django.urls import path

from .views import CollectCreateView, CollectDeleteView, CollectListView

urlpatterns = [
    path("create", CollectCreateView.as_view()),
    path("delete", CollectDeleteView.as_view()),
    path("list", CollectListView.as_view()),
]
