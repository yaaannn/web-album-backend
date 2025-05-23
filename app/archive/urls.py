from django.urls import path

from app.archive.views import (
    CancelLikePhotoView,
    IsLikePhotoView,
    LikeCountView,
    LikeListView,
    LikePhotoView,
)

urlpatterns = [
    path("like", LikePhotoView.as_view(), name="like_photo"),
    path("is_like", IsLikePhotoView.as_view(), name="is_like_photo"),
    path("list", LikeListView.as_view(), name="like_list"),
    path("count", LikeCountView.as_view(), name="like_count"),
    path("cancel", CancelLikePhotoView.as_view(), name="cancel_like_photo"),
]
