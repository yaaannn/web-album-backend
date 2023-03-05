from rest_framework import generics

from app.photo.models import Photo
from extension.auth.jwt_auth import JwtAuthentication
from extension.json_response_ext import JsonResponse
from extension.permission_ext import IsAuthPermission

from .models import Tag
from .serializers import TagSerializer


class TagListView(generics.GenericAPIView):
    """
    标签列表
    """

    # authentication_classes = (JwtAuthentication,)
    # permission_classes = (IsAuthPermission,)
    serializer_class = TagSerializer

    def get(self, request):
        res = JsonResponse()
        tags = Tag.objects.all()
        tag_list = self.get_serializer(tags, many=True).data
        res.update(data=tag_list)
        return res.data


class TagCreateView(generics.GenericAPIView):
    """
    添加标签
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthPermission,)
    serializer_class = TagSerializer

    def post(self, request):
        res = JsonResponse()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res.update(data="添加标签成功")

        return res.data


class TagDeleteView(generics.GenericAPIView):
    """
    删除标签
    """

    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthPermission,)

    def get(self, request):
        res = JsonResponse()
        tag_id = request.GET.get("tag_id")
        tag = Tag.objects.filter(id=tag_id).first()
        if not tag:
            res.update(code=1, msg="标签不存在")
            return res.data
        tag.delete()
        res.update(data="删除标签成功")
        return res.data
