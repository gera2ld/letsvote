from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from django.core.cache import cache
import requests

def cache_result(get_cache_key, timeout=30):
    def wrapper(handle):
        @wraps(handle)
        def wrapped(*k, **kw):
            cache_key = get_cache_key(*k, **kw)
            result = cache.get(cache_key)
            if result is None:
                result = handle(*k, **kw)
                if result is not None:
                    cache.set(cache_key, result, timeout)
            return result
        return wrapped
    return wrapper

@cache_result(lambda a: a.replace(' ', ':'))
def load_user_from_token(authorization):
    url = settings.ARBITER_URL + '/api/user'
    headers = {
        'Authorization': authorization,
    }
    r = requests.get(url, headers=headers)
    if 100 < r.status_code < 300:
        return r.json()

def require_token(allow_anonymous=False):
    def wrapper(handle):
        @wraps(handle)
        def wrapped(request, *k, **kw):
            authorization = request.META.get('HTTP_AUTHORIZATION')
            user = None
            if authorization:
                try:
                    user = load_user_from_token(authorization)
                except Exception as exc:
                    return JsonResponse({
                        'error': repr(exc),
                    }, status=500)
            if user is None and not allow_anonymous:
                return JsonResponse({
                    'error': 'Invalid token',
                }, status=401)
            request.user_data = user or {}
            return handle(request, *k, **kw)
        return wrapped
    return wrapper
