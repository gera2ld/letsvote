import json
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import requests
from .models import Question, Choice, UserChoice
from .forms import PollForm, ChoiceForm, AnswerForm
from .utils import require_token, drop_empty

@require_GET
def authorize(request):
    ticket = request.GET.get('ticket')
    if not ticket:
        return JsonResponse({
            'errors': {
                'ticket': 'Invalid ticket',
            },
        }, status=400)
    url = settings.ARBITER_URL + '/api/token'
    r = requests.get(url, params={'ticket': ticket})
    return JsonResponse(r.json(), status=r.status_code)

@require_GET
@require_token()
def me(request):
    return JsonResponse(request.user_data)

@require_GET
@require_token()
def my_polls(request):
    # TODO pagination
    fields = [
        'id',
        'title',
        'desc',
        'user_number',
    ]
    questions = [
        dict(zip(fields, data))
        for data in Question.objects.filter(
            owner_id=request.user_data['uid'],
        ).values_list(*fields)
    ]
    return JsonResponse({
        'data': questions,
    })

@require_GET
@require_token(allow_anonymous=True)
def get_detail(request, poll_id):
    question = get_object_or_404(Question, id=poll_id)
    choices = question.choice_set.all()
    uid = request.user_data.get('uid')
    userquestion = uid and question.userquestion_set.filter(user_id=uid).first()
    if userquestion:
        userchoices = userquestion.userchoice_set.select_related('choice')
        selected = [userchoice.choice.id for userchoice in userchoices]
    else:
        selected = None
    question_data = question.as_json(('votes_lb', 'votes_ub'))
    question_data['choices'] = [c.as_json() for c in choices]
    question_data['selected'] = selected
    return JsonResponse({
        'data': question_data,
    })

@require_POST
@require_token()
def create_poll(request):
    POST = json.loads(request.body.decode())
    choices = POST.pop('choices')
    choices_forms = []
    for choice in choices:
        form = ChoiceForm(choice)
        if not form.is_valid():
            return JsonResponse({
                'errors': form.errors,
            }, status=422)
        choices_forms.append(form)
    form = PollForm(POST.get('question'))
    if not form.is_valid():
        return JsonResponse({
            'errors': form.errors,
        }, status=422)
    question_data = drop_empty(form.cleaned_data)
    question_data['owner_id'] = request.user_data['uid']
    question = Question.objects.create(**question_data)
    question.choice_set.bulk_create([
        Choice(question=question, **drop_empty(form.cleaned_data))
        for form in choices_forms
    ])
    question_data = question.as_json()
    question_data['choices'] = [c.as_json() for c in question.choice_set.all()]
    return JsonResponse({
        'data': question_data,
    }, status=201)

@require_POST
@require_token()
def make_poll(request, poll_id):
    question = get_object_or_404(Question, id=poll_id)
    choices = question.choice_set.all()
    uid = request.user_data.get('uid')
    userquestion = uid and question.userquestion_set.filter(user_id=uid).first()
    if userquestion is not None:
        return JsonResponse({
            'errors': {
                'question': 'Already voted',
            },
        }, status=422)
    POST = json.loads(request.body.decode())
    form = AnswerForm(question, POST)
    if not form.is_valid():
        return JsonResponse({
            'errors': form.errors,
        }, status=422)
    user_choices = form.cleaned_data['poll_values']
    userquestion = question.userquestion_set.create(user_id=uid)
    userquestion.userchoice_set.bulk_create([
        UserChoice(userquestion=userquestion, choice=choice)
        for choice in user_choices
    ])
    user_choices.update(votes=F('votes')+1)
    user_number = question.user_number + 1
    question.user_number = F('user_number') + 1
    question.save()
    question_data = question.as_json()
    question_data['user_number'] = user_number
    question_data['choices'] = [c.as_json() for c in choices]
    question_data['selected'] = [choice.id for choice in user_choices]
    return JsonResponse({
        'data': question_data,
    }, status=201)
