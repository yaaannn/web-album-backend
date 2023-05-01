from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class OnlineUsersViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def count(self, request):
        online_users = 0
        for i in range(10):  # 假设最大有10人在线
            if (
                async_to_sync(get_channel_layer().group_discard)(
                    "online_users", "test_channel_" + str(i)
                )
                == 1
            ):
                online_users += 1

        return Response({"online_users": online_users})
