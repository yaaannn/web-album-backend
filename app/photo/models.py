from django.db import models
from extension.base.model import BaseModel
from app.user.models import User
from app.album.models import Album
from app.partition.models import Partition

STATUS_CHOICES = ((0, "正常"), (1, "待审核"), (2, "审核未通过"))


class Photo(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    album = models.ForeignKey(
        Album, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="相册"
    )
    partition = models.ForeignKey(
        Partition, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="分区"
    )
    name = models.CharField(max_length=32, unique=True, verbose_name="照片名")
    url = models.CharField(max_length=255, verbose_name="照片地址")
    desc = models.CharField(max_length=255, blank=True, default="", verbose_name="描述")
    is_public = models.BooleanField(default=True, verbose_name="是否公开")
    click = models.IntegerField(default=0, verbose_name="点击量")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态")

    class Meta:
        db_table = "a_photo"
        verbose_name = "照片表"
        verbose_name_plural = verbose_name
        # 按照创建时间倒序
        ordering = ["-create_time"]
