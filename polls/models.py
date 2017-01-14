from django.db import models

def json_transformer(default_fields):
    def as_json(model, extra_fields=()):
        result = {}
        for fields in default_fields, extra_fields:
            for field in fields:
                result[field] = getattr(model, field)
        return result
    return as_json

class Question(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True)
    owner_id = models.CharField(max_length=64)
    user_number = models.IntegerField(default=0)
    votes_lb = models.IntegerField(default=1)
    votes_ub = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    as_json = json_transformer([
        'id', 'title', 'desc', 'user_number',
    ])

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    as_json = json_transformer([
        'id', 'title', 'desc', 'votes',
    ])

class UserQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=64)

    def __str__(self):
        return self.user.userinfo.nickname + '@' + self.question.title

class UserChoice(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    userquestion = models.ForeignKey(UserQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.userquestion.user.userinfo.nickname + '@' + self.choice.title
