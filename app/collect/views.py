from rest_framework import generics

from app.photo.models import Photo
from extension.auth.jwt_auth import JwtAuthentication
from extension.json_response_ext import JsonResponse
from extension.permission_ext import IsAuthPermission

from .models import Collect
from .serializers import CollectSerializer


class CollectCreateView(generics.GenericAPIView):
    """
    收藏
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthPermission,)

    def get(self, request):
        res = JsonResponse()
        user = request.user
        photo_id = request.GET.get("photo_id")
        photo = Photo.objects.filter(id=photo_id).first()
        collect = Collect.objects.filter(user=user, photo=photo).first()
        if collect:
            res.update(code=1, msg="已收藏")
            return res.data
        Collect.objects.create(user=user, photo=photo)
        res.update(data="收藏成功")
        return res.data


class CollectDeleteView(generics.GenericAPIView):
    """
    取消收藏
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthPermission,)

    def get(self, request):
        res = JsonResponse()
        user = request.user
        photo_id = request.GET.get("photo_id")
        photo = Photo.objects.filter(id=photo_id).first()
        collect = Collect.objects.filter(user=user, photo=photo).first()
        if not collect:
            res.update(code=1, msg="未收藏")
            return res.data
        collect.delete()
        res.update(data="取消收藏成功")
        return res.data


class CollectListView(generics.GenericAPIView):
    """
    收藏列表
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthPermission,)
    serializer_class = CollectSerializer

    def get(self, request):
        res = JsonResponse()
        user = request.user
        collects = Collect.objects.filter(user=user)

        collect_list = self.serializer_class(collects, many=True).data

        res.update(data=collect_list)
        return res.data
