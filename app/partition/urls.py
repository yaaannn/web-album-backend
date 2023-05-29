from django.urls import path

from app.partition.views import (
    CreatePartitionView,
    DeletePartitionView,
    ListPartitionView,
    UpdatePartitionView,
)

urlpatterns = [
    path("list", ListPartitionView.as_view(), name="list-partition"),
    path("create", CreatePartitionView.as_view(), name="create-partition"),
    path("delete", DeletePartitionView.as_view(), name="delete-partition"),
    path("update", UpdatePartitionView.as_view(), name="update-partition"),
]
