from extension.base.serializer import BaseModelSerializer
from rest_framework import serializers
from app.user.serializers import SimpleUserInfoSerializer
from .models import Comment


class CommentSerializer(BaseModelSerializer, serializers.ModelSerializer):
    author = SimpleUserInfoSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
