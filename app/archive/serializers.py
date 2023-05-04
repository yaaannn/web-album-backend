from .models import Like
from app.photo.serializers import SimplePhotoSerializer
from rest_framework import serializers


class LikeSerializer(serializers.ModelSerializer):
    photo = SimplePhotoSerializer()

    class Meta:
        model = Like
        fields = "__all__"
