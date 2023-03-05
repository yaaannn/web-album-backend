from django.urls import path

from .views import CommentCreateView, CommentListView, CommentDeleteView

urlpatterns = [
    path("create", CommentCreateView.as_view(), name="comment_create"),
    path("list", CommentListView.as_view(), name="comment_list"),
    path("delete", CommentDeleteView.as_view(), name="comment_delete"),
]
