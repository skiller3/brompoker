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

from django.apps import AppConfig
from django.db.models import signals
from channels.layers import get_channel_layer
from django.forms.models import model_to_dict
from asgiref.sync import async_to_sync
import logging


class BrompokerAppConfig(AppConfig):
    name = 'brompoker'

    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(f'brompoker.{self.__class__.__name__}')
        super().__init__(*args, **kwargs)

    def _notify_clublist_consumers(self, sender, **kwargs):
        self._logger.debug(f"_notify_clublist_consumers() called. Kwargs: {kwargs}")
        event_type = "CREATE_CLUBS" if kwargs["created"] else "UPDATE_CLUBS"
        event_data = model_to_dict(kwargs["instance"])
        event = {"type": event_type, "data": event_data}
        notification = {"type": "handle_clublist_update", "event": event}
        async_to_sync(get_channel_layer().group_send)('clublist', notification)

    def ready(self):
        self._logger.debug("ready() called")

        from . import models

        signals.post_save.connect(self._notify_clublist_consumers, sender=models.Club)
        self._logger.debug("Connected clublist post_save handler")