from django.db import models
from extension.base.model import BaseModel
from app.user.models import User

# Create your models here.
class Album(BaseModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="作者"
    )
    name = models.CharField(max_length=32, unique=True, verbose_name="相册名")
    cover = models.CharField(max_length=255, blank=True, default="", verbose_name="封面")
    desc = models.CharField(max_length=255, blank=True, default="", verbose_name="描述")

    class Meta:
        db_table = "a_album"
        verbose_name = "相册表"
        verbose_name_plural = verbose_name
