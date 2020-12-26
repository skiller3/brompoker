# Copyright 2020 Skye Isard
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    name = models.CharField(null=False, blank=False, max_length=128, unique=True)
    allow_non_members = models.BooleanField(null=False, default=False)
    allow_anonymous_users = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Club: {self}>'


class ClubMembership(models.Model):
    class Meta():
        unique_together = ('user', 'club')
        verbose_name = 'Club Membership'
        verbose_name_plural = 'Club Memberships'

    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, null=False, on_delete=models.CASCADE)
    admin = models.BooleanField(null=False, default=False)
    allow_play_games = models.BooleanField(null=False, default=False)
    allow_manage_games = models.BooleanField(null=False, default=False)
    allow_create_games = models.BooleanField(null=False, default=False)
    # allow_modify_games = models.BooleanField(null=False, default=False)
    # allow_delete_games = models.BooleanField(null=False, default=False)
    allow_invite_members = models.BooleanField(null=False, default=False)
    # allow_expel_members = models.BooleanField(null=False, default=False)
    # allow_modify_member_permissions = models.BooleanField(null=False, default=False)
    # allow_modify_club = models.BooleanField(null=False, default=False)
    # allow_delete_club = models.BooleanField(null=False, default=False)


class Game(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    name = models.CharField(null=False, blank=False, max_length=128, unique=True)
    club = models.ForeignKey(Club, null=False, on_delete=models.CASCADE)
    config = models.JSONField(null=False, blank=False)
    state = models.JSONField(null=False, blank=False)


class GameEvent(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    game_id = models.IntegerField(null=False)
    game_name = models.CharField(null=False, blank=False, max_length=128)

    # NOTE:
    # The value -1 will represent the game engine (i.e the house/dealer itself)
    # The value 0 will represent all users observing the game
    emitter_user_id = models.IntegerField(null=False)

    # NOTE: Next field character length matches django.contrib.auth.models.User
    # username field length
    emitter_user_username = models.CharField(null=False, blank=False, max_length=150)

    # NOTE:
    # The value -1 will represent the game engine (i.e the house/dealer itself)
    # The value 0 will represent all users observing the game
    recipient_user_id = models.IntegerField(null=False)

    # NOTE: Next field character length matches django.contrib.auth.models.User
    # username field length
    recipient_user_username = models.CharField(null=False, blank=False, max_length=150)

    type = models.CharField(null=False, blank=False, max_length=64)
    content = models.JSONField(null=False, blank=False)


