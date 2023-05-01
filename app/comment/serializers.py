from extension.base.serializer import BaseModelSerializer
from rest_framework import serializers
from app.user.serializers import SimpleUserInfoSerializer
from .models import Comment, Reply


# class ReplySerializer(BaseModelSerializer, serializers.ModelSerializer):
#     author = SimpleUserInfoSerializer()

#     class Meta:
#         model = Reply
#         fields = "__all__"


# class CommentSerializer(BaseModelSerializer, serializers.ModelSerializer):
#     author = SimpleUserInfoSerializer()
#     # reply = ReplySerializer()

#     class Meta:
#         model = Comment
#         fields = "__all__"


class CommentReplySerializer(serializers.ModelSerializer):
    author = SimpleUserInfoSerializer()

    class Meta:
        model = Reply
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserInfoSerializer()
    replies = CommentReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
