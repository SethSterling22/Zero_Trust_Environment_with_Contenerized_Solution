from zoodb import *
from debug import *

import hashlib
import secrets
import pbkdf2


def newtoken(db, person):
    hashinput = "%s.%s" % (secrets.token_bytes(16), person.password)
    person.token = hashlib.sha256(hashinput.encode('utf-8')).hexdigest()
    db.commit()
    return person.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if cred.password == pbkdf2.PBKDF2(password, cred.salt).hexread(32):
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    cdb = cred_setup()
    person = cdb.query(Cred).get(username)
    if person:
        return None
    newcred = Cred()
    newcred.username = username
    newcred.salt = os.urandom(32)
    newcred.password = pbkdf2.PBKDF2(password, newcred.salt).hexread(32)
    cdb.add(newcred)
    cdb.commit()
    return newtoken(cdb, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False
