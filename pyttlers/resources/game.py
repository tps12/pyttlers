from json import dumps
import logging
from re import compile

from base import Base

from ..data.game import selectgame

class Game(Base):
    pattern = compile('^/games/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$')

    @property
    def url(self):
        return self.geturl(self._uuid)

    @staticmethod
    def geturl(uuid):
        return '/games/{0}/'.format(uuid) if uuid else None

    def __init__(self, db, uuid):
        self._db = db
        logging.info('Finding game')
        game = selectgame(self._db, uuid)
        if game:
            self._uuid = uuid
            self._data = game[u'game']
            self.found = True
        else:
            self.found = False

    def retrieve(self, env, rin, wout):
        logging.info('Retrieving game')
        return True, None, wout(self.url, self._data)

    @staticmethod
    def tojson(url, data):
        return dumps({ 'id': url, 'game': data })

Game.methods = {
    'GET': ({}, Game.retrieve, { 'application/vnd.tps12.pyttlers-game+v1.json': Game.tojson })
}
