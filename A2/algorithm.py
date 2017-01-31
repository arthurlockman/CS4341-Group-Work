import time
from bin import *
import random
from random import shuffle
import itertools, sys
from genome import *


# Function for current time in millis
def current_milli_time():
    return int(round(time.time() * 1000))


spinner = itertools.cycle(['\\', '|', '/', '-'])


def spin():
    if current_milli_time() - spin.last_spin > 100:
        sys.stdout.write(next(spinner) + ' Working...')
        sys.stdout.flush()
        sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b\b')
        spin.last_spin = current_milli_time()

spin.last_spin = current_milli_time()


class Algorithm():
    def __init__(self, bin1, bin2, bin3, running_time_ms):
        self.bin1 = bin1
        self.bin2 = bin2
        self.bin3 = bin3
        self.running_time_ms = running_time_ms
        self.bin_size = bin1.get_bin_size()


class Hill(Algorithm):
    def __init__(self, bin1, bin2, bin3, running_time_ms):
        super().__init__(bin1, bin2, bin3, running_time_ms)

    def run(self):

        end_time = current_milli_time() + self.running_time_ms
        best_score = None
        while current_milli_time() < end_time:

            start_score = self.bin1.score() + self.bin2.score() + self.bin3.score()
            best_score = self.bin1.score() + self.bin2.score() + self.bin3.score()
            best_swap = None
            for i in range(100):

                # Choose two randome bins to swap numbers
                bins = [self.bin1, self.bin1, self.bin2, self.bin2, self.bin3, self.bin3]
                random.shuffle(bins)
                bin_a, bin_b = bins[0], bins[1]

                # Choose two indexes to swap
                a, b = random.randint(0, self.bin_size - 1), random.randint(0, self.bin_size - 1)

                # Swap the numbers and evaluate the score
                Bin.swap(bin_a, a, bin_b, b)
                score = self.bin1.score() + self.bin2.score() + self.bin3.score()

                # Unswap the numbers
                Bin.swap(bin_a, a, bin_b, b)

                # Is the score max?
                if score > best_score:
                    best_score = score
                    best_swap = (bin_a, a, bin_b, b)

                spin()  # Give some indication of progress

            # If found swap, swap
            if best_score != start_score:
                Bin.swap(*best_swap)

            # Else terminate and restart
            else:
                return self.bin1, self.bin2, self.bin3, best_score, end_time - current_milli_time()

        return self.bin1, self.bin2, self.bin3, best_score, 0


class Annealing(Algorithm):
    def __init__(self, bin1, bin2, bin3, running_time_ms, t_max=10, sideways_max=100, t_schedule_fun=lambda max_temp, time_left, total_time: max_temp * (time_left / total_time)):
        super().__init__(bin1, bin2, bin3, running_time_ms)
        self.t_max = t_max
        self.max_sideways_moves = sideways_max
        self.t_schedule_fun = t_schedule_fun

    def run(self):

        end_time = current_milli_time() + self.running_time_ms
        best_score = None
        sideways_move_count = 0
        while current_milli_time() < end_time:

            start_score = self.bin1.score() + self.bin2.score() + self.bin3.score()
            best_score = self.bin1.score() + self.bin2.score() + self.bin3.score()

            # Choose two random bins to swap numbers
            bins = [self.bin1, self.bin1, self.bin2, self.bin2, self.bin3, self.bin3]
            random.shuffle(bins)
            bin_a, bin_b = bins[0], bins[1]

            # Choose two indexes to swap
            a, b = random.randint(0, self.bin_size - 1), random.randint(0, self.bin_size - 1)

            # Swap the numbers and evaluate the score
            Bin.swap(bin_a, a, bin_b, b)
            score = self.bin1.score() + self.bin2.score() + self.bin3.score()

            # Unswap the numbers
            Bin.swap(bin_a, a, bin_b, b)

            # Modify the temperature
            temperature = self.t_schedule_fun(float(end_time - current_milli_time()), self.t_max, self.running_time_ms)

            # Is this the new state to select?
            if self.p_func(score, best_score, temperature) >= random.random():
                if best_score == score:
                    sideways_move_count += 1
                else:
                    sideways_move_count = 0
                best_score = score
                Bin.swap(bin_a, a, bin_b, b)

            # Restarts based on if enough of the previous moves had the same score (5)
            if sideways_move_count >= self.max_sideways_moves:
                return self.bin1, self.bin2, self.bin3, best_score, end_time - current_milli_time()

            spin()  # Give some indication of progress

        return self.bin1, self.bin2, self.bin3, best_score, 0

    @staticmethod
    def p_func(current_score, new_score, temperature):
        if temperature == 0:
            return 0
        try:
            return math.exp(-(max(0, new_score - current_score)) / temperature)
        except OverflowError:
            return math.inf

class GeneticAlgorithm(Algorithm):
    def __init__(self, bin1, bin2, bin3, running_time_seconds, pop_size=100, elitism_pct=0.3):
        super().__init__(bin1, bin2, bin3, running_time_seconds)
        self.population_size = pop_size
        self.elitism_percentage = elitism_pct
    
    def run(self):
        numbers = []
        numbers.extend(self.bin1.number_list)
        numbers.extend(self.bin2.number_list)
        numbers.extend(self.bin3.number_list)
        # Initial step: generate n genomes
        genomes = []
        for i in range(0, self.population_size):
            shuffle(numbers)
            new_genome = Genome(numbers)
            # Append the new genome to the population (bin1, bin2, bin3, counts, score)
            genomes.append(new_genome)
        genomes.sort(reverse=True)
        print(genomes)

