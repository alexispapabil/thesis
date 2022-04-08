## Description
A Python implementation of an adjustable resource manager for MPI applications that run on a computer cluster. It consists of:
  - A *scheduling* module supporting two algorithms:
    1. ***FCFS***: Favours old jobs.
    2. ***WFP3***: Favours short/old jobs while taking in account their respective size.
  - An optional *backfilling* module.
  - A *resource allocation* module implementing three policies: 
    1. ***Compact***: Use all the cores of a node on one app.
    2. ***Spare***: Use half the cores of a node on one app (unfavored).
    3. ***Strip (co-scheduling)***: Split the cores of a node between two apps. Can be improved with the inclusion of a heatmap, used to indicate apps that match well together.
  - The *main* module that glues all of the above.

## Execution

The main module of this program has been designed as a command line interface (CLI). It takes two arguments:
1. **<-c,-config>**: A yaml configuration file that contains the user's preferences. An example is shown below. This is a required parameter for the commence of the execution. In order to run, simply type: `python3 main.py -c path/to/config`.

2. **<-i,-info>**: An optional argument that can take one of two values:
    1. **queue**: Display information about the cluster's current jobs.
    2. **state**: Display information about the cluster's nodes.

## Usage within a cluster

After being submitted as a batch job, the main program assigns MPI tasks across a number of bound nodes. These tasks are part of a queue consisting of applications from the Nas Parallel Benchmarks (NPB) suite.
