from django.db import models

# from extension.base_model_ext import BaseModel
from extension.base.model import BaseModel
from util.password_util import PasswordUtil
from django.conf import settings


class User(BaseModel):

    GENDER_CHOICES = (("0", "男"), ("1", "女"), ("2", "秘密"))

    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=255, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")
    mobile = models.CharField(max_length=11, blank=True, default="", verbose_name="手机号")
    nickname = models.CharField(
        max_length=32, blank=True, default="", verbose_name="昵称"
    )
    regions = models.CharField(
        max_length=255, blank=True, default="", verbose_name="地区"
    )
    avatar = models.CharField(max_length=255, blank=True, default="", verbose_name="头像")
    birthday = models.DateField(blank=True, default="1970-01-01", verbose_name="生日")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="性别")
    is_freeze = models.BooleanField(default=False, verbose_name="是否冻结")
    jwt_version = models.IntegerField(default=0, verbose_name="jwt版本")

    # 加密密码字段\
    def set_password(self, raw_password):
        self.password = PasswordUtil.encode(
            PasswordUtil(),
            raw_password,
            # "123456",
            # "100000"
            # settings.ENCODE_PASSWORD_SETTINGS["SALT"],
            # settings.ENCODE_PASSWORD_SETTINGS["ITERATIONS"],
        )

    class Meta:
        db_table = "user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
