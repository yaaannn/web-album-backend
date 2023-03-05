from django.db import models
from extension.base.model import BaseModel
from app.user.models import User
from app.photo.models import Photo

# Create your models here.


class Collect(BaseModel):
    """
    收藏
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="图片")

    class Meta:
        db_table = "a_collect"
        verbose_name = "收藏表"
        verbose_name_plural = verbose_name
