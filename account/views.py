from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import UserInfo
import requests

GITHUB = settings.LOGIN['GITHUB']
json_headers = {
    'Accept': 'application/json',
}

def callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponseBadRequest('Invalid code')
    payload = {
        'client_id': GITHUB['CLIENT_ID'],
        'client_secret': GITHUB['CLIENT_SECRET'],
        'code': code,
    }
    res = requests.post('https://github.com/login/oauth/access_token', json=payload, headers=json_headers)
    data = res.json()
    if data.get('error'):
        return HttpResponseBadRequest('Invalid code')
    access_token = data['access_token']
    params = {
        'access_token': access_token,
    }
    res = requests.get('https://api.github.com/user', params=params)
    data = res.json()
    open_id = 'github/'+str(data['id'])
    user, created = User.objects.update_or_create(
        userinfo__open_id=open_id,
        username=open_id)
    defaults = {
        'open_id': open_id,
        'avatar_url': data['avatar_url'],
        'gravatar_id': data['gravatar_id'],
        'nickname': data['name'],
        'token': access_token,
    }
    UserInfo.objects.update_or_create(user=user, defaults=defaults)
    login(request, user)
    return redirect(request.GET.get('next') or '/')

def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next') or '/')