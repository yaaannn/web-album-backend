from rest_framework import serializers

from app.album.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField()
    # author = SimpleUserInfoSerializer()

    class Meta:
        model = Album
        fields = "__all__"
