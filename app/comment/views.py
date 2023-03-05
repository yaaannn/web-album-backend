from rest_framework import generics

from app.photo.models import Photo
from app.user.models import User
from extension.auth.jwt_auth import JwtAuthentication
from extension.json_response_ext import JsonResponse
from extension.permission_ext import IsAuthPermission
from util.sensitive_filter_util import DFAFilter

from .models import Comment
from .serializers import CommentSerializer


class CommentCreateView(generics.GenericAPIView):
    """
    发表评论
    """

    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = CommentSerializer

    def post(self, request):
        """
        评论
        """
        res = JsonResponse()
        User = request.user
        data = request.data
        photo_id = data.get("photo_id")
        content = DFAFilter().filter(data.get("content"))
        photo = Photo.objects.filter(id=photo_id).first()
        if not photo:
            res.update(code=1, msg="照片不存在")
            return res.data
        Comment.objects.create(author=User, photo=photo, content=content)
        res.update(data="评论成功")
        return res.data


class CommentListView(generics.GenericAPIView):
    """
    评论列表
    """

    # authentication_classes = [JwtAuthentication]
    # permission_classes = [IsAuthPermission]
    serializer_class = CommentSerializer

    def get(self, request):
        """
        评论列表
        """
        res = JsonResponse()
        photo_id = request.GET.get("photo_id")
        photo = Photo.objects.filter(id=photo_id).first()
        if not photo:
            res.update(code=1, msg="照片不存在")
            return res.data
        comments = Comment.objects.filter(photo=photo)
        comment_list = self.serializer_class(comments, many=True).data
        res.update(data=comment_list)
        return res.data


class CommentDeleteView(generics.GenericAPIView):
    """
    删除评论
    """

    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = CommentSerializer

    def get(self, request):
        """
        删除评论
        """
        res = JsonResponse()
        comment_id = request.GET.get("comment_id")
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            res.update(code=1, msg="评论不存在")
            return res.data
        if not comment.author == request.user:
            res.update(code=1, msg="无权限")
            return res.data
        comment.delete()
        res.update(data="删除成功")
        return res.data
