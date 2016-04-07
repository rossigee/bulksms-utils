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

url = "https://bulksms.vsms.net/eapi/user/get_credits/1/1.1"
params = urllib.urlencode({
    'username' : config.get('api', 'username'),
    'password' : config.get('api', 'password'),
})
f = urllib.urlopen(url, params)
s = f.read()
f.close()

result = s.split('|')
statusCode = result[0]
statusString = result[1]
if statusCode != '0':
    print "ERROR -" + statusCode + ": " + statusString
    sys.exit(3)

credits = float(statusString)
if credits > 10:
    print "Balance OK - %0.2f credits" % credits
else:
    print "Low balance - %0.2f credits" % credits
    sys.exit(1)

