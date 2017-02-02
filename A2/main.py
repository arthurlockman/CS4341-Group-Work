from algorithm import *
from bin import *
from input_parser import InputParser


def parse_command_line_input():
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

    return algorithm_type, filename, run_time


def main():
    (algorithm_type, filename, run_time) = parse_command_line_input()

    input_array = InputParser.parse_input(filename)

    best_bin_1, best_bin_2, best_bin_3, best_score = None, None, None, None
    if algorithm_type == 'hill':
        best_bin_1, best_bin_2, best_bin_3, best_score = run_hill(input_array, run_time)
    elif algorithm_type == 'annealing':
        best_bin_1, best_bin_2, best_bin_3, best_score = run_annealing(input_array, run_time)
    elif algorithm_type == 'ga':
        best_bin_1, best_bin_2, best_bin_3, best_score = run_genetic(input_array, run_time)
    else:
        print('Unsupported algorithm.')
        exit()

    print('Bin 1: ', best_bin_1, '\nBin 2: ', best_bin_2, '\nBin 3: ', best_bin_3, '\nBest Score:', best_score)


def run_hill(input_array, run_time):
    # Assume the best score to be negative infinity
    best_score = -math.inf

    # Initialize the bins
    best_bin_1 = None
    best_bin_2 = None
    best_bin_3 = None

    # Run hill climbing while there is still time left
    while run_time > 0:

        # Shuffle the input array
        shuffle(input_array)

        # Get the size of each bin. The length of input is guarenteed to be divisible by 3
        _split = len(input_array) // 3

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

    return best_bin_1, best_bin_2, best_bin_3, best_score


def run_annealing(input_array, run_time, t_max=10, sideways_max=100,
                  t_schedule_fun=lambda max_temp, time_left, total_time: max_temp * (time_left / total_time)):
    # Assume the best score to be negative infinity
    best_score = -math.inf

    # Initialize the bins
    best_bin_1 = None
    best_bin_2 = None
    best_bin_3 = None

    # Run annealing while there is still time left
    while run_time > 0:

        # Shuffle the input array
        shuffle(input_array)

        # Get the size of each bin. The length of input is guarenteed to be divisible by 3
        _split = len(input_array) // 3

        # Split the input array into 3 portions
        bin_1 = Bin1(input_array[0:_split])
        bin_2 = Bin2(input_array[_split:2 * _split])
        bin_3 = Bin3(input_array[2 * _split:len(input_array)])

        # Perform annealing
        # Return the 3 bins, the score, and the time left
        _b1, _b2, _b3, _score, run_time = Annealing(bin_1, bin_2, bin_3, run_time, t_max, sideways_max,
                                                    t_schedule_fun).run()

        # If the score is better than the current best, log that
        if _score > best_score:
            best_score = _score
            best_bin_1 = _b1
            best_bin_2 = _b2
            best_bin_3 = _b3

    return best_bin_1, best_bin_2, best_bin_3, best_score


def run_genetic(input_array, run_time, pop_size=100, elitism_pct=0.30):
    # Shuffle the input array
    shuffle(input_array)

    # Get the size of each bin. The length of input is guarenteed to be divisible by 3
    _split = len(input_array) // 3

    # Split the input array into 3 portions
    bin_1 = Bin1(input_array[0:_split])
    bin_2 = Bin2(input_array[_split:2 * _split])
    bin_3 = Bin3(input_array[2 * _split:len(input_array)])

    _b1, _b2, _b3, _score, _ = GeneticAlgorithm(bin_1, bin_2, bin_3, run_time, pop_size=pop_size,
                                                elitism_pct=elitism_pct).run()

    return _b1, _b2, _b3, _score


def tune_annealing():
    temperature_schedule_functions = [
        lambda time_left, _max_temp, total_time: time_left * (_max_temp / total_time),
        lambda time_left, _max_temp, total_time: (time_left ** 2) * (_max_temp / total_time),
        lambda time_left, _max_temp, total_time: math.exp(time_left * (_max_temp / total_time)) - 1]

    max_temperatures = [
        1000, 500, 100, 10, 5, 1, 0.5, 0.1, 0.05
    ]

    tuning_files = [
        'tuning_sets/tune_3000_a.txt',
        'tuning_sets/tune_3000_b.txt',
        'tuning_sets/tune_3000_c.txt',
        'tuning_sets/tune_3000_d.txt',
        'tuning_sets/tune_3000_e.txt'
    ]

    run_time_ms = 10000

    # Tune for temperature function
    # for temperature_schedule_function in temperature_schedule_functions:
    #     total = 0
    #     for filename in tuning_files:
    #         input_array = InputParser.parse_input(filename)
    #         _, _, _, score = run_annealing(input_array, run_time_ms, t_max=10,
    #                          sideways_max=100, t_schedule_fun=temperature_schedule_function)
    #         total += score

    #     average = float(total) / float(len(tuning_files))
    #     print(average)

    for max_temp in max_temperatures:
        total = 0
        for filename in tuning_files:
            input_array = InputParser.parse_input(filename)

            # Running with linear function. Performed best earlier
            _, _, _, score = run_annealing(input_array, run_time_ms, t_max=max_temp, sideways_max=100,
                                           t_schedule_fun=temperature_schedule_functions[0])
            total += score

        average = float(total) / float(len(tuning_files))
        print(average)


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'tune':
        if sys.argv[2] == 'annealing':
            tune_annealing()
        elif sys.argv[2] == 'ga':
            pass
    else:
        main()
