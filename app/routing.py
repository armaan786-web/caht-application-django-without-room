from django.urls import path
from . import consumers
websocket_urlpatterns=[
    path('ws/chat/single/<int:other_user_id>/', consumers.SingleChatConsumer.as_asgi()),
    path('ws/chat/group/<str:group_name>/', consumers.GroupChatConsumer.as_asgi()),
]