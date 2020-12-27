from django.urls import re_path
from brompoker import consumers


websocket_urlpatterns = [
    re_path(r'ws/clublist/$', consumers.ClubListConsumer.as_asgi()),
    re_path(r'ws/gamelist/(?P<club_id>\d+)/$', consumers.GameListConsumer.as_asgi()),
    re_path(r'ws/sessionlist/(?P<club_id>\d+)/$', consumers.SessionListConsumer.as_asgi()),
    re_path(r'ws/game/(?P<game_id>\d+)/$', consumers.GameConsumer.as_asgi()),
]