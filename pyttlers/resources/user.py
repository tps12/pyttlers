import logging
from re import compile

from base import Base

from ..data.user import deleteuser, selectuser
from ..formats.userjson import mediatype, tojson

class User(Base):
    pattern = compile('^/users/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$')

    @property
    def url(self):
        return self.geturl(self._uuid)

    @staticmethod
    def geturl(uuid):
        return '/users/{0}/'.format(uuid) if uuid else None
    
    def __init__(self, db, uuid):
        self._db = db
        logging.info('Finding user')
        user = selectuser(self._db, uuid)
        if user:
            self._uuid = uuid
            self._emailaddress = user[0]
            self.found = True
        else:
            self.found = False

    def retrieve(self, env, rin, wout):
        logging.info('Retrieving user')
        return True, None, wout(self.url, self._emailaddress)

    def destroy(self, env, rin, wout):
        deleteuser(self._db, self._uuid)
        self._uuid = None
        return True, None, wout(self.url, self._emailaddress)

User.methods = {
    'GET': ({}, User.retrieve, { mediatype: tojson }),
    'DELETE': ({}, User.destroy, { mediatype : tojson })
}
