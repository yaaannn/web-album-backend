from django.urls import path

from app.public.views import (
    AddSensitiveWord,
    GetSliderCaptcha,
    ListSensitiveWords,
    UploadPhotoToIPFS,
    UploadPhotoToLocal,
    ValidateSliderCaptcha,
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
    path("sensitive/list", ListSensitiveWords.as_view(), name="list_sensitive_words"),
    path("sensitive/add", AddSensitiveWord.as_view(), name="add_sensitive_word"),
]
