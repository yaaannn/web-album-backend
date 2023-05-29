from django.urls import path

from app.comment.views import (
    CommentCreateView,
    CommentDeleteView,
    CommentListView,
    CommentReplyCreateView,
    CommentReplyDeleteView,
)

urlpatterns = [
    path("create", CommentCreateView.as_view(), name="comment_create"),
    path("list", CommentListView.as_view(), name="comment_list"),
    path("delete", CommentDeleteView.as_view(), name="comment_delete"),
    path("reply", CommentReplyCreateView.as_view(), name="comment_reply"),
    path("reply/delete", CommentReplyDeleteView.as_view(), name="comment_reply_delete"),
]
