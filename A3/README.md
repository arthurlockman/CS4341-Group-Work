# Assignment 3

## Installing Python 3

To run this program, you will need to have Python 3 installed on your system.
To install Python 3, use the download link on [Python.org](https://www.python.org)
for Python 3.6.0 for your system. Once installed, you should be able to run the program.

## Running the Program

The command line options for the program are listed below.

  python3 sample.py [query node=condition] [number of iterations] [observed node=condition] ...

Each node could be one of the following:
    humidity=[LOW, HIGH], temperature=[WARM, MILD, COLD], icy=[TRUE, FALSE],
    snow=[TRUE, FALSE], day=[WEEKEND, WEEKDAY], cloudy=[TRUE, FALSE],
    exams=[TRUE, FALSE], stress=[HIGH, LOW]

    Example: python3 sample.py humidity=low 50000 day=weekday snow=true

The same information can be printed by running the function `python3 sample.py` with no arguments provided.

Depending on your system configuration, the python 3 binary may be linked to either
`python3` or simply `python`. If you're having trouble running the program, check to make
sure that you're actually running under python 3.