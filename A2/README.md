# Assignment 2

## Installing Python 3

To run this program, you will need to have Python 3 installed on your system. 
To install Python 3, use the download link on [Python.org](https://www.python.org) 
for Python 3.6.0 for your system. Once installed, you should be able to run the program.

## Running the Program

The command line options for the program are listed below.

  python3 optimize.py [optimization type] [filename] [time limit] [-mp]
       optimization type: hill, annealing, or ga
       filename: the input filename to read
       time limit: the time limit (in seconds) to limit the optimization to
       mp processes: use -mp to use multiple processes [EXPERIMENTAL]


    Example: python3 optimize.py hill tuning_sets/tune_600_a.txt 30.0 -mp

The same information can be printed by running the function `python3 optimize.py` with no arguments provided.

Depending on your system configuration, the python 3 binary may be linked to either
`python3` or simply `python`. If you're having trouble running the program, check to make
sure that you're actually running under python 3.

## Tuning & Testing Files
To tune the simulated annealing and genetic algorithm hyperparameters, we used a number of tuning sets found in the tuning_sets/ directory. To test the temperature schedule functions for the simulated annealing, all three sets of size 600, 3000, and 9999 were used and the the scores for each result were averaged. For the genetic algorithm, only the set of size 600 was used. To test the algorithms, each algorithm was run on the test.txt and the results are displayed in the write-up.


## Multi-Processor Support
We added multiple process support to our code. When run in multi-processor support mode, the program will detect the number of possible parallel processes that can run and run the algorithm multiple times in parallel using that number of processors. For example, a machine with 4 cores (with hyperthreading) can run 8 simultaneous processes. The program will run any algorithm 8 times in parallel and then take the maximum value. We squeeze out a bit of extra performance in the same amount of time. For example, the hill climbing algorithm might return a value between 2100-2400 for any individual run, but maximizing over 8 processes often yields a value around 2400, the optimal value. To run the program in multi-processing mode, simply add a '-mp' flag at the end of the command line.
