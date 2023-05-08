from django.shortcuts import render
import logging

from django.core.cache import caches
from django.core.mail import send_mail
from rest_framework import generics

from app.admin.models import Admin

from app.photo.models import Photo
from app.user.serializers import *
from extension.json_response_ext import JsonResponse
from extension.auth.jwt_auth import AdminJwtAuthentication

# from extension.jwt_token_ext import JwtToken
from extension.cache.cache import CacheDecorator
from extension.permission_ext import IsAuthPermission
from util.password_util import PasswordUtil
from util.verification_code_util import create_random_code
from util.jwt_token_util import JwtTokenUtil

from .serializers import AdminLoginSerializer
from .serializers import UserSerializer, PhotoSerializer, AlbumSerializer
from app.comment.serializers import CommentSerializer
from app.comment.models import Comment


# 管理员登录
class AdminLoginView(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request):
        res = JsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        admin = Admin.objects.filter(username=username).first()
        if not admin:
            res.update(msg="管理员不存在", code=2)
            return res.data

        # if not user.password == password:
        if not password == admin.password:
            res.update(msg="密码错误", code=2)
            return res.data
        admin.jwt_version += 1
        payload = {"id": admin.id, "jwt_version": admin.jwt_version}
        logging.debug(payload)
        jwt_token = JwtTokenUtil().encode_user(payload)
        admin.save()
        res.update(
            data={
                "username": admin.username,
                "token": jwt_token,
                "jwt_version": admin.jwt_version,
            }
        )
        return res.data


# 获取管理员信息
class GetAdminInfoView(generics.GenericAPIView):
    """
    获取管理员信息
    """

    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        user = request.user
        print(user)
        res.update(
            data={
                "admin_info": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }
        )
        return res.data


# 获取用户列表
class GetUserListView(generics.GenericAPIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = UserSerializer

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        users = User.objects.all()
        # 分页
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserViewSetSerializer(users, many=True)
        res.update(data=serializer.data)
        return res.data


# 删除用户
class DeleteUserView(generics.GenericAPIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
    def get(self, request):
        res = JsonResponse()
        pk = request.query_params.get("id")
        queryset = User.objects.filter(id=pk)
        if queryset.exists():
            queryset.delete()
            res.update(msg="删除成功")
            return res.data
        res.update(msg="删除失败", code=2)
        return res.data


# 冻结/解冻用户
class FreezeUserView(generics.GenericAPIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
    def get(self, request):
        res = JsonResponse()
        pk = request.query_params.get("id")
        queryset = User.objects.filter(id=pk)
        if queryset.exists():
            user = queryset.first()
            user.is_freeze = not user.is_freeze
            user.save()
            res.update(msg="操作成功")
            return res.data
        res.update(msg="操作失败", code=2)
        return res.data


# 获取照片列表
class GetPhotoListView(generics.GenericAPIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = PhotoSerializer

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        photos = Photo.objects.all()
        # 分页
        page = self.paginate_queryset(photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PhotoSerializer(photos, many=True)
        res.update(data=serializer.data)
        return res.data


# 删除照片
class DeletePhotoView(generics.GenericAPIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
    def get(self, request):
        res = JsonResponse()
        pk = request.query_params.get("id")
        queryset = Photo.objects.filter(id=pk)
        if queryset.exists():
            queryset.delete()
            res.update(msg="删除成功")
            return res.data
        res.update(msg="删除失败", code=2)
        return res.data


# 获取评论列表
class GetCommentListView(generics.GenericAPIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = CommentSerializer

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        comments = Comment.objects.all()
        # 分页
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        res.update(data=serializer.data)
        return res.data
