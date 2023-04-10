from .models import Photo
from extension.base.serializer import BaseModelSerializer
from rest_framework import serializers
from app.user.serializers import SimpleUserInfoSerializer


class PhotoSerializer(BaseModelSerializer, serializers.ModelSerializer):
    # author = SimpleUserInfoSerializer()

    class Meta:
        model = Photo
        fields = "__all__"


class SimplePhotoSerializer(BaseModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "name", "url"]
