from extension.base.serializer import BaseModelSerializer
from .models import Collection
from rest_framework import serializers


class CollectionSerializer(BaseModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"
