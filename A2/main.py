from input_parser import InputParser
import sys
from random import shuffle
from algorithm import *
from bin import *

def main():
    if len(sys.argv) < 4:
        print('Error: incorrect input arguments selected.')
        print()
        print('Usage: python3 main.py [optimization type] [filename] ' +
              '[time limit]')
        print('       optimization type: hill, annealing, or ga')
        print('       filename: the input filename to read')
        print('       time limit: the time limit (in seconds) to limit ' +
              'the optimization to')
        exit()
    algorithm_type = sys.argv[1]
    filename = sys.argv[2]
    run_time = int(sys.argv[3])

    _input = InputParser.parse_input(filename)
    shuffle(_input)

    _split = len(_input) // 3

    bin_1 = Bin1(_input[0:_split])
    bin_2 = Bin2(_input[_split:2*_split])
    bin_3 = Bin3(_input[2*_split:len(_input)])

    Hill(bin_1, bin_2, bin_3, run_time).run()

    print(_input)
    if algorithm_type is 'hill':
        print('Hill climbing')
    elif algorithm_type is 'annealing':
        print('Annealing')
    elif algorithm_type is 'ga':
        print('Genetic Algorithm')
    else:
        print('Unsupported algorithm.')
        exit()


if __name__ == '__main__':
    main()
