from django.db import models

from extension.base.model import BaseModel


class Partition(BaseModel):
    name = models.CharField(max_length=32, unique=True, verbose_name="分区名")

    class Meta:
        db_table = "a_partition"
        verbose_name = "分区表"
        verbose_name_plural = verbose_name
