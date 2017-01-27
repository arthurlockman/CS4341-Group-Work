# Assignment 1

This assignment will familiarize you with A* search, 
the use of different heuristic functions, computing 
effective branching factor, and writing up your results. 
You should use the graph version of A* search.

## Installing Python 3

To run this program, you will need to have Python 3 installed on your system. 
To install Python 3, use the download link on [Python.org](https://www.python.org) 
for Python 3.6.0 for your system. Once installed, you should be able to run the program.

## Running the Program

The command line options for the program are listed below.

    python3 astar.py [filename] [heurstic value (1-6)] [-v]
           filename: should be the name or path to a map file to load
           heurstic: can be one of the following:
               1: 0 heuristic
               2: Min(vertical, horizontal)
               3: Max(vertical, horizontal)
               4: Vertical + horizontal
               5: Manhattan Distance + number of turns
               6: Heuristic 5 * 3
               7: Distance formula
           -v: this option (if set) will provide a visualization of the A* progress
           -c: this option (if set) will print the output in a machine-readable format

    Example: python3 astar.py grid25.txt 4 -v

The same information can be printed by running the function `python3 astar.py` with 
no arguments provided.

Depending on your system configuration, the python 3 binary may be linked to either
`python3` or simply `python`. If you're having trouble running the program, check to make
sure that you're actually running under python 3.

## Visualizing the Program
A quick visualizer for A* algorithm was put together using Python3's Tkinter. To visualize the algorithm, run the program with the -v argument. Tkinter is not included in all python distributions, so it may not work out of the box on your machine. Included in the repo is an A*-visualization.mov file. It is a screen recording of the visualization of a 25x25 boards.