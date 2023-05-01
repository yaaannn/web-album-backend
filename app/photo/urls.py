from django.urls import path
from .views import *


urlpatterns = [
    path("list", ListPhotoView.as_view(), name="photo_list"),
    path("delete", DeletePhotoView.as_view(), name="photo_delete"),
    path("public", ListPublicPhotoView.as_view(), name="public_photo_list"),
    path("add_to_album", AddPhotoToAlbumView.as_view(), name="add_photo_to_album"),
    path(
        "delete_from_album",
        DeletePhotoFromAlbumView.as_view(),
        name="delete_photo_from_album",
    ),
    path("album_photo_list", ListAlbumPhotoView.as_view(), name="album_photo_list"),
    path("upload", UploadPhotoInfoView.as_view(), name="upload_photo"),
    path("get_info", GetPhotoInfoView.as_view(), name="get_photo_info"),
    path("get_photo_by_id", GetPublicPhotoByUidView.as_view(), name="get_photo_by_id"),
    path("update", UpdatePhotoInfoView.as_view(), name="update_photo_info"),
]
