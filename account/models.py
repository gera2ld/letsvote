from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    open_id = models.CharField(max_length=255)
    avatar_url = models.TextField()
    gravatar_id = models.TextField()
    token = models.TextField()
    nickname = models.CharField(max_length=64)

    def __str__(self):
        return self.nickname + ' <' + self.open_id + '>'