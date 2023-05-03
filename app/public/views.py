import logging
import os
from datetime import datetime
from io import BytesIO
from uuid import uuid4

from django.conf import settings
from django.core.cache import caches
from django.shortcuts import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from rest_framework import views
from rest_framework.parsers import MultiPartParser

from extension.json_response_ext import JsonResponse
from extension.auth.jwt_auth import JwtAuthentication
from extension.permission_ext import IsAuthPermission
from util.verification_code_util import create_code_image, create_random_code
from util.slider_captcha_util import SliderCaptchaUtil

# Create your views here.


def generate_captcha_code(request):
    """
    生成验证码
    :param request:
    :return:
    """
    code = create_random_code(4, True)
    image = create_code_image(code)
    cache = caches["default"]
    cache.set(f"captcha", code, timeout=None)
    stream = BytesIO()
    image.save(stream, "png")
    return HttpResponse(stream.getvalue(), content_type="image/png")


class UploadImageToLocal(views.APIView):
    """
    上传图片到本地
    """

    # authentication_classes = [JwtAuthentication]
    # permission_classes = [IsAuthPermission]
    # parser_classes = [MultiPartParser]

    def post(self, request):
        res = JsonResponse()
        images = request.FILES.items()
        image_list = []
        for key, image in images:
            image_name = image.name
            image_size = image.size
            check_image = os.path.splitext(image_name)[1]
            print(check_image)
            if check_image[1:].lower() not in settings.IMAGE_FILE_CHECK:
                res.update(
                    msg=f"{image_name} Not the specified type, alow type({'/'.join(settings.IMAGE_FILE_CHECK)})"
                )
                return res.data
            if image_size > settings.IMAGE_FILE_SIZE:
                res.update(
                    msg=f"{image_name} File size more than {settings.IMAGE_FILE_SIZE/1024/1024} mb"
                )
                return res.data

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
            image_list.append(image_name)
        image_list_url = ["http://127.0.0.1:8000/media/upload/" + i for i in image_list]
        res.update(data={"url": image_list_url})
        return res.data


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
        print(x, y)
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
