from rest_framework import generics

from app.archive.models import Like
from app.archive.serializers import *
from extension.auth.jwt_auth import UserJwtAuthentication
from extension.auth.login_auth import IsAuthPermission
from extension.cache.cache import CacheDecorator
from extension.json_response_ext import JsonResponse


# 对图片进行点赞
class LikePhotoView(generics.GenericAPIView):
    """
    对图片进行点赞
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
    def post(self, request):
        """
        点赞
        """
        res = JsonResponse()
        User = request.user
        data = request.data
        photo_id = data.get("photo_id")
        like = Like.objects.filter(user=User, photo_id=photo_id).first()
        if like:
            res.update(code=1, msg="已经点赞过了")
            return res.data
        Like.objects.create(user=User, photo_id=photo_id)
        res.update(data="点赞成功")
        return res.data


# 是否点赞
class IsLikePhotoView(generics.GenericAPIView):
    """
    是否点赞
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("r")
    def get(self, request):
        """
        是否点赞
        """
        res = JsonResponse()
        User = request.user
        photo_id = request.GET.get("photo_id")
        like = Like.objects.filter(user=User, photo_id=photo_id).first()
        if like:
            res.update(data={"is_like": True})
            return res.data
        res.update(data={"is_like": False})
        return res.data


# 获取我的点赞列表
class LikeListView(generics.GenericAPIView):
    """
    获取点赞列表
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = LikeSerializer

    @CacheDecorator("r")
    def get(self, request):
        """
        获取点赞列表
        """
        res = JsonResponse()
        User = request.user
        likes = Like.objects.filter(user=User)
        # 分页
        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(likes, many=True)
        res.update(data=serializer.data)
        return res.data


# 获取点赞量
class LikeCountView(generics.GenericAPIView):
    """
    获取点赞量
    """

    @CacheDecorator("r")
    def get(self, request):
        """
        获取点赞量
        """
        res = JsonResponse()
        photo_id = request.GET.get("photo_id")
        likes = Like.objects.filter(photo_id=photo_id)
        res.update(data={"count": likes.count()})
        return res.data


# 取消点赞
class CancelLikePhotoView(generics.GenericAPIView):
    """
    取消点赞
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
    def post(self, request):
        """
        取消点赞
        """
        res = JsonResponse()
        User = request.user
        data = request.data
        photo_id = data.get("photo_id")
        like = Like.objects.filter(user=User, photo_id=photo_id).first()
        if not like:
            res.update(code=1, msg="还未点赞")
            return res.data
        like.delete()
        res.update(data="取消点赞成功")
        return res.data
