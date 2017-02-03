from algorithm import *
from bin import *
from input_parser import InputParser
from multiprocessing import *


def parse_command_line_input():
    if len(sys.argv) < 4:
        print('Error: incorrect input arguments selected.')
        print()
        print('Usage: python3 main.py [optimization type] [filename] ' +
              '[time limit] [-mp]')
        print('       optimization type: hill, annealing, or ga')
        print('       filename: the input filename to read')
        print('       time limit: the time limit (in seconds) to limit ' +
              'the optimization to')
        print('       mp processes: use -mp to use multiple processes [EXPERIMENTAL]')
        exit()

    # Parsing command line input
    algorithm_type = sys.argv[1]
    filename = sys.argv[2]
    run_time = float(sys.argv[3]) * 1000

    if '-mp' in sys.argv:
        mp = True
    else:
        mp = False

    return algorithm_type, filename, run_time, mp


def main():
    (algorithm_type, filename, run_time, mp) = parse_command_line_input()

    input_array = InputParser.parse_input(filename)

    best_bin_1, best_bin_2, best_bin_3, best_score = None, None, None, None
    algorithm = None

    # Which algorithm is running? 
    if algorithm_type == 'hill':
        algorithm = run_hill
    elif algorithm_type == 'annealing':
        algorithm = run_annealing
    elif algorithm_type == 'ga':
        algorithm = run_genetic
    else:
        print('Unsupported algorithm.')
        exit()

    # Multiprocess?
    if mp:
        best_bin_1, best_bin_2, best_bin_3, best_score = multi_thread_algorithm(input_array, run_time, algorithm)
    else:
        best_bin_1, best_bin_2, best_bin_3, best_score = algorithm(input_array, run_time)

    print('Bin 1: ', best_bin_1, '\nBin 2: ', best_bin_2, '\nBin 3: ', best_bin_3, '\nBest Score:', best_score)


def multi_thread_algorithm(input_array, run_time, algorithm):
    result_queue = Queue()
    processes = []
    params = (input_array, run_time)

    for i in range(cpu_count()):
        p = Process(target=algorithm, args=params, kwargs={'result_queue': result_queue})
        processes.append(p)
        p.start()

    # Wait for processes to finish
    for p in processes:
        p.join()

    # Get the max result
    best_score = -math.inf
    while not result_queue.empty():
        bin_1, bin_2, bin_3, score = result_queue.get()
        print(score)

        if score > best_score:
            best_bin_1, best_bin_2, best_bin_3, best_score = bin_1, bin_2, bin_3, score

    return best_bin_1, best_bin_2, best_bin_3, best_score


def run_hill(input_array, run_time, result_queue=None):
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

    if result_queue is None:
        return best_bin_1, best_bin_2, best_bin_3, best_score
    else:
        result_queue.put((best_bin_1, best_bin_2, best_bin_3, best_score), block=True)


def run_annealing(input_array, run_time, t_max=10, sideways_max=100, t_schedule_fun=None, result_queue=None):
    if t_schedule_fun is None:
        # t_schedule_fun = lambda time_left, total_time, current_temp, max_temp: max_temp * (time_left / total_time)
        t_schedule_fun = lambda time_left, total_time, current_temp, max_temp: max_temp / (
            1 + 0.1 * (total_time - time_left) ** 2)
        # t_schedule_fun = lambda time_left, total_time, current_temp, max_temp: current_temp * 0.97

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

    if result_queue is None:
        return best_bin_1, best_bin_2, best_bin_3, best_score
    else:
        result_queue.put((best_bin_1, best_bin_2, best_bin_3, best_score), block=True)


