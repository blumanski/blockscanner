#!/usr/bin/python3
import sys,binascii
from bitcoinrpc.authproxy import *
from bitcoin import *

rpc_user = 'username'
rpc_password = 'password'
port=43123
start = 207568
prefix = 'CHNC'

con = AuthServiceProxy("http://%s:%s@127.0.0.1:%i"%(rpc_user, rpc_password,port))

height = con.getblockcount()
curr = con.getblock(con.getblockhash(start))
opreturns = []

#getting all opreturns
for i in range(start,height+1):
    curr = con.getblock(con.getblockhash(i))
    for f in curr['tx']:
        tx = con.getrawtransaction(f)
        deser = deserialize(tx)
        for out in deser['outs']:
            if out['script'][:2] == '6a':
                opreturns.append(out['script'])

#removing opreturn initial codes
for i in range(len(opreturns)):
    opreturns[i] = opreturns[i].replace(opreturns[i][:6],'')

#converting hex to ascii
for i in range(len(opreturns)):
    try:
        opreturns[i] = binascii.unhexlify(opreturns[i]).decode('utf-8')
    except:
        continue

#testing for prefix
l = True
while l:
    l = False
    for i in range(len(opreturns)):
        if not prefix in opreturns[i]:
            l = True
            del opreturns[i]
            break
        else:
            opreturns[i] = opreturns[i].replace(prefix,'')
            print(opreturns[i])
