import os

str = os.environ.get('MAIL_PASSWORD')
pwd = os.environ['MAIL_PASSWORD']
tmp = os.environ['TEMP']

import os
print (os.environ["TEMP"])
print 'pwd:',pwd
print 'tmp:',tmp
print 'get env:',str