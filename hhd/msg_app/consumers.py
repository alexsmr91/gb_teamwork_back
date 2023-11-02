from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


class GuestChatConsumer(AsyncJsonWebsocketConsumer):
    room = None
    profile = None
    user = None

    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['room_name']
        self.profile, self.user = await get_user(self.room)
        if self.user is not None:
            await self.channel_layer.group_add(self.room, self.channel_name)
            await self.accept()
        else:
            await self.accept()
            await self.close(code=4000)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        if 'type' in content and content['type'] in [
            'chat_message'
        ]:
            await self.channel_layer.group_send(
                self.room,
                content
            )
        else:
            await self.send_json(content={
                'type': 'error',
                'message': 'unknown action type'
            })

    async def chat_message(self, event):
        if 'message' in event:
            await self.send_json(content={
                'type': 'new_message',
                'message': event['message'],
                'from': self.user.username
            })


class StuffChatConsumer(AsyncJsonWebsocketConsumer):
    room = 'stuff'
    profile = None
    user = None

    async def connect(self):
        token = self.scope['url_route']['kwargs']['chat_token']
        self.profile, self.user = await get_user(token)
        if self.user is not None and not self.profile.is_guest:
            await self.channel_layer.group_add(self.room, self.channel_name)
            await self.accept()
        else:
            await self.accept()
            await self.close(code=4000)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        if 'type' in content and content['type'] in [
            'chat_message'
        ]:
            await self.channel_layer.group_send(
                self.room,
                content
            )
        else:
            await self.send_json(content={
                'type': 'error',
                'message': 'unknown action type'
            })

    async def chat_message(self, event):
        if 'message' in event:
            await self.send_json(content={
                'type': 'new_message',
                'message': event['message'],
                'from': self.user.username
            })


@database_sync_to_async
def get_user(token):
    from user_app.models import Profile
    qs = Profile.objects.filter(chat_room=token)
    if len(qs) == 1:
        return qs[0], qs[0].user
    else:
        return None, None
