from rest_framework import serializers

from app.comment.models import Comment, Reply
from app.user.serializers import SimpleUserInfoSerializer


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
