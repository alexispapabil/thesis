## Description
A Python implementation of an adjustable resource manager for MPI applications of a computer cluster. It consists of:
  - A *scheduling* module supporting two algorithms:
    1. ***FCFS***: Favours old jobs.
    2. ***WFP3***: Favours short/old jobs while taking into account their respective size.
  - An optional *backfilling* module.
  - A *resource allocation* module implementing three policies: 
    1. ***Compact***: Use all the cores of a node on one app.
    2. ***Spare***: Use half the cores of a node on one app (unfavored).
    3. ***Strip (co-scheduling)***: Split the cores of a node between two apps. Can be improved with the inclusion of a heatmap, used to identify apps that match well together.
  - The *main* module that glues all of the above.

## Execution

The main module of this program has been designed as a command line interface (CLI). It takes two arguments:
1. ***<-c,-config>***: A yaml configuration file that contains the user's preferences. An example is shown below. This is a required parameter for commencing the execution. In order to run, simply type: `python3 main.py -c path/to/config`.
<p align="center">
  <img width="600" height="450" src="https://user-images.githubusercontent.com/57871211/162432383-062c3ea8-39a5-4f92-83c5-259de3a4dd09.png">
</p>

2. ***<-i,-info>***: An optional argument that can take one of two values:
    1. **queue**: Display information about the cluster's current jobs.
    <p align="center">
      <img width="550" height="150" src="https://user-images.githubusercontent.com/57871211/162433778-e1592b6d-26d4-4775-b035-5197cdd2f226.png">
    </p>
    
    3. **state**: Display information about the cluster's nodes.
    <p align="center">
      <img width="550" height="400"src="https://user-images.githubusercontent.com/57871211/162433927-d3ba862f-c1f2-42b8-9ed2-e3b2407421f4.png">
    </p>

## Usage within a cluster

After being submitted as a batch job, the main program assigns MPI tasks across a number of bound nodes. These tasks are part of a queue consisting of applications from the Nas Parallel Benchmarks (NPB) suite.
<p align="center">
      <img width="650" height="450" src="https://user-images.githubusercontent.com/57871211/162578959-caa576a3-2b52-4de7-aa06-ac33d7f40ec4.png">
</p>

## Dependencies

In order to run the code, Python's PyYAML framework must be installed. This can be done with the pip package installer by typing `pip install pyyaml`. Full code dependencies can be found in the **environment.yml** file which has been exported from the miniconda package manager and can be used locally with the `conda env create -f environment.yml` command.
