import logging
from uuid import uuid1, UUID

def creategame(db, game):
    uuid = uuid1()
    return True, db.games.games.insert({ '_id': uuid, 'game': game })

def selectgame(db, uuid):
    return db.games.games.find_one({ '_id': UUID(uuid) })
