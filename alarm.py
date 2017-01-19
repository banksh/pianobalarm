#!/usr/bin/python

import time, subprocess, sys, re

station = '3'

args = sys.argv

def getFlags(args):
	matches = map(re.compile('-{1,2}[a-z]+').match,args)
	args = [i for i in args if not re.match('-',i)]
	return [flag.group() for flag in matches if flag], args

def checkArgs(args, flags):
	if len(args) != 2 and ('-h' not in flags and '--help' not in flags):
		sys.exit("Incorrect number of arguments. Try -h or --help for usage")
	if ('-h' in flags or '--help' in flags):
		printHelp()
		sys.exit()

def printHelp():
	print """Usage: alarm [-r|--help] <time>

<time> syntax: <hh:mm> | <hh> | <mm>m

Use -r for a relative time using <hh:mm>, otherwise absolute time is the default."""

def getTime(args):
	alarmTime = args[1]
	if (re.sub('(\d+)m$','00:\\1',args[1]) != alarmTime):
		alarmTime = re.sub('(\d+)m$','00:\\1',args[1])
		return alarmTime, 1
	if (re.sub('^(\d+)$','\\1:00', args[1]) != alarmTime):
		alarmTime = re.sub('(\d+)$','\\1:00', args[1])
		return alarmTime, 2
        if not (re.match('^[0-9]+:[0-5][0-9]$',args[1])):
               sys.exit("Incorrectly formatted arguments. Try -h or --help for usage")
	return alarmTime, 0

def setTime(flags):
	alarmTime, rel = getTime(args)
	alarmTime = alarmTime.split(':')
	realTime = time.localtime()
	if '-r' in flags: rel = 2
	if rel==1:
		print "Alarm set for %sh %sm from now" %(alarmTime[0].zfill(2),alarmTime[1].zfill(2))
		alarmTime = map(int, alarmTime)
		alarmTime[1] += realTime[4]
		return alarmTime
	if rel==2:
		print "Alarm set for %sh %sm from now" %(alarmTime[0].zfill(2),alarmTime[1].zfill(2))
		alarmTime = map(int, alarmTime)
		alarmTime[0] += realTime[3]
		alarmTime[1] += realTime[4]
		return alarmTime
        if alarmTime[0] > 23:
                sys.exit("Specified time is invalid. Try -h or --help for usage")
	print "Alarm set for %s:%s" %(alarmTime[0].zfill(2),alarmTime[1].zfill(2))
	alarmTime = map(int, alarmTime)
	return alarmTime

flags, args = getFlags(args)
checkArgs(args, flags)
alarmTime = setTime(flags)

while(1):
	now = list(time.localtime()[3:5])
	if (now == alarmTime):
		print "Ding ding!"
		if subprocess.call(['pidof','pianobar'], stdout=open(__import__('os').devnull,'wb')):
			print 'Starting Pianobar instance...'
			subprocess.call(['pianobar'])
			open('~/.config/pianobar/ctl','a').write(station+'\n')
		else:	open('~/.config/pianobar/ctl','a').write('p')

		break
	time.sleep(1)
