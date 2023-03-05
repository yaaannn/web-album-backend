from rest_framework import serializers
from .models import Album
from app.user.serializers import SimpleUserInfoSerializer
from extension.base.serializer import BaseModelSerializer


class AlbumSerializer(BaseModelSerializer, serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="album-detail")
    author = SimpleUserInfoSerializer()

    class Meta:
        model = Album
        fields = "__all__"
