from django.urls import path
from app.photo.views import *


urlpatterns = [
    path("list", ListPhotoView.as_view(), name="photo_list"),
    path("delete", DeletePhotoView.as_view(), name="photo_delete"),
    path("public", ListPublicPhotoView.as_view(), name="public_photo_list"),
    path("update", UpdatePhotoInfoView.as_view(), name="update_photo_info"),
    path(
        "album/delete",
        DeletePhotoFromAlbumView.as_view(),
        name="delete_photo_from_album",
    ),
    path("album/list", ListAlbumPhotoView.as_view(), name="album_photo_list"),
    path("upload", UploadPhotoInfoView.as_view(), name="upload_photo"),
    path("info", GetPhotoInfoView.as_view(), name="get_photo_info"),
    path("public/id", GetPublicPhotoByUidView.as_view(), name="get_photo_by_id"),
    path(
        "public/partition", GetPhotoByPidView.as_view(), name="get_photo_by_partition"
    ),
]
