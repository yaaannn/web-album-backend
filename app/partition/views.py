from app.partition.models import Partition
from .serializers import PartitionSerializer

from rest_framework import views
from extension.auth.jwt_auth import AdminJwtAuthentication
from extension.permission_ext import IsAuthPermission
from extension.json_response_ext import JsonResponse


# 获取所有分区
class ListPartitionView(views.APIView):
    serializer_class = PartitionSerializer

    def get(self, request):
        res = JsonResponse()
        partitions = Partition.objects.all()
        partition_list = self.serializer_class(partitions, many=True).data
        res.update(data=partition_list)
        return res.data


# 新增分区
class CreatePartitionView(views.APIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]

    def post(self, request):
        res = JsonResponse()
        name = request.data.get("name")
        if Partition.objects.filter(name=name).exists():
            res.update(code=1, msg="分区已存在")
            return res.data
        Partition.objects.create(name=name)
        res.update(msg="创建成功")
        return res.data


# 删除分区
class DeletePartitionView(views.APIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]

    def post(self, request):
        res = JsonResponse()
        id = request.data.get("id")
        if not Partition.objects.filter(id=id).exists():
            res.update(code=1, msg="分区不存在")
            return res.data
        Partition.objects.filter(id=id).delete()
        res.update(msg="删除成功")
        return res.data


# 修改分区
class UpdatePartitionView(views.APIView):
    authentication_classes = [AdminJwtAuthentication]
    permission_classes = [IsAuthPermission]

    def post(self, request):
        res = JsonResponse()
        id = request.data.get("id")
        name = request.data.get("name")
        if not Partition.objects.filter(id=id).exists():
            res.update(code=1, msg="分区不存在")
            return res.data
        Partition.objects.filter(id=id).update(name=name)
        res.update(msg="修改成功")
        return res.data
