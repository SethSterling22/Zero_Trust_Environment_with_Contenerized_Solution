from zoodb import *
from debug import *

import hashlib
import secrets

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
    if cred.password == password:
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    pdb = person_setup()
    cdb = cred_setup()
    person = pdb.query(Person).get(username)
    if person:
        return None
    newperson = Person()
    newcred = Cred()
    newperson.username = username
    newcred.username = username
    newcred.password = password
    pdb.add(newperson)
    cdb.add(newcred)
    pdb.commit()
    cdb.commit()
    return newtoken(cdb, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = cdb.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return
