import os
from datetime import datetime
from uuid import uuid4

from django.conf import settings
from PIL import Image
from rest_framework import views, generics
from rest_framework.parsers import MultiPartParser

from app.photo.models import Photo
from extension.auth.jwt_auth import JwtAuthentication
from extension.json_response_ext import JsonResponse
from extension.permission_ext import IsAuthPermission
from .serializers import PhotoSerializer

# 上传图片到本地
class UploadPhotoToLocal(views.APIView):
    """
    上传图片到本地
    """

    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthPermission]
    parser_classes = [MultiPartParser]

    def post(self, request):
        user = request.user
        res = JsonResponse()
        images = request.FILES.items()

        for key, image in images:
            # 检查图片格式及大小，交给前端处理
            check_image = os.path.splitext(image.name)[1]
            base_dir = os.path.join(
                settings.UPLOAD_DIR, datetime.now().strftime("%Y-%m")
            )
            if not os.path.exists(base_dir):
                os.makedirs(base_dir, exist_ok=True)
                os.chmod(base_dir, 0o755)

            image_name = os.path.join(
                datetime.now().strftime("%Y-%m"),
                "%su" % request.user.id
                + str(uuid4()).replace("-", "")
                + check_image.lower(),
            )

            image_path = settings.UPLOAD_DIR / image_name
            if check_image[1:].lower() in ("jpg", "jpeg", "png", "gif"):
                image = Image.open(image)
                image.save(image_path)
            else:
                with open(image_path, "wb") as f:
                    for chunk in image.chunks():
                        f.write(chunk)
            Photo.objects.create(
                author=user, name=key, url="/media/upload/" + image_name
            )

        res.update()
        return res.data


# 获取用户所有图片
class ListPhotoView(generics.GenericAPIView):
    """
    获取用户所有图片
    """

    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = PhotoSerializer

    def get(self, request):
        res = JsonResponse()
        user = request.user
        photos = Photo.objects.filter(author=user)
        serializer = self.get_serializer(photos, many=True)
        res.update(data=serializer.data)
        return res.data


# 删除图片
class DeletePhotoView(views.APIView):
    """
    删除图片
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
        pk = request.query_params.get("id")
        queryset = Photo.objects.filter(author=user, id=pk)
        if queryset.exists():
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

    def get(self, request):
        res = JsonResponse()
        photos = Photo.objects.filter(status="0")
        serializer = self.get_serializer(photos, many=True)
        res.update(data=serializer.data)
        return res.data


# 修改用户图片状态
class UpdatePhotoStatusView(views.APIView):
    """
    修改用户图片状态
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
        pk = request.query_params.get("id")
        status = request.query_params.get("status")
        queryset = Photo.objects.filter(author=user, id=pk)
        if queryset.exists():
            queryset.update(status=str(status))
            res.update(data="修改成功")
        else:
            res.update(code=2, msg="修改失败")
        return res.data


# 修改照片描述
class UpdatePhotoDescView(views.APIView):
    """
    修改照片描述
    """

    authentication_classes = [
        JwtAuthentication,
    ]
    permission_classes = [
        IsAuthPermission,
    ]

    def post(self, request):
        res = JsonResponse()
        user = request.user
        pk = request.query_params.get("id")
        desc = request.data.get("desc")
        queryset = Photo.objects.filter(author=user, id=pk)
        if queryset.exists():
            queryset.update(desc=desc)
            res.update(data="修改成功")
        else:
            res.update(code=2, msg="修改失败")
        return res.data
