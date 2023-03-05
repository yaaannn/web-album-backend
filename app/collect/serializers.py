from extension.base.serializer import BaseModelSerializer
from .models import Collect
from rest_framework import serializers


class CollectSerializer(BaseModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = "__all__"
