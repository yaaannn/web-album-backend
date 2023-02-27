from django.urls import path
from .views import generate_captcha_code, UploadImageToLocal

urlpatterns = [
    path("generate_code", generate_captcha_code, name="generate_code"),
    path("upload", UploadImageToLocal.as_view(), name="upload_local_image"),
]
