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

    # Parsing command line input
    algorithm_type = sys.argv[1]
    filename = sys.argv[2]
    run_time = float(sys.argv[3]) * 1000
    input_array = InputParser.parse_input(filename)

    # Get the size of each bin. The length of input is guarenteed to be divisible by 3
    _split = len(input_array) // 3

    # Initialize the bins
    best_bin_1 = None
    best_bin_2 = None
    best_bin_3 = None

    # Assume the best score to be negative infinity
    best_score = -math.inf

    if algorithm_type == 'hill':

        # Run hill climbing while there is still time left
        while run_time > 0:

            # Shuffle the input array
            shuffle(input_array)

            # Split the input array into 3 portions
            bin_1 = Bin1(input_array[0:_split])
            bin_2 = Bin2(input_array[_split:2 * _split])
            bin_3 = Bin3(input_array[2 * _split:len(input_array)])

            # Perform hill climbing
            # Return the 3 bins, the score, and the time left
            _b1, _b2, _b3, _score, run_time = Hill(bin_1, bin_2, bin_3, run_time).run()

            # If the score is better than the current best, log that
            if _score > best_score:
                best_score = _score
                best_bin_1 = _b1
                best_bin_2 = _b2
                best_bin_3 = _b3

    elif algorithm_type == 'annealing':

        # Run annealing while there is still time left
        while run_time > 0:

            # Shuffle the input array
            shuffle(input_array)

            # Split the input array into 3 portions
            bin_1 = Bin1(input_array[0:_split])
            bin_2 = Bin2(input_array[_split:2 * _split])
            bin_3 = Bin3(input_array[2 * _split:len(input_array)])

            # Perform annealing
            # Return the 3 bins, the score, and the time left
            _b1, _b2, _b3, _score, run_time = Annealing(bin_1, bin_2, bin_3, run_time).run()

            # If the score is better than the current best, log that
            if _score > best_score:
                best_score = _score
                best_bin_1 = _b1
                best_bin_2 = _b2
                best_bin_3 = _b3

    elif algorithm_type == 'ga':
        # TODO: Genetic Algorithm
        # Split the input array into 3 portions
        bin_1 = Bin1(input_array[0:_split])
        bin_2 = Bin2(input_array[_split:2 * _split])
        bin_3 = Bin3(input_array[2 * _split:len(input_array)])
        print('Genetic Algorithm')
        GeneticAlgorithm(bin_1, bin_2, bin_3, run_time).run()
    else:
        print('Unsupported algorithm.')
        exit()
    print('Bin 1: ', best_bin_1, '\nBin 2: ', best_bin_2, '\nBin 3: ', best_bin_3, '\nBest Score:', best_score)

if __name__ == '__main__':
    main()
