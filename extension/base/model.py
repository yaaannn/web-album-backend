from django.core.validators import MinValueValidator
from django.db import models
from extension.custom_field_ext import TimestampField


class BaseModel(models.Model):
    """
    基础模型
    """

    create_time = TimestampField(
        verbose_name="创建时间戳",
        auto_now_add=True,
        validators=[MinValueValidator(limit_value=0)],
        help_text="创建时间戳",
    )
    update_time = TimestampField(
        verbose_name="更新时间戳",
        auto_now=True,
        validators=[MinValueValidator(limit_value=0)],
        help_text="更新时间戳",
    )

    class Meta:
        abstract = True
