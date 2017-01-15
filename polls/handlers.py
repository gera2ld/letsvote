import json
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat
from .utils import require_token, pick_keys
from .models import *

handlers = []
def handler(path):
    def decorator(handler):
        handlers.append((path, handler))
        return handler
    return decorator

@handler('/authorize')
class AuthorizeHandler(RequestHandler):
    async def get(self):
        ticket = self.get_argument('ticket')
        if not ticket:
            self.set_status(400)
            self.write({
                'errors': {
                    'ticket': 'Invalid ticket',
                },
            })
            return
        url = url_concat(
            self.application.settings['ARBITER_URL'] + '/api/token',
            {'ticket': ticket}
        )
        client = AsyncHTTPClient()
        response = await client.fetch(url)
        data = json.loads(response.body)
        self.set_status(response.code)
        self.write(data)

@handler('/me')
class UserHandler(RequestHandler):
    @require_token()
    def get(self):
        self.write(self.user)

@handler('/my/polls')
class MyPollsHandler(RequestHandler):
    @require_token()
    def get(self):
        # TODO pagination
        fields = [
            'id',
            'title',
            'desc',
            'user_number',
        ]
        session = Session()
        items = session.query(Question).filter_by(
            owner_id=self.user['uid'],
        )
        questions = [
            dict((field, getattr(item, field)) for field in fields)
            for item in items
        ]
        self.write({
            'data': questions,
        })

@handler('/polls/(\w+)')
class DetailHandler(RequestHandler):
    @require_token(allow_anonymous=True)
    def get(self, poll_id):
        session = Session()
        question = session.query(Question).filter_by(
            id=poll_id,
        ).one()
        choices = question.choices
        uid = self.user.get('uid')
        userquestion = uid and session.query(UserQuestion).filter_by(
            question_id=poll_id,
            user_id=uid,
        ).one_or_none()
        if userquestion:
            userchoices = userquestion.userchoices
            selected = [userchoice.choice.id for userchoice in userchoices]
        else:
            selected = None
        question_data = question.as_json(('votes_lb', 'votes_ub'))
        question_data['choices'] = [c.as_json() for c in choices]
        question_data['selected'] = selected
        self.write({
            'data': question_data,
        })

    @require_token()
    def post(self, poll_id):
        session = Session()
        question = session.query(Question).filter_by(
            id=poll_id,
        ).one()
        uid = self.user.get('uid')
        userquestion = uid and session.query(UserQuestion).filter_by(
            question_id=poll_id,
            user_id=uid,
        ).one_or_none()
        if userquestion is not None:
            self.set_status(422)
            self.write({
                'errors': {
                    'question': 'Already voted',
                },
            })
            return
        data = json.loads(self.request.body)
        poll_values = set(data['poll_values'])
        selected = [choice for choice in question.choices if choice.id in poll_values]
        userquestion = UserQuestion(user_id=uid, question_id=poll_id)
        userquestion.userchoices = [
            UserChoice(choice=choice) for choice in selected
        ]
        session.query(Choice).filter(
            Choice.id.in_(choice.id for choice in selected),
        ).update({Choice.votes: Choice.votes + 1}, synchronize_session=False)
        question.user_number = Question.user_number + 1
        session.add(userquestion)
        session.commit()
        question_data = question.as_json()
        question_data['choices'] = [c.as_json() for c in question.choices]
        question_data['selected'] = [choice.id for choice in selected]
        self.set_status(201)
        self.write({
            'data': question_data,
        })

@handler('/polls')
class CreateHandler(RequestHandler):
    @require_token()
    def post(self):
        session = Session()
        data = json.loads(self.request.body)
        data_question = pick_keys(data['question'], ('title', 'desc', 'votes_lb', 'votes_ub'))
        data_choices = [pick_keys(choice, ('title', 'desc')) for choice in data['choices']]
        data_question['owner_id'] = self.user['uid']
        question = Question(**data_question)
        question.choices = [Choice(**data_choice) for data_choice in data_choices]
        session.add(question)
        session.commit()
        question_data = question.as_json()
        question_data['choices'] = [c.as_json() for c in question.choices]
        self.set_status(201)
        self.write({
            'data': question_data,
        })
