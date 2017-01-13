from django.shortcuts import get_object_or_404
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import requests
from .models import Question, Choice, UserChoice
from .forms import PollForm, ChoiceForm, AnswerForm
from .utils import require_token

@require_POST
def authorize(request):
    ticket = request.POST.get('ticket')
    if not ticket:
        return JsonResponse({
            'errors': {
                'ticket': 'Invalid ticket',
            },
        }, status=400)
    url = settings.ARBITER_URL + '/api/token'
    r = requests.post(url, params={'ticket': ticket})
    return JsonResponse(r.json(), status=r.status)

@require_GET
@require_token()
def me(request):
    return JsonResponse(request.user_data)

@require_GET
@require_token(allow_anonymous=True)
def get_detail(request, poll_id):
    question = get_object_or_404(Question, id=poll_id)
    choices = question.choice_set.all()
    uid = request.user_data.get('id')
    userquestion = uid and question.userquestion_set.filter(user_id=uid).first()
    if userquestion:
        userchoices = userquestion.userchoice_set.select_related('choice')
        selected = [userchoice.choice.id for userchoice in userchoices]
    else:
        selected = None
    return JsonResponse({
        'question': question.as_json(),
        'choices': map(lambda c: c.as_json(), choices),
        'selected': selected,
    })

@require_POST
@require_token()
def create_poll(request):
    choices = request.POST.pop('choices')
    choices_forms = []
    for choice in choices:
        form = ChoiceForm(choice)
        if not form.is_valid():
            return JsonResponse({
                'errors': form.errors,
            }, status=422)
        choices_forms.append(form)
    form = PollForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'errors': form.errors,
        }, status=422)
    question = Question.objects.create(**form.cleaned_data)
    question.choice_set.bulk_create([
        Choice(question=question, **form.cleaned_data)
        for form in choices_forms
    ])
    return JsonResponse({
        'question': question.as_json(),
        'choices': map(lambda c: c.as_json(), question.choice_set.all()),
    }, status=201)

@require_POST
@require_token()
def make_poll(request, poll_id):
    question = get_object_or_404(Question, id=poll_id)
    choices = question.choice_set.all()
    uid = request.user_data.get('id')
    userquestion = uid and question.userquestion_set.filter(user_id=uid).first()
    if userquestion is not None:
        return JsonResponse({
            'errors': {
                'question': 'Already voted',
            },
        }, status=422)
    form = AnswerForm(question, request.POST)
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
    question.update(user_number=F('user_number')+1)
    return JsonResponse({
        'choices': map(lambda c: c.as_json(), choices),
        'selected': [choice.id for choice in user_choices],
    }, status=201)
