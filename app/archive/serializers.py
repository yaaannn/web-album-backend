from rest_framework import serializers

from app.archive.models import Like
from app.photo.serializers import SimplePhotoSerializer


class LikeSerializer(serializers.ModelSerializer):
    photo = SimplePhotoSerializer()

    class Meta:
        model = Like
        fields = "__all__"
