from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True)
    created_by = models.ForeignKey(User)
    user_number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.userinfo.nickname + '@' + self.question.title

class UserChoice(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    userquestion = models.ForeignKey(UserQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.userquestion.user.userinfo.nickname + '@' + self.choice.title
