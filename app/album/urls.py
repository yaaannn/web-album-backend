from django.urls import path

from .views import (
    AlbumCreateView,
    AlbumDeleteView,
    AlbumDetailView,
    AlbumListView,
    AlbumUpdateView,
)

urlpatterns = [
    path("create", AlbumCreateView.as_view()),
    path("list", AlbumListView.as_view()),
    path("delete", AlbumDeleteView.as_view()),
    path("detail", AlbumDetailView.as_view()),
    path("update", AlbumUpdateView.as_view()),
]
