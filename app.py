import logging
from os import environ
from sys import stdout
from urlparse import urlparse, urlunparse

import psycopg2
import pymongo

from pyttlers.resources.user import User
from pyttlers.resources.users import Users
from pyttlers.resources.game import Game
from pyttlers.resources.games import Games

resources = [Users, User, Game, Games]

# configure logging
try:
    lvl = logging.__dict__[environ['LOG_LEVEL']]
except KeyError:
    lvl = logging.DEBUG
logging.getLogger().setLevel(lvl)

class Databases(object):
    def __init__(self, usersurl, gamesurl):
        url = urlparse(usersurl)
        if url.scheme == 'postgres':
            self.users = psycopg2.connect(dbname=url.path[1:], user=url.username, password=url.password, host=url.hostname)
        else:
            raise ValueError
        url = urlparse(gamesurl)
        if url.scheme == 'mongodb':
            self.games = pymongo.Connection(gamesurl)[url.path[1:]]
        else:
            raise ValueError
db = Databases(environ['DATABASE_URL'], environ['MONGOHQ_URL'])

def application(env, start_response):
    env['db'] = db
    try:
        for Resource in resources:
            match = Resource.pattern.match(env['PATH_INFO'])
            if match is not None:
                resource = Resource(db, *match.groups())
                if resource.found:
                    return resource.respond(env, start_response)
        else:
            start_response('404 Not Found', [])
            return []
    except:
        from sys import exc_info
        start_response('500 Internal Server Error', [], exc_info())
        return []
