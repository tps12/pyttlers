from json import loads
import logging
from re import compile

from base import Base
from user import User

from ..data.user import createuser
from ..formats.userjson import mediatype, tojson

class Users(Base):
    pattern = compile('^/users/$')

    url = '/users/'

    def __init__(self, db):
        self._db = db
        self.found = True

    def create(self, env, rin, wout):
        logging.info('Creating user')
        emailaddress = rin(env)
        success, data = createuser(self._db, emailaddress)
        if success:
            uuid, emailaddress = data
            url = User.geturl(uuid)
            return True, url, wout(url, emailaddress)
        else:
            return False, None, data

    @staticmethod
    def fromjson(env):
        return loads(env['wsgi.input'].read(int(env['CONTENT_LENGTH'])))['email_address']

Users.methods = {
    'POST': ({ 'application/vnd.tps12.pyttlers-new_user+v1.json': Users.fromjson }, Users.create, { mediatype: tojson }),
}
