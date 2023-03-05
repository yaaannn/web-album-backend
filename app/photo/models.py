from django.db import models
from extension.base.model import BaseModel
from app.user.models import User
from app.album.models import Album
from app.tag.models import Tag

STATUS_CHOICES = (("0", "公开"), ("1", "私密"))


class Photo(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, null=True, verbose_name="相册"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, verbose_name="标签")
    name = models.CharField(max_length=32, unique=True, verbose_name="照片名")
    url = models.CharField(max_length=255, verbose_name="照片地址")
    desc = models.CharField(max_length=255, blank=True, default="", verbose_name="描述")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="0", verbose_name="状态"
    )

    class Meta:
        db_table = "a_photo"
        verbose_name = "照片表"
        verbose_name_plural = verbose_name
