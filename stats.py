#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import datetime

def runtime(path):
    f = open(path, 'r')
    while 1:
        line = f.readline()
        if 'Time in seconds' in line:
            return float(line.split()[-1])

def avgs(logdir,jobs):
    wait = 0
    run = 0
    for job in jobs:
        wait += (job.start-job.enter).total_seconds()
        run += runtime(logdir + '/' + job.app + '.' + str(job.id) + '.' + 'o')
    return (round(wait/len(jobs), 2), round(run/len(jobs), 2), round((wait+run)/len(jobs), 2))
