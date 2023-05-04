from rest_framework import serializers
from .models import Album
from app.user.serializers import SimpleUserInfoSerializer


class AlbumSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField()
    # author = SimpleUserInfoSerializer()

    class Meta:
        model = Album
        fields = "__all__"
