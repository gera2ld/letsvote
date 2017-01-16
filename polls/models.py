from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .settings import DB_ENGINE, PYTHON_ENV

__all__ = [
    'session',
    'Question', 'Choice', 'UserQuestion', 'UserChoice',
]

def init():
    Base.metadata.create_all(engine)

engine = create_engine(DB_ENGINE or 'sqlite:///:memory:', echo=PYTHON_ENV != 'production')
Base = declarative_base()

if not DB_ENGINE: init()

Session = sessionmaker(bind=engine)
session = Session()

def json_transformer(default_fields):
    def as_json(model, extra_fields=()):
        result = {}
        for fields in default_fields, extra_fields:
            for field in fields:
                result[field] = getattr(model, field)
        return result
    return as_json

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    desc = Column(Text)
    owner_id = Column(String(64))
    user_number = Column(Integer, default=0)
    votes_lb = Column(Integer, default=1)
    votes_ub = Column(Integer, default=1)

    def __str__(self):
        return self.title

    as_json = json_transformer([
        'id', 'title', 'desc', 'user_number',
    ])

class Choice(Base):
    __tablename__ = 'choice'
    id = Column(Integer, primary_key=True)
    question_id = Column(ForeignKey('question.id', ondelete='CASCADE'))
    title = Column(String(200))
    desc = Column(Text)
    votes = Column(Integer, default=0)

    def __str__(self):
        return self.title

    as_json = json_transformer([
        'id', 'title', 'desc', 'votes',
    ])

class UserQuestion(Base):
    __tablename__ = 'userquestion'
    id = Column(Integer, primary_key=True)
    question_id = Column(ForeignKey('question.id', ondelete='CASCADE'))
    user_id = Column(String(64))

    def __str__(self):
        return self.user_id + '@' + self.question.title

class UserChoice(Base):
    __tablename__ = 'userchoice'
    id = Column(Integer, primary_key=True)
    userquestion_id = Column(ForeignKey('userquestion.id', ondelete='CASCADE'))
    choice_id = Column(ForeignKey('choice.id', ondelete='CASCADE'))

    def __str__(self):
        return self.userquestion.user_id + '@' + self.choice.title

Choice.question = relationship('Question', backref='choices')
UserQuestion.question = relationship('Question', backref='userquestions')
UserQuestion.userchoices = relationship('UserChoice')
UserChoice.userquestion = relationship('UserQuestion')
UserChoice.choice = relationship('Choice')
