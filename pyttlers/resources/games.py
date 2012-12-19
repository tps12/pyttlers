from json import loads
import logging
from re import compile

from base import Base
from game import Game

from ..data.game import creategame

class Games(Base):
    pattern = compile('^/games/$')

    url = '/games/'

    def __init__(self, db):
        self._db = db
        self.found = True

    def create(self, env, rin, wout):
        logging.info('Creating game')
        json = rin(env)
        success, data = creategame(self._db, json)
        if success:
            url = Game.geturl(data)
            return True, url, None
        else:
            return False, None, data

    @staticmethod
    def fromjson(env):
        return loads(env['wsgi.input'].read(int(env['CONTENT_LENGTH'])))

Games.methods = {
    'POST': ({ 'application/vnd.tps12.pyttlers-new_game+v1.json': Games.fromjson }, Games.create, {}),
}
