from django.db import models
from extension.base.model import BaseModel
from app.user.models import User
from app.album.models import Album
from app.photo.models import Photo


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="照片")
    content = models.CharField(
        max_length=255, blank=True, default="", verbose_name="评论内容"
    )

    class Meta:
        db_table = "a_comment"
        verbose_name = "评论表"
        verbose_name_plural = verbose_name
