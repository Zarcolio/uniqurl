#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import requests
import hashlib
import multiprocessing 

requests.packages.urllib3.disable_warnings() 

def GetRequest(sUrl,sHeaders, sCookies, sProxies):
    try:
        sGetRequestResults = requests.get(sUrl, headers=sHeaders, cookies=sCookies, proxies={"http": sProxies, "https": sProxies}, allow_redirects=aArguments.redirect, timeout=aArguments.timeout, verify=False)
        if sGetRequestResults:
            sHash=hashlib.md5(sGetRequestResults.text.encode('utf-8')).hexdigest()
            dAllGetRequestResults[sUrl] = sHash
    except:
        return False

# Get some commandline arguments:
sArgParser=argparse.ArgumentParser(description='Use uniqurl to distinguish unique URLs based on the MD5 hash of the content of the page.')
sArgParser.add_argument('-headers', metavar="<headers>", help='Supply header to a GET request.', default=None)
sArgParser.add_argument('-cookies', metavar="<cookies>", help='Supply cookie to a GET request.', default=None)
sArgParser.add_argument('-proxy', metavar="<proxy>", help='Supply a proxy to a GET request.', default=None)
sArgParser.add_argument('-redirect', metavar="<boolean>", help='Allow redirects, defaults to "True", use "False" to disable.', default=True)
sArgParser.add_argument('-timeout', metavar="<seconds>", help='Define a timeout for the requests, defaults to 2 seconds.', default=5)
sArgParser.add_argument('-workers', metavar="<workers>", help='Define a number of parallel workers, defaults to 20 workers.', default=20)

aArguments=sArgParser.parse_args()

x = 0
dResults = {}

#Read from standard input and put it in a list:
lInput=[]
try:
    for strInput in sys.stdin:
        lInput.append(strInput.rstrip())
except:
    pass


if aArguments.headers:
    if ";" in aArguments.headers:
        dHeaders = dict(item.split(":") for item in aArguments.headers.split(";"))
    else:
        dHeaders = dict([aArguments.headers.split(":")])
else:
    dHeaders = []

if aArguments.cookies:
    if ";" in aArguments.cookies:
        dCookies = dict(item.split(":") for item in aArguments.cookies.split(";"))
    else:
        dCookies = dict([aArguments.cookies.split(":")])
else:
    dCookies = []


manager = multiprocessing.Manager()
dAllGetRequestResults = manager.dict()

pool = multiprocessing.Pool(int(aArguments.workers))

try:
    for strInput in lInput:
        #sGetRequestResults = GetRequest(strInput, dHeaders, dCookies, aArguments.proxy)
        result = pool.apply_async(GetRequest, args = (strInput, dHeaders, dCookies, aArguments.proxy))
    
    pool.close()
    pool.join()
except KeyboardInterrupt:
    sys.stderr.write("\nCtrl-C detected, terminating all workers...\n")
    pool.terminate()
    pool.join()
    sys.exit(0)
    
dAllGetRequestResults2 = {}
for sUrlx in sorted(dAllGetRequestResults.keys(), key=len, reverse=True):
    dAllGetRequestResults2[dAllGetRequestResults[sUrlx]] = sUrlx

for sUrlx in sorted(dAllGetRequestResults2.values()):
    print(sUrlx)
