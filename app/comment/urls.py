from django.urls import path

from .views import (
    CommentCreateView,
    CommentListView,
    CommentDeleteView,
    CommentReplyCreateView,
)

urlpatterns = [
    path("create", CommentCreateView.as_view(), name="comment_create"),
    path("list", CommentListView.as_view(), name="comment_list"),
    path("delete", CommentDeleteView.as_view(), name="comment_delete"),
    path("reply", CommentReplyCreateView.as_view(), name="comment_reply"),
]
