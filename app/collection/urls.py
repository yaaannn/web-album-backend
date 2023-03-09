from django.urls import path

from .views import CollectionCreateView, CollectionDeleteView, CollectionListView

urlpatterns = [
    path("create", CollectionCreateView.as_view()),
    path("delete", CollectionDeleteView.as_view()),
    path("list", CollectionListView.as_view()),
]
