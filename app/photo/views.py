import os
from django.conf import settings
from pathlib import Path
from django.db.models import F
from rest_framework import generics, views

from app.photo.models import Photo
from extension.auth.jwt_auth import UserJwtAuthentication
from extension.cache.cache import CacheDecorator
from extension.json_response_ext import JsonResponse
from extension.permission_ext import IsAuthPermission

from app.photo.serializers import PhotoSerializer
from PIL import Image, ImageFilter, ImageFont, ImageDraw


# 获取用户所有图片
class ListPhotoView(generics.GenericAPIView):
    """
    获取用户所有图片
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = PhotoSerializer

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        user = request.user
        photos = Photo.objects.filter(author=user)
        # 分页
        page = self.paginate_queryset(photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(photos, many=True)
        res.update(data=serializer.data)
        return res.data


# 删除图片
class DeletePhotoView(views.APIView):
    """
    删除图片
    """

    authentication_classes = [
        UserJwtAuthentication,
    ]
    permission_classes = [
        IsAuthPermission,
    ]

    @CacheDecorator("w")
    def get(self, request):
        res = JsonResponse()
        user = request.user
        pk = request.query_params.get("id")
        queryset = Photo.objects.filter(author=user, id=pk)
        if queryset.exists():
            # 删除本地图片
            # print(queryset.first().url[1:])
            os.remove(queryset.first().url[1:])
            queryset.delete()
            res.update(data="删除成功")

        else:
            res.update(code=2, msg="删除失败")
        return res.data


# 获取所有公开图片
class ListPublicPhotoView(generics.GenericAPIView):
    """
    获取所有公开图片
    """

    serializer_class = PhotoSerializer

    # pagination_class = Pagination

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        photos = Photo.objects.filter(is_public=True)
        # 分页
        page = self.paginate_queryset(photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(photos, many=True)
        res.update(data=serializer.data)
        return res.data


# 从相册中删除照片
class DeletePhotoFromAlbumView(views.APIView):
    """
    从相册中删除照片
    """

    authentication_classes = [
        UserJwtAuthentication,
    ]
    permission_classes = [
        IsAuthPermission,
    ]

    @CacheDecorator("w")
    def get(self, request):
        res = JsonResponse()
        user = request.user
        pk = request.query_params.get("id")
        queryset = Photo.objects.filter(author=user, id=pk)
        if queryset.exists():
            queryset.update(album_id=None)
            res.update(data="删除成功")
        else:
            res.update(code=2, msg="删除失败")
        return res.data


# 获取相册中所有照片
class ListAlbumPhotoView(generics.GenericAPIView):
    """
    获取相册中所有照片
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = PhotoSerializer

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        user = request.user
        album_id = request.query_params.get("album_id")
        photos = Photo.objects.filter(author=user, album_id=album_id)
        # 分页
        page = self.paginate_queryset(photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(photos, many=True)
        res.update(data=serializer.data)
        return res.data


# 上传照片信息（名称，描述，相册，状态）
class UploadPhotoInfoView(generics.CreateAPIView):
    """
    上传照片信息（名称，描述，相册，状态）
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]
    # serializer_class = UpdatePhotoSerializer

    @CacheDecorator("w")
    def post(self, request):
        res = JsonResponse()
        user = request.user
        name = request.data.get("name")
        desc = request.data.get("desc")
        album_id = request.data.get("album_id")
        is_public = request.data.get("is_public")
        url = request.data.get("url")
        is_watermark = request.data.get("is_watermark")
        # 添加水印
        if is_watermark:
            img_path = f"{settings.BASE_DIR}{url}"
            img = Image.open(img_path)
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            txt = Image.new("RGBA", img.size, (0, 0, 0, 0))
            fnt = ImageFont.truetype(
                f"{settings.BASE_DIR}/static/font/SmileySans-Oblique.ttf", 40
            )
            d = ImageDraw.Draw(txt)
            d.text(
                (img.size[0] - 200, img.size[1] - 100),
                request.user.username,
                font=fnt,
                fill=(255, 255, 255, 255),
            )
            out = Image.alpha_composite(img, txt)
            out.save(img_path)
        queryset = Photo.objects.filter(author=user, name=name)
        if queryset.exists():
            res.update(code=2, msg="照片已存在")
        else:
            Photo.objects.create(
                author=user,
                name=name,
                desc=desc,
                album_id=album_id,
                is_public=is_public,
                url=url,
            )
            res.update(data="添加成功")
        return res.data


# 获取照片信息
class GetPhotoInfoView(generics.GenericAPIView):
    """
    获取照片信息
    """

    # authentication_classes = [UserJwtAuthentication]
    # permission_classes = [IsAuthPermission]
    serializer_class = PhotoSerializer

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        pk = request.query_params.get("id")
        queryset = Photo.objects.filter(id=pk)
        # 启用缓存后，这里的点击量+1会失效,因为缓存的是序列化后的数据，而不是数据库中的数据，该如何解决？
        # 利用信号机制，实现点击量+1，在信号中实现，但是信号中没有request对象，无法获取用户信息
        # 点击量+1
        queryset.update(click=F("click") + 1)
        if queryset.exists():
            serializer = self.get_serializer(queryset[0])
            res.update(data=serializer.data)
        else:
            res.update(code=2, msg="照片不存在")
        return res.data


# 获取某一用户的公开照片
class GetPublicPhotoByUidView(generics.GenericAPIView):
    """
    获取某一用户的公开照片
    """

    # authentication_classes = [UserJwtAuthentication]
    # permission_classes = [IsAuthPermission]
    serializer_class = PhotoSerializer

    @CacheDecorator("r")
    def get(self, request):
        res = JsonResponse()
        user_id = request.query_params.get("id")
        photos = Photo.objects.filter(author_id=user_id, is_public=True)
        # 分页
        page = self.paginate_queryset(photos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(photos, many=True)
        res.update(data=serializer.data)
        return res.data


class UpdatePhotoInfoView(views.APIView):
    """
    更新照片信息
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
    def post(self, request):
        res = JsonResponse()
        user = request.user
        pk = request.data.get("id")
        name = request.data.get("name")
        desc = request.data.get("desc")
        album_id = request.data.get("album_id")
        is_public = request.data.get("is_public")
        queryset = Photo.objects.filter(author=user, id=pk)
        if queryset.exists():
            queryset.update(
                name=name,
                desc=desc,
                album_id=album_id,
                is_public=is_public,
            )
            res.update(data="修改成功")
        else:
            res.update(code=2, msg="照片不存在")
        return res.data
