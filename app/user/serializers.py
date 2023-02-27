from .models import User
from rest_framework import serializers

# from extension.base_serializer_ext import BaseModelSerializer
from extension.base.serializer import BaseModelSerializer


class UserViewSetSerializer(BaseModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CreateUserSerializer(serializers.Serializer):
    """
    用户注册序列化器
    """

    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def create(self, validated_data):
        """
        用户注册
        写法一：重写 create 方法，将密码加密
        """
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    # class Meta:
    #     model = User
    #     fields = ("username", "password", "email")


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""

    username = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField()


# 修改用户密码序列化器
class ChangePasswordSerializer(serializers.Serializer):
    # username = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()


# 发送重置密码邮件序列化器
class SendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


# 重置用户密码序列化器
class ResetPasswordSerializer(serializers.Serializer):
    # username = serializers.CharField()
    email = serializers.EmailField()
    new_password = serializers.CharField()
    # 验证码
    code = serializers.CharField()


# 修改用户信息序列化器
class ModifyUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            # "username",
            # "email",
            "mobile",
            "nickname",
            "regions",
            "avatar",
            "birthday",
            "gender",
            # "create_time",
        )
