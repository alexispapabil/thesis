#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import argparse,yaml
import math,aux
import shared,stats

from manager import Manager

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'A parser used to obtain information concerning the resource manager. Also used to display state of execution.', usage = './main.py [-h] [-c C] [-l L] [-v]', add_help = False)
    parser.add_argument('-h', '--help', action='help', default = argparse.SUPPRESS, help = 'Show this help message and exit.')
    parser.add_argument('-c', '-config', metavar = ('FILEPATH'), nargs = '?', required = False, default = 'config/compact.yaml', type = str, help = 'The yaml file with the configuration for the job scheduler.')
    parser.add_argument('-i', '-info', required = False, help = 'Show information about the cluster. Accepted values: queue, state.')
    args = parser.parse_args()

    if args.i:
        with open(args.c) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            with open(config['State']) as f:
                tokens = f.readlines()
                i = tokens.index('\n')
                if args.i == 'queue':
                    lines = tokens[:i]
                    lines.sort(key = lambda line: int(line.split()[0]))
                    headers = ['Id', 'App', 'Procs', 'Status', 'Started', 'Remaining']
                    text = aux.format(headers)
                    for line in lines:
                        line = line.split(' ' + ' ')
                        if line[3] == 'R':
                            date, time = line[-2].split()
                            runtime = aux.elapsed(aux.todatetime(date, time))
                            line[-1] = aux.timew(int(line[-1]) - runtime)
                            line[-2] = time
                        else:
                            line[-1] = aux.timew(int(line[-1]))
                            line[-2] = '-'
                        text += aux.format(line)
                    aux.prettyprint(text)
                elif args.i == 'state':
                    lines = tokens[i+1:]
                    headers = ['Node', 'Socket', 'Taken', 'Status'] + ['Core' + ' ' + str(num) for num in range(config['Cores'])]
                    text = aux.format(headers)
                    for line in lines:
                        text += aux.format(line.split())
                    aux.prettyprint(text)
                else:
                    print('Provided invalid argument. See help for more info.')
    else:
        shared.init()
        with open(args.c) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            heatmap = config['Applications']['Heatmap'] if config['Allocation']['Policy'] == 'strip' else None
            manager = Manager(config['Nodes'], config['Sockets'], config['Cores'], config['Applications']['Path'], config['Applications']['Queue'], config['Log'], config['State'], heatmap)
            #Utility functions for the supported scheduling algorithms
            algorithms = {'FCFS': lambda j: aux.elapsed(j.enter), 'WFP3': lambda j: math.pow(aux.elapsed(j.enter)/j.duration,3)*j.procs}
            if config['Allocation']['Policy'] == 'strip':
                manager.readmap()
            manager.scheduler(config['Allocation']['Policy'], algorithms[config['Scheduling']['Algorithm']], config['Scheduling']['Backfilling'])
            print('{}({}):'.format(config['Scheduling']['Algorithm'],config['Scheduling']['Backfilling']), end = ' ')
            print(stats.avgs(config['Log'], shared.jobs))
