#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os,subprocess
import math,datetime,time
import shared,init

from job import Job
from node import Node

class Manager:
    def __init__(self, nodes, sockets, cores, appdir, queuefile, logdir, f, hmapfile = None):
        self.sockets = sockets
        self.cores = cores
        self.appdir = appdir
        self.queuefile = queuefile
        self.logdir = logdir
        self.hmapfile = hmapfile
        self.rankdir = os.path.join(os.getcwd(), 'rankfiles')
        self.piddir = os.path.join(os.getcwd(), 'pids')
        self.queue = []
        self.scheduled = set()
        self.heatmap = dict()
        self.f = f
        self.nodes = []
        for num in range(nodes):
            self.nodes.append(Node('n' + str(num), sockets, cores))

    #Read the heatmap
    def readmap(self):
        f = open(self.hmapfile, 'r')
        tokens = f.readline().split()
        while tokens:
            for num,token in enumerate(tokens):
                if not num:
                    key = token
                    self.heatmap[token] = dict()
                else:
                    self.heatmap[key][token] = num
            tokens = f.readline().split()

    #Read the queue starting from the line indicated by (index)
    def readqueue(self, index):
        f = open(self.queuefile, 'r')
        lines = f.readlines()[index:]
        id = index
        for line in lines:
            tokens = line.split()
            self.queue.append(Job(id, tokens[0], int(tokens[1]), int(tokens[2]), datetime.datetime.now(), int(tokens[3])))
            id += 1
        return id

    #Find backfilling time window 
    def backlog(self, job, nodes, i):
        occupied = [node for node in self.nodes if node not in nodes]
        window = map(lambda node: node.remaining(), occupied)
        job.runafter(sorted(window)[i-1])

    #Backfilling
    def backfill(self, policy):
        i = 1
        while i < len(self.queue) and not self.full(policy):
            if self.queue[i].duration <= self.queue[0].interval:
                if self.submit(self.queue[i], policy, 1):
                    job = self.queue.pop(i)
                    job.startedat(datetime.datetime.now())
                    self.scheduled.add(job)
                    shared.jobs.add(job)
            i += 1

    #Find required nodes for a job
    def findnodes(self, job, policy, bf):
        if policy == 'compact':
            nodes = [node for node in self.nodes if not node.occupied(policy)]
            num = math.ceil(job.procs/(self.cores*self.sockets))
        elif policy == 'spare':
            nodes = [node for node in self.nodes if not node.occupied(policy)]
            num = math.ceil(2*job.procs/(self.cores*self.sockets))
        elif policy == 'strip':
            nodes = [node for node in self.nodes if not (node.occupied(policy) or node.exclusive)]
            nodes.sort(key = lambda node: node.precedence(self.heatmap, job))
            num = math.ceil(2*job.procs/(self.cores*self.sockets))
        if num > len(nodes):
            if bf and job == self.queue[0]:
                self.backlog(job, set(nodes), num-len(nodes))
            return []
        return nodes[:num]

    #Assign parallel tasks to processors
    def bind(self, nodes, job, pps):
        if not os.path.exists(self.rankdir):
            os.mkdir(self.rankdir)
        rem = job.procs
        rf = open(os.path.join(self.rankdir, job.app + '.' + str(job.id) + '.' + 'rf'), 'w')
        for num,node in enumerate(nodes):
            node.exclusive = job.exclusive
            for socket in node.sockets:
                while rem:
                    i = socket.freecore()
                    socket.jobs[i] = job
                    rf.write('rank' + ' ' + str(job.procs-rem) + '=+n' + str(num) + ' ' + 'slot=' + str(socket.num) + ':' + str(i) + '\n')
                    rem -= 1
                    if not rem%pps:
                        break
        return os.path.abspath(rf.name)

    #Run from shell
    def mpirun(self, hosts, job, rankfile):
        out = job.app + '.' + str(job.id) + '.' + 'o'
        err = job.app + '.' + str(job.id) + '.' + 'e'
        subprocess.call('echo '' > ' + self.piddir + '/' + str(job.id), shell = True)
        mpirun = 'mpirun -H ' + hosts + ' -np ' + str(job.procs) + ' -v --report-bindings --timestamp-output -rf ' + \
           rankfile + ' ' + self.appdir + '/' + job.app + ' 2>> ' + self.logdir + '/' + \
           err + ' 1>> ' + self.logdir + '/' + out + ' && '
        mpirun += 'rm' + ' ' + self.piddir + '/' + str(job.id) + '\n'
        subprocess.Popen(mpirun, shell = True)

    #Submit a job for execution
    def submit(self, job, policy, bf):
        policy = 'spare' if policy == 'strip' and job.exclusive else policy
        nodes = self.findnodes(job, policy, bf)
        if nodes and policy == 'compact':
            rankfile = self.bind(nodes, job, self.cores)
        elif nodes and policy == 'spare':
            rankfile = self.bind(nodes, job, self.cores//2)
        elif nodes and policy == 'strip':
            rankfile = self.bind(nodes, job, self.cores//2)
        else:
            return 0
        names = [node.name for node in nodes]
        hosts = '+' + ',+'.join(names)
        self.mpirun(hosts, job, rankfile)
        return 1
    
    #Job scheduler. Applies an algorithm by sorting the queue according to the (fun) parameter
    def scheduler(self, policy, fun, bf):
        flag = 0
        index = 0
        os.mkdir(self.piddir)
        p = init.makeqfile()
        while 1:
            self.free()
            index = self.readqueue(index)
            if self.queue:
                self.queue.sort(key = lambda job: (fun)(job), reverse = True)
                if self.submit(self.queue[0], policy, bf):
                    job = self.queue.pop(0)
                    job.startedat(datetime.datetime.now())
                    self.scheduled.add(job)
                    shared.jobs.add(job)
                elif bf:
                    self.backfill(policy)
            elif self.empty() and p.poll()==0:
                os.rmdir(self.piddir)
                flag = 1
            self.snapshot()
            if flag:
                break
            time.sleep(10)

    #Free nodes from completed jobs
    def free(self):
        running = set(int(pid) for pid in os.listdir(self.piddir))
        for node in self.nodes:
            jobs = set(job for job in node.myjobs() if job.id not in running)
            if jobs:
                self.scheduled = self.scheduled.difference(jobs)
                node.free(jobs)

    #Check if the cluster is empty
    def empty(self):
        return not os.listdir(self.piddir)

    #Check if the cluster is full
    def full(self, policy):
        for node in self.nodes:
            if not node.occupied(policy):
                return 0
        return 1
    
    #Save the cluster's current state
    def snapshot(self):
        text = ''
        for job in set(self.queue).union(self.scheduled):
            text += str(job) + '\n'
        text += '\n'
        for node in self.nodes:
            text += str(node) +'\n'
        with open(self.f, 'w') as f:
            f.write(text[:-1])
