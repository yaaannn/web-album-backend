from datetime import datetime
from django.db.models import BigIntegerField
from util.time_util import TimeUtil


class TimestampField(BigIntegerField):
    """
    自定义时间戳字段
    """

    description = "自定义时间戳字段"

    def __init__(
        self, verbose_name=None, name=None, auto_now=False, auto_now_add=False, **kwargs
    ):
        """
        初始化
        :param verbose_name: 字段名称
        :param name: 字段别名
        :param auto_now: 每次保存对象时，都会将字段的值设置为当前时间
        :param auto_now_add: 在对象第一次被创建时，将字段的值设置为当前时间
        :param kwargs: 其他参数
        """
        self.auto_now, self.auto_now_add = auto_now, auto_now_add
        if auto_now or auto_now_add:
            # 如果设置了 auto_now 或 auto_now_add 为 True，那么 editable 和 blank 都为 False
            kwargs["editable"] = False
            kwargs["blank"] = True
        super().__init__(verbose_name, name, **kwargs)

    def pre_save(self, model_instance, add):
        """
        保存前处理
        :param model_instance: 模型实例
        :param add: 是否新增
        :return:
        """
        # 如果设置了 auto_now 或 auto_now_add 为 True，那么每次保存对象时，都会将字段的值设置为当前时间
        if self.auto_now or (self.auto_now_add and add):
            # 获取当前时间戳
            value = TimeUtil.datetime_timestamp(datetime.now())
            # 设置字段值
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
