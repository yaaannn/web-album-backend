from rest_framework import serializers
from app.partition.models import Partition


class PartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partition
        fields = "__all__"
