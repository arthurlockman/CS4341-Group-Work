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
        split_index = random.randint(0, len(self.numbers()) - 1)
        new_genome_1 = self.numbers()[0:split_index]
        bottom_genome_1 = other.numbers()[split_index:len(other.numbers())]
        new_genome_2 = other.numbers()[0:split_index]
        bottom_genome_2 = self.numbers()[split_index:len(self.numbers())]
        new_genome_1.extend(bottom_genome_1)
        new_genome_2.extend(bottom_genome_2)
        _n1 = Genome(new_genome_1)
        _n2 = Genome(new_genome_2)
        # TODO: Remove duplicate counts
        new_genome_1_mismatch = {}
        new_genome_2_mismatch = {}
        for key in _n1.counts():
            if _n2.counts()[key] - other.counts()[key] != 0:
                new_genome_2_mismatch[key] = _n2.counts()[key] - other.counts()[key]
            if _n1.counts()[key] - self.counts()[key]:
                new_genome_1_mismatch[key] = _n1.counts()[key] - self.counts()[key]
        while len(new_genome_1_mismatch) > 0:
            _idx = 1
            _keys1 = list(new_genome_1_mismatch.keys())
            key1 = _keys1[0]
            key2 = _keys1[1]
            count1 = new_genome_1_mismatch[_keys1[0]]
            count2 = new_genome_1_mismatch[_keys1[_idx]]
            while count1 / math.fabs(count1) == count2 / math.fabs(count2):
                _idx += 1
                count2 = new_genome_1_mismatch[_keys1[_idx]]
                key2 = _keys1[_idx]
            if count1 < 0:
                new_genome_1[new_genome_1.index(key2)] = key1
            else:
                new_genome_1[new_genome_1.index(key1)] = key2
            _n1 = Genome(new_genome_1)
            for key in _n1.counts():
                if _n1.counts()[key] - self.counts()[key]:
                    new_genome_1_mismatch[key] = _n1.counts()[key] - self.counts()[key]
        while len(new_genome_2_mismatch) > 0:
            _idx = 1
            _keys1 = list(new_genome_2_mismatch.keys())
            key1 = _keys1[0]
            key2 = _keys1[1]
            count1 = new_genome_2_mismatch[_keys1[0]]
            count2 = new_genome_2_mismatch[_keys1[_idx]]
            while count1 / math.fabs(count1) == count2 / math.fabs(count2):
                _idx += 1
                count2 = new_genome_2_mismatch[_keys1[_idx]]
                key2 = _keys1[_idx]
            if count1 < 0:
                new_genome_2[new_genome_2.index(key2)] = key1
            else:
                new_genome_2[new_genome_2.index(key1)] = key2
            _n2 = Genome(new_genome_2)
            for key in _n2.counts():
                if _n2.counts()[key] - other.counts()[key]:
                    new_genome_2_mismatch[key] = _n2.counts()[key] - other.counts()[key]
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
 
 # UNIT TESTS
b1 = Genome([1, 2, 3, 4, 5, 1, 2, 2, 1, 5, 1, -2, 4, 3, -7])
assert(b1.score() == -1)
assert(b1.numbers() == [1, 2, 3, 4, 5, 1, 2, 2, 1, 5, 1, -2, 4, 3, -7])
assert(b1.numbers() != [1, 2, 3, 5, 4, 1, 2, 2, 1, 5, 1, -2, 4, -1, 3])
b2 = Genome([1, 2, 3, 4, 5, 1, 2, 2, 1, 5, 1, -2, -7, 4, 3])
assert(b1.numbers() != b2.numbers())

