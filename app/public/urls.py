from django.urls import path
from .views import (
    generate_captcha_code,
    UploadImageToLocal,
    UploadPhotoToLocal,
    GetSliderCaptcha,
    ValidateSliderCaptcha,
)

urlpatterns = [
    path("generate_code", generate_captcha_code, name="generate_code"),
    # path("upload", UploadImageToLocal.as_view(), name="upload_local_image"),
    path("upload", UploadPhotoToLocal.as_view(), name="upload_local_photo"),
    path("captcha/get", GetSliderCaptcha.as_view(), name="get_slider_captcha"),
    path(
        "captcha/validate",
        ValidateSliderCaptcha.as_view(),
        name="validate_slider_captcha",
    ),
]
