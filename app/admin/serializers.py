from rest_framework import serializers

from app.album.models import Album
from app.photo.models import Photo
from app.user.models import User


class AdminLoginSerializer(serializers.Serializer):
    """管理员登录序列化器"""

    username = serializers.CharField()
    password = serializers.CharField()


class AlbumSerializer(serializers.ModelSerializer):
    """相册序列化器"""

    class Meta:
        model = Album
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = "__all__"


class PhotoSerializer(serializers.ModelSerializer):
    """图片序列化器"""

    author = UserSerializer()
    album = AlbumSerializer()

    class Meta:
        model = Photo
        fields = "__all__"
