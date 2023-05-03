from .models import Like
from extension.base.serializer import BaseModelSerializer
from app.photo.serializers import SimplePhotoSerializer


class LikeSerializer(BaseModelSerializer):
    photo = SimplePhotoSerializer()

    class Meta:
        model = Like
        fields = "__all__"
