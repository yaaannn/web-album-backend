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
from extension.jwt_auth_ext import JwtAuthentication
from extension.permission_ext import IsAuthPermission
from util.verification_code_util import create_code_image, create_random_code

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

    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthPermission]
    parser_classes = [MultiPartParser]

    def post(self, request):
        res = JsonResponse()
        images = request.FILES.items()
        image_list = []
        for key, image in images:
            image_name = image.name
            image_size = image.size
            check_image = os.path.splitext(image_name)[1]
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
        res.update(data={"url": "http://127.0.0.1:8000/media/upload/" + image_list[1]})
        return res.data
