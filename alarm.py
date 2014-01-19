#!/usr/bin/python

import time, subprocess, sys, re

station = '3'

if (len(sys.argv) != 2 or not re.match('^[0-2][0-9]:[0-5][0-9]$',sys.argv[1]) or int(sys.argv[1].split(':')[0]) > 23):
	sys.exit("Please format as: alarm hh:mm")

wakeup = map(int, sys.argv[1].split(':'))
print "Waking you up at: %s:%s" %(str(wakeup[0]).zfill(2),str(wakeup[1]).zfill(2))

while(1):
	now = list(time.localtime()[3:5])
	if (now == wakeup):
		print "Ding ding!"
		if subprocess.call(['pidof','pianobar'], stdout=open(__import__('os').devnull,'wb')):
			print 'Starting Pianobar instance...'
			subprocess.call(['pianobar'])
			open('/home/banks/.config/pianobar/ctl','a').write(station+'\n')
		else:	open('/home/banks/.config/pianobar/ctl','a').write('p')

		break

