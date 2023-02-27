import logging

from django.core.cache import caches
from django.core.mail import send_mail
from rest_framework import generics

from app.user.models import User
from app.user.serializers import *
from extension.json_response_ext import JsonResponse
from extension.jwt_auth_ext import JwtAuthentication
from extension.jwt_token_ext import JwtToken
from extension.permission_ext import IsAuthPermission
from util.password_util import PasswordUtil
from util.verification_code_util import create_random_code


class UserLoginView(generics.GenericAPIView):
    """
    用户登录
    """

    serializer_class = UserLoginSerializer

    def post(self, request):

        res = JsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        code = serializer.validated_data["code"]
        if not code == caches["default"].get("captcha"):
            res.update(msg="验证码错误", code=2)
            return res.data

        user = User.objects.filter(username=username).first()
        if not user:
            res.update(msg="用户不存在", code=2)
            return res.data

        # if not user.password == password:
        if not PasswordUtil.verify(PasswordUtil(), password, user.password):
            res.update(msg="密码错误", code=2)
            return res.data
        user.jwt_version += 1
        payload = {"id": user.id, "jwt_version": user.jwt_version}
        logging.debug(payload)
        jwt_token = JwtToken().encode_user(payload)
        user.save()
        res.update(data={"username": user.username, "token": jwt_token})
        return res.data


class UserRegisterView(generics.GenericAPIView):
    """
    用户注册
    写法二
    """

    serializer_class = CreateUserSerializer

    def post(self, request):
        res = JsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        email = serializer.validated_data["email"]
        user = User.objects.filter(username=username).first()
        if user:
            res.update(msg="用户已存在", code=2)
            return res.data
        user = User.objects.create(username=username, password=password, email=email)
        user.set_password(password)
        user.save()
        res.update(data={"username": user.username})
        return res.data


class ChangePasswordView(generics.GenericAPIView):
    """
    修改密码
    """

    authentication_classes = [
        JwtAuthentication,
    ]
    permission_classes = [
        IsAuthPermission,
    ]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        res = JsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # username = serializer.validated_data["username"]
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        # user = User.objects.filter(username=username).first()
        user = request.user
        if not PasswordUtil.verify(PasswordUtil(), old_password, user.password):
            res.update(msg="旧密码错误", code=2)
            return res.data
        user.set_password(new_password)
        user.save()
        # res.update(data={"username": user.username})
        return res.data


class SendResetPasswordEmailView(generics.GenericAPIView):
    """
    发送重置密码邮件
    """

    serializer_class = SendResetPasswordEmailSerializer

    def post(self, request):
        res = JsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            res.update(msg="用户不存在", code=2)
            return res.data
        code = create_random_code(6, False)
        cache = caches["default"]
        cache.set(f"reset_password_{email}", code, timeout=60 * 5)
        logging.info("本次验证码为: " + f"{code}")
        send_mail("reset password", f"{code}", "admin@localhost", [email])
        # user.send_reset_password_email()
        # res.update(data={"email": user.email})
        return res.data


class ResetPasswordView(generics.GenericAPIView):
    """
    重置密码
    """

    serializer_class = ResetPasswordSerializer

    def post(self, request):
        res = JsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        new_password = serializer.validated_data["new_password"]
        # redis_conn = get_redis_connection("default")
        # redis_code = redis_conn.get(f"reset_password_{email}")
        cache = caches["default"]
        redis_code = cache.get(f"reset_password_{email}")
        if not redis_code:
            res.update(msg="验证码已过期", code=2)
            return res.data
        if not code == redis_code:
            res.update(msg="验证码错误", code=2)
            return res.data
        user = User.objects.filter(email=email).first()
        user.set_password(new_password)
        user.save()
        # res.update(data={"username": user.username})
        return res.data


class GetUserInfoView(generics.GenericAPIView):
    """
    获取用户信息
    """

    authentication_classes = [
        JwtAuthentication,
    ]
    permission_classes = [
        IsAuthPermission,
    ]

    def get(self, request):
        res = JsonResponse()
        user = request.user
        res.update(
            data={
                "user_info": {
                    "username": user.username,
                    "email": user.email,
                    "mobile": user.mobile,
                    "nickname": user.nickname,
                    "regions": user.regions,
                    "avatar": user.avatar,
                    "birthday": user.birthday,
                    "gender": user.gender,
                    "create_time": user.create_time,
                }
            }
        )
        return res.data


class ModifyUserInfoView(generics.GenericAPIView):
    serializer_class = ModifyUserInfoSerializer
    authentication_classes = [
        JwtAuthentication,
    ]
    permission_classes = [
        IsAuthPermission,
    ]

    def post(self, request):
        res = JsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        for key, value in serializer.validated_data.items():
            setattr(user, key, value)
        user.save()
        return res.data
