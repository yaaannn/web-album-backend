from rest_framework import generics

from extension.json_response_ext import JsonResponse
from extension.jwt_auth_ext import JwtAuthentication
from extension.permission_ext import IsAuthPermission

from .models import Album
from .serializers import AlbumSerializer


class AlbumCreateView(generics.GenericAPIView):
    serializer_class = AlbumSerializer
    authentication_classes = [
        JwtAuthentication,
    ]
    permission_classes = [
        IsAuthPermission,
    ]

    def post(self, request):
        res = JsonResponse()
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)
        # res.update(data=serializer.data)
        if serializer.data:
            res.update(data="创建成功")
        return res.data


class AlbumListView(generics.GenericAPIView):
    serializer_class = AlbumSerializer
    authentication_classes = [
        JwtAuthentication,
    ]
    permission_classes = [
        IsAuthPermission,
    ]

    def get(self, request):
        res = JsonResponse()
        user = request.user
        queryset = Album.objects.filter(author=user)
        serializer = self.get_serializer(queryset, many=True)
        res.update(data=serializer.data)
        return res.data


class AlbumDeleteView(generics.GenericAPIView):
    serializer_class = AlbumSerializer
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
        queryset = Album.objects.filter(author=user, id=pk)
        if queryset.exists():
            queryset.delete()
            res.update(data="删除成功")
        else:
            res.update(code=2, msg="删除失败")
        return res.data


class AlbumUpdateView(generics.GenericAPIView):
    serializer_class = AlbumSerializer
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

        if Album.objects.update_or_create(author=user, id=pk, defaults=request.data):
            res.update(data="更新成功")
        else:
            res.update(code=2, msg="更新失败")
        return res.data


class AlbumDetailView(generics.GenericAPIView):
    serializer_class = AlbumSerializer
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
        queryset = Album.objects.filter(author=user, id=pk)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            res.update(data=serializer.data)
        else:
            res.update(code=2, msg="查询失败")
        return res.data
