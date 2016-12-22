from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.db.models import F
from django.http import HttpResponseBadRequest
from .models import Question, UserQuestion, UserChoice
from .forms import PollForm

def detail(request, poll_id):
    poll = get_object_or_404(Question, id=poll_id)
    choices = poll.choice_set.all()
    userquestion = poll.userquestion_set.first()
    if request.method == 'GET':
        if userquestion:
            userchoices = userquestion.userchoice_set.select_related('choice')
            selected = set(userchoice.choice for userchoice in userchoices)
        else:
            selected = set()
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'choices': choices,
            'voted': userquestion is not None,
            'total': sum(choice.votes for choice in choices),
            'selected': selected,
            'LOGIN': settings.LOGIN,
            'user': request.user if request.user.is_authenticated() else None,
            'request': request,
            'redirect_uri': request.build_absolute_uri('/account/callback?next=' + request.path),
        })
    elif request.method == 'POST':
        form = PollForm(choices, request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()
        if userquestion is None:
            user_choices = form.cleaned_data['poll_values']
            userquestion = poll.userquestion_set.create(user=request.user)
            userquestion.userchoice_set.bulk_create([
                UserChoice(userquestion=userquestion, choice=choice)
                for choice in user_choices
            ])
            user_choices.update(votes=F('votes')+1)
            Question.objects.filter(id=poll_id).update(user_number=F('user_number')+1)
        return redirect(request.path)
