# from typing import *
from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction

from extension.custom_field_ext import TimestampField
from util.time_util import TimeUtil


class BigDataFilterManager(models.Manager):
    """
    大数据过滤器管理器
    """

    def all(self, flitter_time=None):
        """
        获取所有数据
        :param flitter_time: 过滤时间
        :return:
        """
        if flitter_time:
            if "," in flitter_time:
                start_time = TimeUtil.datetime_timestamp(
                    datetime.strptime(
                        flitter_time.split(",")[0] + "-01 00:00:00", "%Y-%m-%d %H:%M:%S"
                    )
                )
                end_time = TimeUtil.datetime_timestamp(
                    datetime.strptime(
                        flitter_time.split(",")[1] + "-01 00:00:00", "%Y-%m-%d %H:%M:%S"
                    )
                )
                return (
                    super()
                    .all()
                    .filter(create_time__gte=start_time, create_time__lte=end_time)
                )
            return super().all()
        return super().all()


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

    # @transaction.atomic
    # def delete(self, *args, **kwargs) -> None:
    #     """
    #     逻辑删除
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     self.update_time = TimeUtil.datetime_timestamp(datetime.now())
    #     super().delete(*args, **kwargs)
