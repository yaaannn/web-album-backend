from rest_framework import generics

from app.photo.models import Photo
from extension.auth.jwt_auth import JwtAuthentication
from extension.json_response_ext import JsonResponse
from extension.permission_ext import IsAuthPermission

from .models import Collection
from .serializers import CollectionSerializer


class CollectionCreateView(generics.GenericAPIView):
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
        collection = Collection.objects.filter(user=user, photo=photo).first()
        if collection:
            res.update(code=1, msg="已收藏")
            return res.data
        Collection.objects.create(user=user, photo=photo)
        res.update(data="收藏成功")
        return res.data


class CollectionDeleteView(generics.GenericAPIView):
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
        collection = Collection.objects.filter(user=user, photo=photo).first()
        if not collection:
            res.update(code=1, msg="未收藏")
            return res.data
        collection.delete()
        res.update(data="取消收藏成功")
        return res.data


class CollectionListView(generics.GenericAPIView):
    """
    收藏列表
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthPermission,)
    serializer_class = CollectionSerializer

    def get(self, request):
        res = JsonResponse()
        user = request.user
        collections = Collection.objects.filter(user=user)

        collection_list = self.serializer_class(collections, many=True).data

        res.update(data=collection_list)
        return res.data
