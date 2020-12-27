from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from asgiref.sync import sync_to_async
import filelock


def create_lock(id):
    if not isinstance(settings.LOCKING_BACKEND, str):
        raise ImproperlyConfigured("Unrecognized Django LOCKING_BACKEND value")
    if settings.LOCKING_BACKEND.upper() == "FILE":
        return filelock.FileLock(f"{id}.lock")
    raise ImproperlyConfigured("Unrecognized Django LOCKING_BACKEND value")

async def async_acquire(lock):
    await sync_to_async(lock.acquire)()

async def async_release(lock):
    await sync_to_async(lock.release)()
