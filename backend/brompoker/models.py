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
    creation_timestamp = models.DateTimeField(null=False)
    name = models.CharField(null=False, blank=False, max_length=128)
    non_members_allowed = models.BooleanField(null=False, default=False)
    anonymous_users_allowed = models.BooleanField(null=False, default=False)


class ClubMembership(models.Model):
    creation_timestamp = models.DateTimeField(null=False)
    user = models.ForeignKey(User, null=False)
    club = models.ForeignKey(Club, null=False)
    admin = models.BooleanField(null=False, default=False)


class Game(models.Model):
    creation_timestamp = models.DateTimeField(null=False)
    name = models.CharField(null=False, blank=False, max_length=128)
    club = models.Foreignkey(Club, null=False)
    config = models.JSONField(null=False, blank=False)
    state = models.JSONField(null=False, blank=False)


class GameEvent(models.Model):
    timestamp = models.DateTimeField(null=False)
    game = models.ForeignKey(Game, null=False)
    type = models.CharField(null=False, blank=False, max_length=64)
    content = models.JSONField(null=False, blank=False)


