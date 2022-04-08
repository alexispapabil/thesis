#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os,sys,time
import random,math

def rewind(num):
    r = open('rewind','r')
    f = open('queue','a')
    for i in range(num):
        app, p, w, x, interval = r.readline().split()
        f.write(app + ' ' + p  + ' ' + w + ' ' + x + '\n')
        f.flush()
        time.sleep(int(interval))

def generator(num):
    apps = ['bt','cg','ep','ft','is','lu','mg','sp']
    procs = [2**i for i in range(2,7)]
    classes = ['B']
    walltime = {
            'bt':[550, 230, 230, 80, 90, 80, 80],
            'cg':[120, 90, 70, 60, 90, 150, 120],
            'ep':[70, 40, 20, 10, 5, 3, 2],
            'ft':[100, 70, 60, 50, 60, 50, 80],
            'is':[10, 5, 5, 5, 10, 20, 10],
            'lu':[260, 170, 120, 60, 45, 50, 50],
            'mg':[20, 20, 10, 10, 10, 5, 5],
            'sp':[640, 470, 470, 160, 160, 130, 130]
            }

    r = open('rewind','a')
    f = open('queue','a')
    for i in range(num):
        app = random.choice(apps)
        c = random.choice(classes)
        p = random.choice(procs)
        w = walltime[app][int(math.log(p,2))-1]
        interval = random.randint(3,10)
        r.write(app + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w) + ' ' + str(0) + ' ' + str(interval) + '\n')
        f.write(app + '.' + c + '.' + 'x' + ' ' + str(p) + ' ' + str(w) + ' ' + str(0) + '\n')
        f.flush()
        time.sleep(interval)

if __name__ == '__main__':

    if os.path.exists('rewind'):
        rewind(int(sys.argv[1]))
    else:
        generator(int(sys.argv[1]))
