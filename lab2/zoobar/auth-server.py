#!/usr/bin/env python3

import rpcsrv
import sys
import otroauth as auth
from debug import *

class AuthRpcServer(rpcsrv.RpcServer):
    ## Fill in RPC methods here.
    def rpc_register(self, username, password):
        return auth.register(username, password)
    def rpc_check_token(self, username, token):
        return auth.check_token(username, token)
    def rpc_login(self, username, password):
        return auth.login(username, password)

if len(sys.argv) != 2:
    print(sys.argv[0], "too few args")

s = AuthRpcServer()
s.run_fork(sys.argv[1])
