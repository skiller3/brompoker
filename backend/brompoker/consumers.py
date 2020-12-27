from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .locking import create_lock, async_acquire, async_release
from . import models
import logging
import json


class ClubListConsumer(AsyncWebsocketConsumer):

    _logger = logging.getLogger('brompoker.ClubListConsumer')

    async def connect(self):
        self._logger.debug(f"connect() called. Channel name: {self.channel_name}. User: {self.scope['user']}")
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name """

        # Join room group
        await self.channel_layer.group_add('clublist', self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        self._logger.debug(f"disconnect() called with close code {close_code}. User: {self.scope['user']}")
        await self.channel_layer.group_discard('clublist', self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        event = json.loads(text_data, encoding="utf-8")
        if event.get("type") != "READY":
            return
        lock = create_lock("clublist") 
        await async_acquire(lock)
        self._logger.debug("Acquired clublist lock")
        clubs = await sync_to_async(self._get_clubs)()
        await self.send(text_data=json.dumps({
            "clubs": clubs,
            "games": [],
            "sessions": []
        }))
        await async_release(lock)
        self._logger.debug("Released clublist lock")


    # Receive message from room group
    async def handle_clublist_update(self, notification):
        self._logger.debug(f'handle_clublist_update() called. Notification: {notification}')
        lock = create_lock("clublist")
        await async_acquire(lock)
        await self.send(text_data=json.dumps(notification["event"]))
        await async_release(lock)

    def _get_clubs(self):
        user = self.scope["user"]
        if user.is_authenticated:
            clubs = models.Club.objects.filter(allow_non_members=True)
            clubs = clubs | models.Club.objects.filter(clubmembership__user=user)
        else:
            clubs = models.Club.objects.filter(allow_non_members=True, allow_anonymous_users=True)
        return [club.name for club in clubs]


class GameListConsumer(AsyncWebsocketConsumer):
    pass


class SessionListConsumer(AsyncWebsocketConsumer):
    pass


class GameConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        pass

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass
