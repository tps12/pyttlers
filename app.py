import logging
from os import environ
from sys import stdout
from urlparse import urlparse as parse

import psycopg2

from pyttlers.resources.user import User
from pyttlers.resources.users import Users

resources = [Users, User]

# configure logging
try:
    lvl = logging.__dict__[environ['LOG_LEVEL']]
except KeyError:
    lvl = logging.DEBUG
logging.getLogger().setLevel(lvl)

class Databases(object):
    def __init__(self, users_url):
        url = parse(users_url)
        if url.scheme == 'postgres':
            self.users = psycopg2.connect(dbname=url.path[1:], user=url.username, password=url.password, host=url.hostname)
        else:
            raise ValueError
db = Databases(environ['DATABASE_URL'])

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
