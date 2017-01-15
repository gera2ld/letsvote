import os

environ = dict(os.environ)
try:
    from . import env
    for key in dir(env):
        if not key.startswith('_') and key.upper() == key:
            environ[key] = getattr(env, key)
except ImportError:
    pass

def as_dict():
    kw = {
        'cookie_secret': SECRET_KEY,
    }
    for key, value in globals().items():
        if not key.startswith('_') and key.upper() == key:
            kw[key] = value
    return kw

SECRET_KEY = environ['SECRET_KEY']
ARBITER_URL = environ['ARBITER_URL']
DB_ENGINE = environ.get('DB_ENGINE', 'sqlite:///:memory:')

UNIX_SOCKET = environ.get('UNIX_SOCKET')
PORT = environ.get('PORT', 3000)
