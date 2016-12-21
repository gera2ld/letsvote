from django.contrib import admin
from .models import Question, Choice, UserQuestion, UserChoice

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserQuestion)
admin.site.register(UserChoice)