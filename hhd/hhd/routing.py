from django.urls import path
from msg_app.consumers import GuestChatConsumer, StuffChatConsumer

websocket_urlpatterns = [
    path('chat/<str:room_name>/', GuestChatConsumer.as_asgi()),
    path('stuff/<str:chat_token>/', StuffChatConsumer.as_asgi()),
]