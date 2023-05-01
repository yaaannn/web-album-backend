from channels.generic.websocket import WebsocketConsumer

# 导入async_to_sync
from asgiref.sync import async_to_sync
import json


class OnlineUsersConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("online_users", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "online_users", self.channel_name
        )

    def online_users(self, event):
        self.send(text_data=json.dumps({"online_users": event["online_users"]}))
