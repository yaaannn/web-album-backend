from rest_framework import generics

from app.comment.models import Comment, Reply
from app.comment.serializers import CommentSerializer
from app.photo.models import Photo
from extension.auth.jwt_auth import UserJwtAuthentication
from extension.auth.login_auth import IsAuthPermission
from extension.cache.cache import CacheDecorator
from extension.json_response_ext import JsonResponse
from util.sensitive_filter_util import DFAFilter


class CommentCreateView(generics.GenericAPIView):
    """
    发表评论
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
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

    # authentication_classes = [UserJwtAuthentication]
    # permission_classes = [IsAuthPermission]
    serializer_class = CommentSerializer

    @CacheDecorator("r")
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

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]
    serializer_class = CommentSerializer

    @CacheDecorator("w")
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


# 发表回复
class CommentReplyCreateView(generics.GenericAPIView):
    """
    发表回复
    """

    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
    def post(self, request):
        """
        发表回复
        """
        res = JsonResponse()
        User = request.user
        data = request.data
        comment_id = data.get("comment_id")
        content = DFAFilter().filter(data.get("content"))
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            res.update(code=1, msg="评论不存在")
            return res.data
        Reply.objects.create(author=User, parent_comment_id=comment_id, content=content)
        res.update(msg="回复成功")
        return res.data


# 删除回复
class CommentReplyDeleteView(generics.GenericAPIView):
    authentication_classes = [UserJwtAuthentication]
    permission_classes = [IsAuthPermission]

    @CacheDecorator("w")
    def get(self, request):
        """
        删除回复
        """
        res = JsonResponse()
        reply_id = request.GET.get("reply_id")
        reply = Reply.objects.filter(id=reply_id).first()
        if not reply:
            res.update(code=1, msg="回复不存在")
            return res.data
        if not reply.author == request.user:
            res.update(code=1, msg="无权限")
            return res.data
        reply.delete()
        res.update(data="删除成功")
        return res.data
