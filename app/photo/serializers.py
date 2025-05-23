from rest_framework import serializers

from app.photo.models import Photo
from app.user.serializers import SimpleUserInfoSerializer


class PhotoSerializer(serializers.ModelSerializer):
    author = SimpleUserInfoSerializer()

    class Meta:
        model = Photo
        fields = "__all__"


class SimplePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "name", "url"]