def run_genetic(input_array, run_time, pop_size=10, elitism_pct=0.0, mutation_rate=0.5,
                result_queue=None, tuning=False):
    # Shuffle the input array
    shuffle(input_array)

    # Get the size of each bin. The length of input is guarenteed to be divisible by 3
    _split = len(input_array) // 3

    # Split the input array into 3 portions
    bin_1 = Bin1(input_array[0:_split])
    bin_2 = Bin2(input_array[_split:2 * _split])
    bin_3 = Bin3(input_array[2 * _split:len(input_array)])

    best_bin_1, best_bin_2, best_bin_3, best_score, _ = GeneticAlgorithm(bin_1, bin_2, bin_3, run_time,
                                                                         pop_size=pop_size,
                                                                         elitism_pct=elitism_pct,
                                                                         mutation_rate=mutation_rate,
                                                                         tuning=tuning).run()

    if result_queue is None:
        return best_bin_1, best_bin_2, best_bin_3, best_score
    else:
        result_queue.put((best_bin_1, best_bin_2, best_bin_3, best_score), block=True)


def tune_genetic():
    pop_size = [10, 100, 1000]
    elitism_percentages = [0.0, 0.1, 0.2, 0.3]
    mutation_rates = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    tuning_files = [
        'tuning_sets/tune_600_a.txt',
        'tuning_sets/tune_600_b.txt',
        'tuning_sets/tune_600_c.txt',
        'tuning_sets/tune_600_d.txt',
        'tuning_sets/tune_600_e.txt'
    ]
    print('Filename, population size, elitism percentage, mutation rate, score')
    for pop in pop_size:
        for pct in elitism_percentages:
            for mut in mutation_rates:
                for filename in tuning_files:
                    input_array = InputParser.parse_input(filename)
                    for i in range(5):
                        shuffle(input_array)
                        _, _, _, score = run_genetic(input_array, 10000, elitism_pct=pct, mutation_rate=mut,
                                                     pop_size=pop, tuning=True)
                        print(filename + ',' + str(pop) + ',' + str(pct) + ',' + str(mut) + ',' + str(score))


def tune_annealing():
    temperature_schedule_functions = [
        # Linear
        lambda time_left, total_time, current_temp, max_temp: max_temp * (time_left / total_time),
        # Inverse Quadratic
        lambda time_left, total_time, current_temp, max_temp: max_temp / (1 + 0.1 * (total_time - time_left) ** 2),
        # Geometric
        lambda time_left, total_time, current_temp, max_temp: current_temp * 0.97]

    tuning_files = [
        'tuning_sets/tune_600_a.txt',
        'tuning_sets/tune_600_b.txt',
        'tuning_sets/tune_600_c.txt',
        'tuning_sets/tune_600_d.txt',
        'tuning_sets/tune_600_e.txt'
    ]

    run_time_ms = 10000

    for temperature_schedule_function in temperature_schedule_functions:
        total = 0
        for filename in tuning_files:
            input_array = InputParser.parse_input(filename)
            _, _, _, score = run_annealing(input_array, run_time_ms, t_schedule_fun=temperature_schedule_function)
            total += score

        average = float(total) / float(len(tuning_files))
        print(average)


def test_all(testing_file):
    times = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
    print('Algorithm,Time,Score')
    input_array = InputParser.parse_input(testing_file)
    for run_time in times:
        for i in range(5):
            algorithm = run_hill
            _, _, _, score = algorithm(input_array, run_time * 1000)
            print('Hill,' + str(run_time) + ',' + str(score))
            algorithm = run_annealing
            _, _, _, score = algorithm(input_array, run_time * 1000)
            print('Annealing,' + str(run_time) + ',' + str(score))
            algorithm = run_genetic
            _, _, _, score = algorithm(input_array, run_time * 1000)
            print('Genetic,' + str(run_time) + ',' + str(score))


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'tune':
        if sys.argv[2] == 'annealing':
            tune_annealing()
        elif sys.argv[2] == 'ga':
            tune_genetic()
    elif len(sys.argv) > 1 and sys.argv[1] == 'test':
        filename = sys.argv[2]
        test_all(filename)
    else:
        main()
