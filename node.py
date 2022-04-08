#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from slot import Socket

class Node:
    def __init__(self, name, sockets, cores):
        self.name = name
        self.cores = cores
        self.exclusive = 0
        self.sockets = []
        for i in range(sockets):
            self.sockets.append(Socket(i, self.cores))

    def occupied(self, policy):
        for socket in self.sockets:
            if socket.occupied(policy):
                return 1
        return 0

    def free(self, jobs):
        self.exclusive = 0
        for socket in self.sockets:
            socket.free(jobs)

    def remaining(self):
        window = map(lambda socket: socket.remaining(), self.sockets)
        window = [interval for socket in window for interval in socket]
        return min(window)

    def myjobs(self):
        jobs = set()
        for socket in self.sockets:
            jobs = jobs.union(set(socket.myjobs()))
        return jobs

    def precedence(self, heatmap, job):
        jobs = self.myjobs()
        if jobs:
            (myjob,) = jobs
            return heatmap[job.app.split('.')[0]][myjob.app.split('.')[0]]
        else:
            return 0
    
    def __str__(self):
        text = ''
        for socket in self.sockets:
            text += self.name + ' ' + str(socket) + '\n'
        return text
