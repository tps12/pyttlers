import logging
from uuid import uuid1

def createuser(db, emailaddress):
    c = db.users.cursor()
    uuid = str(uuid1())

    try:
        c.execute('INSERT INTO users (uuid, email_address, created_at, updated_at)' +
                  'VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',
                  (uuid, emailaddress))
    except Exception as ex:
        logging.error(str(ex))
        db.users.rollback()
        return False, 'Email address already taken'
    finally:
        c.close()

    db.users.commit()
    return True, (uuid, emailaddress)

def deleteuser(db, uuid):
    c = db.users.cursor()
    c.execute('DELETE FROM users WHERE uuid = %s', (uuid,))
    c.close()
    db.users.commit()
    return True

def selectuser(db, uuid):
    c = db.users.cursor()
    c.execute('SELECT email_address FROM users WHERE uuid = %s', (uuid,))
    us = c.fetchall()
    c.close()
    return us[0] if len(us) > 0 else None
