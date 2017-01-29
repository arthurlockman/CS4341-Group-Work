from input_parser import InputParser
import sys
from random import shuffle
from algorithm import *
from bin import *
import math


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
    run_time = int(sys.argv[3]) * 1000
    _input = InputParser.parse_input(filename)
    _split = len(_input) // 3

    # bin_1 = Bin1(_input[0:_split])
    # bin_2 = Bin2(_input[_split:2*_split])
    # bin_3 = Bin3(_input[2*_split:len(_input)])

    if algorithm_type == 'hill':
        best_bin_1 = None
        best_bin_2 = None
        best_bin_3 = None
        best_score = -math.inf
        while run_time > 0:
            shuffle(_input)
            bin_1 = Bin1(_input[0:_split])
            bin_2 = Bin2(_input[_split:2 * _split])
            bin_3 = Bin3(_input[2 * _split:len(_input)])
            _b1, _b2, _b3, _score, run_time = Hill(bin_1, bin_2, bin_3, run_time).run()
            if _score > best_score:
                best_score = _score
                best_bin_1 = _b1
                best_bin_2 = _b2
                best_bin_3 = _b3
        print('Bin 1: ', best_bin_1, '\nBin 2: ', best_bin_2, '\nBin 3: ', best_bin_3, '\nBest Score:', best_score)
    elif algorithm_type == 'annealing':
        print('Annealing')
    elif algorithm_type == 'ga':
        print('Genetic Algorithm')
    else:
        print('Unsupported algorithm.')
        exit()


if __name__ == '__main__':
    main()
