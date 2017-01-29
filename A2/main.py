from input_parser import InputParser
import sys
from random import shuffle
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
    run_time = sys.argv[3]
    randomized_input = shuffle(InputParser.parse_input(filename))
    _split = len(randomized_input) / 3
    bin_1 = Bin1(randomized_input[0:_split])
    bin_2 = Bin2(randomized_input[_split:2*_split)
    bin_3 = Bin3(randomized_input[2*_split:len(randomized_input)])
    print(randomized_input)
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
