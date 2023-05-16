from django.urls import path
from .views import (
    UploadPhotoToLocal,
    GetSliderCaptcha,
    ValidateSliderCaptcha,
    UploadPhotoToIPFS,
)

urlpatterns = [
    path("upload", UploadPhotoToLocal.as_view(), name="upload_local_photo"),
    path("captcha/get", GetSliderCaptcha.as_view(), name="get_slider_captcha"),
    path(
        "captcha/validate",
        ValidateSliderCaptcha.as_view(),
        name="validate_slider_captcha",
    ),
    path("upload/ipfs", UploadPhotoToIPFS.as_view(), name="upload_ipfs_photo"),
]
