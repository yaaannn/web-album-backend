import time
from django.conf import settings
from rest_framework import serializers
from util.time_util import TimeUtil


class BaseModelSerializer(serializers.Serializer):
    """
    基础序列化器
    """

    create_time_format = serializers.SerializerMethodField(label="创建时间")
    update_time_format = serializers.SerializerMethodField(label="更新时间")

    def get_create_time_format(self, obj) -> str:
        """
        获取创建时间
        """
        return TimeUtil.timestamp_str(
            obj.create_time, settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        )

    def get_update_time_format(self, obj) -> str:
        """
        获取更新时间
        """
        return TimeUtil.timestamp_str(
            obj.update_time, settings.REST_FRAMEWORK["DATETIME_FORMAT"]
        )
