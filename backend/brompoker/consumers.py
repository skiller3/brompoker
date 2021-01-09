from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .locking import create_lock, async_acquire, async_release
from django.forms.models import model_to_dict
from . import models
import logging
import json


class ClubListConsumer(AsyncWebsocketConsumer):

    _logger = logging.getLogger('brompoker.ClubListConsumer')

    async def connect(self):
        self._logger.debug(f"connect() called. Channel name: {self.channel_name}. User: {self.scope['user']}")

        await self.channel_layer.group_add('clublist', self.channel_name)
        await self.accept()

        lock = create_lock("clublist") 
        await async_acquire(lock)
        self._logger.debug("Acquired clublist lock")
        clubs = await sync_to_async(self._get_clubs)()
        await self.send(text_data=json.dumps({
            "type": "CREATE_CLUBS",
            "data": clubs
        }))
        await async_release(lock)
        self._logger.debug("Released clublist lock")

    async def disconnect(self, close_code):
        self._logger.debug(f"disconnect() called with close code {close_code}. User: {self.scope['user']}")
        await self.channel_layer.group_discard('clublist', self.channel_name)

    async def receive(self, text_data):
        self._logger.debug(f"receive() called with text data {text_data}. User: {self.scope['user']}")

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
        return [model_to_dict(club) for club in clubs]


class GameListConsumer(AsyncWebsocketConsumer):
    _logger = logging.getLogger('brompoker.GameListConsumer')

    async def connect(self):
        self._logger.debug(f"connect() called. Channel name: {self.channel_name}. User: {self.scope['user']}")
        
        club_id = int(self.scope['url_route']['kwargs']['club_id'])
        self._logger.debug(f"Club ID: {club_id}")

        permitted = await sync_to_async(self._has_club_access)(club_id)
        if not permitted:
            self._logger.warning(f'User {self.scope["user"]} attempted to view games '
                                 f'in club {club_id}, but access was denied')
            await self.close()
            return

        await self.channel_layer.group_add(f'gamelist-{club_id}', self.channel_name)
        await self.accept()

        lock = create_lock(self.channel_name) 
        await async_acquire(lock)
        self._logger.debug("Acquired gamelist lock")
        games = await sync_to_async(self._get_games)(club_id)
        await self.send(text_data=json.dumps({
            "type": "CREATE_GAMES",
            "data": games
        }))
        await async_release(lock)
        self._logger.debug("Released gamelist lock")

    async def disconnect(self, close_code):
        self._logger.debug(f"disconnect() called with close code {close_code}. User: {self.scope['user']}")
        club_id = int(self.scope['url_route']['kwargs']['club_id'])
        await self.channel_layer.group_discard(f'gamelist-{club_id}', self.channel_name)

    async def receive(self, text_data):
        self._logger.debug(f"receive() called with text data {text_data}. User: {self.scope['user']}")

    async def handle_gamelist_update(self, notification):
        self._logger.debug(f'handle_gamelist_update() called. Notification: {notification}')
        lock = create_lock(self.channel_name)
        await async_acquire(lock)
        await self.send(text_data=json.dumps(notification["event"]))
        await async_release(lock)

    def _has_club_access(self, club_id):
        user = self.scope["user"]
        club = models.Club.objects.get(id=club_id)
        if user.is_authenticated:
            if club.allow_non_members:
                return True
            if models.ClubMembership.objects.exists(club=club, user=user):
                return True
        else:
            if club.allow_non_members and club.allow_anonymous_users:
                return True
        return False

    def _get_games(self, club_id):
        games = models.Game.objects.filter(club_id=club_id)
        return [model_to_dict(game) for game in games]


class SessionListConsumer(AsyncWebsocketConsumer):
    _logger = logging.getLogger('brompoker.GameListConsumer')

    async def connect(self):
        self._logger.debug(f"connect() called. Channel name: {self.channel_name}. User: {self.scope['user']}")
        await self.accept()

    async def disconnect(self, close_code):
        self._logger.debug(f"disconnect() called with close code {close_code}. User: {self.scope['user']}")

    async def receive(self, text_data):
        self._logger.debug(f"receive() called with text data {text_data}. User: {self.scope['user']}")


class GameConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        pass

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass
