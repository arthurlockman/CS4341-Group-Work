import random
from bin import *
import math


class Genome():
    def __init__(self, numbers):
        self.number_list = []
        self.number_list.extend(numbers)
        _split = len(self.numbers()) // 3
        self.bin1 = Bin1(self.numbers()[0:_split])
        self.bin2 = Bin2(self.numbers()[_split:2 * _split])
        self.bin3 = Bin3(self.numbers()[2 * _split:len(self.numbers())])
        self.bin_score = self.bin1.score() + self.bin2.score() + self.bin3.score()
        self.number_count_list = {}
        for n in range(-9, 10):
            self.number_count_list[n] = self.number_list.count(n)

    def score(self):
        return self.bin_score
    
    def counts(self):
        return self.number_count_list
    
    def numbers(self):
        return self.number_list
        
    def crossover(self, other):
        """
        Crossover this genome with another, return result.
        """
        # Random split index
        split_index = random.randint(2, len(self.numbers()) - 2)
        while split_index % 2 != 0:
            split_index = random.randint(0, len(self.numbers()) - 1)
        new_genome_1 = self.numbers()[0:split_index]
        bottom_genome_1 = other.numbers()[split_index:len(other.numbers())]
        new_genome_2 = other.numbers()[0:split_index]
        bottom_genome_2 = self.numbers()[split_index:len(self.numbers())]

        # Add bottoms with duplicates removed and counts the same
        new_genome_1.extend(self.remove_duplicates(bottom_genome_1, bottom_genome_2))
        new_genome_2.extend(self.remove_duplicates(bottom_genome_2, bottom_genome_1))

        return Genome(new_genome_1), Genome(new_genome_2)
    
    def __gt__(self, other):
        return self.score() > other.score()
    
    def __lt__(self, other):
        return self.score() < other.score()
    
    def __eq__(self, other):
        return other.score() == self.score()
    
    def __str__(self):
        return 'Genome score ' + str(self.score()) + ' ' + str(self.numbers())
    
    def __repr__(self):
        return str(self)

    @staticmethod
    def count(number_list):
        number_count_list = {}
        for n in range(-9, 10):
            number_count_list[n] = number_list.count(n)
        return number_count_list

    @staticmethod
    def diff(number_list_1, number_list_2):
        """
        Get the difference between two number lists (1 - 2)
        :param number_list_1: the first list
        :param number_list_2: the second list
        :return: A dict of the differences in counts
        """
        _list = {}
        for key in number_list_1:
            _list[key] = number_list_1[key] - number_list_2[key]
        return _list

    @staticmethod
    def remaining_swaps(number_count_list):
        _sum = 0
        for key in number_count_list:
            _sum += abs(number_count_list[key])
        return _sum

    def remove_duplicates(self, bottom_1, bottom_2):
        diff_bottom_1 = self.diff(self.count(bottom_2), self.count(bottom_1))
        new_bottom_1 = []
        new_bottom_1.extend(bottom_1)
        while self.remaining_swaps(diff_bottom_1) != 0:
            first_pos = None
            first_neg_idx = None
            first_neg = None
            for key in diff_bottom_1:
                if diff_bottom_1[key] < 0 and first_neg is None:
                    first_neg = key
                    first_neg_idx = new_bottom_1.index(key)
                if diff_bottom_1[key] > 0 and first_pos is None:
                    first_pos = key
            if first_pos is not None and first_neg is not None:
                new_bottom_1[first_neg_idx] = first_pos
            diff_bottom_1 = self.diff(self.count(bottom_2), self.count(new_bottom_1))
        return new_bottom_1

# UNIT TESTS
b1 = Genome([1, 5, 1, -2, 4, 3, -7, 1, 2, 3, 4, 5, 1, 2, 2])
assert(b1.numbers() == [1, 5, 1, -2, 4, 3, -7, 1, 2, 3, 4, 5, 1, 2, 2])
assert(b1.numbers() != [1, 2, 3, 5, 4, 1, 2, 2, 1, 5, 1, -2, 4, -1, 3])
b2 = Genome([1, 2, 3, 4, 5, 1, 2, 2, 1, 5, 1, -2, -7, 4, 3])
assert(b1.numbers() != b2.numbers())
