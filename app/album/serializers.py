from rest_framework import serializers
from .models import Album
from extension.base.serializer import BaseModelSerializer


class AlbumSerializer(BaseModelSerializer, serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="album-detail")

    class Meta:
        model = Album
        fields = "__all__"
