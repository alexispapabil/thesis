#!/usr/bin/env python3
#-*- coding: utf-8 -*-

class Socket:
    def __init__(self, num, cores):
        self.num = num
        self.cores = cores
        self.jobs = [None]*self.cores

    def occupied(self, policy):
        if policy == 'strip':
            jobs = 1
        else:
            jobs = 0
        return len(set(self.myjobs())) > jobs

    def free(self, jobs):
        for i in range(self.cores):
            if self.jobs[i] and self.jobs[i] in jobs:
                self.jobs[i] = None

    def freecore(self):
        for index,job in enumerate(self.jobs):
            if not job:
                return index

    def myjobs(self):
        return [job for job in self.jobs if job]

    def remaining(self):
        jobs = set(self.myjobs())
        window = map(lambda job: job.remaining(), jobs)
        return window

    def taken(self):
        return len(self.myjobs())

    def state(self):
        if not self.taken():
            return 'Empty'
        elif self.taken() == self.cores:
            return 'Full'
        else:
            return 'Slots'

    def __str__(self):
        text = str(self.num) + ' ' + str(self.taken()) + '/' + str(self.cores) +  ' ' + self.state() + ' '
        text += ' '.join([job.app if job else '.' for job in self.jobs])
        return text
