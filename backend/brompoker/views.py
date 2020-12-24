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

from django.contrib.auth import authenticate as auth, login as django_login, logout as django_logout
from django.http.response import HttpResponse, JsonResponse
import json


def _authprotect(view_fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_fn(request, *args, **kwargs)
        return HttpResponse("User is not authenticated!", status=401)
    return wrapper

def is_authenticated(request):
    return JsonResponse({'authenticated': request.user.is_authenticated}, status=200)

def authenticate(request):
    request_payload = json.loads(request.body, encoding="utf-8")
    username = request_payload['username']
    password = request_payload['password']
    user = auth(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return HttpResponse('Authentication succeeded!', status=200)
    return HttpResponse('Authentication failed!', status=401)

@_authprotect
def logout(request):
    django_logout(request)
    return HttpResponse('Logout succeeded!', status=200)

@_authprotect
def change_password(request):
    request_payload = json.loads(request.body, encoding="utf-8")
    old_password = request_payload['old_password']
    new_password = request_payload['new_password']
    user = auth(request, username=request.user.username, password=old_password)
    if not user:
        return HttpResponse("Old password is invalid", status=401)
    user.password = new_password
    user.save()
    return HttpResponse("Password change succeeded!", status=200)

