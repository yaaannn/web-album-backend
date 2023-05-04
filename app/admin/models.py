from django.db import models

# 创建管理员模型类，


class Admin(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=255, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")
    is_freeze = models.BooleanField(default=False, verbose_name="是否冻结")
    jwt_version = models.IntegerField(default=0, verbose_name="jwt版本")

    class Meta:
        db_table = "a_admin"
        verbose_name = "管理员表"
        verbose_name_plural = verbose_name
