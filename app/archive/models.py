from django.db import models

from app.photo.models import Photo
from app.user.models import User
from extension.base.model import BaseModel


# 点赞表
class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="点赞者")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="照片")

    class Meta:
        db_table = "a_like"
        verbose_name = "点赞表"
        verbose_name_plural = verbose_name
