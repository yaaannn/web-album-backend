import os
from datetime import datetime
from uuid import uuid4

import ipfshttpclient as ipfs
from django.conf import settings
from django.core.cache import caches
from PIL import Image
from rest_framework import views
from rest_framework.parsers import MultiPartParser

from extension.auth.jwt_auth import UserJwtAuthentication
from extension.auth.login_auth import IsAuthPermission
from extension.json_response_ext import JsonResponse
from util.slider_captcha_util import SliderCaptchaUtil

# Create your views here.


# 上传图片到本地
class UploadPhotoToLocal(views.APIView):
    """
    上传图片到本地
    """

    authentication_classes = [UserJwtAuthentication]
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
            # Photo.objects.create(
            #     author=user,
            #     name=key,
            #     url="/media/upload/" + image_name,
            # )

        res.update(data={"url": "/media/upload/" + image_name})
        return res.data


# 获取滑块验证码
class GetSliderCaptcha(views.APIView):
    """
    获取滑块验证码
    """

    def get(self, request):
        res = JsonResponse()
        # 获取滑块验证码
        captcha = SliderCaptchaUtil()
        slider_img, bg_img, x, y = captcha.create()
        # 将滑块验证码的x坐标存入缓存
        cache = caches["default"]
        cache.set(f"slider_captcha", x, timeout=None)
        res.update(data={"slider_img": slider_img, "bg_img": bg_img, "y": y})
        return res.data


# 验证滑块验证码
class ValidateSliderCaptcha(views.APIView):
    """
    验证滑块验证码
    """

    def post(self, request):
        res = JsonResponse()
        # 获取滑块验证码
        x = request.data.get("x")
        # 获取缓存中的滑块验证码x坐标
        cache = caches["default"]
        slider_captcha_x = cache.get("slider_captcha")
        # 验证滑块验证码
        if x >= slider_captcha_x - 5 and x <= slider_captcha_x + 5:
            res.update(data={"result": True})
        else:
            res.update(data={"result": False})
        return res.data


# 上传图片到ipfs
class UploadPhotoToIPFS(views.APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        res = JsonResponse()
        images = request.FILES.items()
        key, image = next(images)
        # 连接ipfs节点
        ipfs_client = ipfs.connect("/ip4/127.0.0.1/tcp/5001")
        # 上传图片到ipfs
        image = ipfs_client.add(image)
        # 获取图片的hash值
        image_hash = image["Hash"]
        res.update(data={"url": image_hash})
        return res.data


# 列出敏感词，敏感词位置static/keywords
class ListSensitiveWords(views.APIView):
    def get(self, request):
        res = JsonResponse()
        # 获取敏感词文件路径
        keywords_path = settings.BASE_DIR / "static/keywords"
        # 读取敏感词文件
        with open(keywords_path, "r") as f:
            keywords = f.readlines()
        # 去除换行符
        keywords = [keyword.strip() for keyword in keywords]
        res.update(data={"keywords": keywords})
        return res.data


# 新增敏感词，敏感词位置static/keywords
class AddSensitiveWord(views.APIView):
    def post(self, request):
        res = JsonResponse()
        # 获取敏感词文件路径
        keywords_path = settings.BASE_DIR / "static/keywords"
        # 获取敏感词
        keyword = request.data.get("keyword")
        # 读取敏感词文件
        with open(keywords_path, "a") as f:
            f.write("\n" + keyword)
        res.update(data={"result": True})
        return res.data
