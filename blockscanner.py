#!/usr/bin/python3
import sys
import binascii
import zlib
from bitcoinrpc.authproxy import *
from bitcoin import *

rpc_user = 'xxxx'
rpc_password = 'xxxxx'
port = 8332
start = 390076
end = 391076
# just testing, more prefixes will be used
prefix = {'s8': "S08k", 'n8': "08k"}

con = AuthServiceProxy("http://%s:%s@127.0.0.1:%i" %
                       (rpc_user, rpc_password, port))

height = con.getblockcount()
curr = con.getblock(con.getblockhash(start))
opreturns = []

# getting all opreturns
for i in range(start, end):
    curr = con.getblock(con.getblockhash(i))
    for f in curr['tx']:
        tx = con.getrawtransaction(f)
        deser = deserialize(tx)

        for out in deser['outs']:
            if out['script'][:2] == '6a':
                opreturns.append(out['script'])

# removing opreturn initial codes
for i in range(len(opreturns)):
    #print('opreturns -> ', opreturns)
    opreturns[i] = opreturns[i].replace(opreturns[i][:6], '')

# converting hex to ascii
for i in range(len(opreturns)):
    try:
        opreturns[i] = binascii.unhexlify(opreturns[i]).decode('utf-8')
    except:
        continue

# testing for prefix
l = True
while l:
    l = False
    for i in range(len(opreturns)):
        if not prefix['s8'] in opreturns[i] and not prefix['n8'] in opreturns[i]:
            l = True
            del opreturns[i]
            break
        else:
            #opreturns[i] = opreturns[i].replace(prefix,'')
            print(opreturns[i])
