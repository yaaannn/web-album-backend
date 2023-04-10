from django.urls import path
from .views import (
    UploadPhotoToLocal,
    ListPhotoView,
    DeletePhotoView,
    ListPublicPhotoView,
    UpdatePhotoStatusView,
    UpdatePhotoDescView,
)

urlpatterns = [
    path("upload", UploadPhotoToLocal.as_view(), name="upload_local_photo"),
    path("list", ListPhotoView.as_view(), name="photo_list"),
    path("delete", DeletePhotoView.as_view(), name="photo_delete"),
    path("public", ListPublicPhotoView.as_view(), name="public_photo_list"),
    path("update_status", UpdatePhotoStatusView.as_view(), name="update_photo_status"),
    path("update_desc", UpdatePhotoDescView.as_view(), name="update_photo_desc"),
]
