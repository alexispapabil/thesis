#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import datetime

def format(tokens):
    return ''.join('{:<10}'.format(token) for token in tokens) + '\n'

def todatetime(date, time):
    return datetime.datetime.strptime(date + ' ' + time, '%d-%m-%Y %H:%M:%S')

def elapsed(timestamp):
    return (datetime.datetime.now()-timestamp).total_seconds()

def tostring(timestamp):
    if timestamp:
        return timestamp.strftime('%d-%m-%Y %H:%M:%S')
    return str(None)

def timew(limit):
    minutes, seconds = divmod(limit, 60)
    hours, minutes = divmod(minutes, 60)
    return "%02d" % (hours,) + ':' + "%02d" % (minutes,) + ':' + "%02d" % (seconds,)

def prettyprint(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['+' + '-' * width + '+']
    for num,s in enumerate(lines):
        res.append('|' + (s + ' ' * width)[:width] + '|')
        if not num:
            res.append('+' + ('-' * width) + '+')
    res.append('+' + '-' * width + '+')
    print('\n'.join(res))
