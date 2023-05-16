from rest_framework import serializers
from .models import Partition


class PartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partition
        fields = "__all__"
