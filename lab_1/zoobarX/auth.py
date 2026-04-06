from zoodb import *
from debug import *
from flask import g, render_template, request
import rpclib

import hashlib
import secrets

sys.path.append(os.getcwd())
import readconf

def newtoken(db, person):
    hashinput = "%s.%s" % (secrets.token_bytes(16), person.password)
    person.token = hashlib.sha256(hashinput.encode('utf-8')).hexdigest()
    db.commit()
    return person.token

@catch_err
def login(username, password):
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        ret = c.call('login', username=request.args.get('username', ''), password=request.args.get('password', ''))
    return ret

#def login(username, password):
    #db = person_setup()
   # person = db.query(Person).get(username)
  #  if not person:
 #       return None
 #   if person.password == password:
 #       return newtoken(db, person)
  #  else:
 #       return None
@catch_err
def register(username, password):
    db = person_setup()
    person = db.query(Person).get(username)
    if person:
        return None
    newperson = Person()
    newperson.username = username
 #   newperson.password = password
    db.add(newperson)
    db.commit()
    with rpclib.client_connect(host) as c:
        ret = c.call('register', username=request.args.get('username', ''), password=request.args.get('password', ''))
    return ret
#    return newtoken(db, newperson)

@catch_err
def check_token(username, token):
    host = readconf.read_conf().lookup_host('auth')
    with rpclib.client_connect(host) as c:
        ret = c.call('check_token', username=request.args.get('username', ''), token=request.args.get('token', ''))
    return ret
