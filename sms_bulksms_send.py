#!/usr/bin/env python
#
# Usage:
#   echo "Message on standard input" | send_sms.py 44123456789
#

import urllib
import sys
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/etc/bulksms.conf')

recipient = sys.argv[1]
message = sys.stdin.read()

url = "https://bulksms.vsms.net/eapi/submission/send_sms/2/2.0"
params = urllib.urlencode({
    'username' : config.get('api', 'username'),
    'password' : config.get('api', 'password'),
    'message' : message,
    'msisdn' : recipient
})
f = urllib.urlopen(url, params)
s = f.read()
f.close()

result = s.split('|')
statusCode = result[0]
statusString = result[1]
if statusCode != '0':
    print "ERROR: " + statusCode + ": " + statusString
    sys.exit(2)

print "OK: batch ID " + result[2]
