import random
from bin import *

class Genome():
    def __init__(self, numbers):
        self.number_list = numbers
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
        print(split_index)
        new_genome_1 = self.numbers()[0:split_index]
        bottom_genome_1 = other.numbers()[split_index:len(other.numbers())-1]
        new_genome_2 = other.numbers()[0:split_index]
        bottom_genome_2 = self.numbers()[split_index:len(self.numbers())-1]
        new_genome_1.extend(bottom_genome_1)
        new_genome_2.extend(bottom_genome_2)
        print('Genomes Equal: ', bottom_genome_1 == bottom_genome_2)
        _n1 = Genome(new_genome_1)
        _n2 = Genome(new_genome_2)
        # TODO: Remove duplicate counts
        new_genome_1_mismatch = {}
        new_genome_2_mismatch = {}
        for key in _n1.counts():
            new_genome_1_mismatch[key] = 0
            new_genome_2_mismatch[key] = 0
            if _n1.counts()[key] != self.counts()[key]:
                new_genome_1_mismatch[key] = new_genome_1_mismatch[key] + 1
                print('g1 mismatch ', key, _n1)
            if _n2.counts()[key] != other.counts()[key]:
                new_genome_2_mismatch[key] = new_genome_2_mismatch[key] + 1
                print('g2 mismatch ', key, _n2)
        return Genome(new_genome_1), Genome(new_genome_2)
    
    def __gt__(self, other):
        return self.score() > other.score()
    
    def __lt__(self, other):
        return self.score() < other.score()
    
    def __eq__(self, other):
        return other.score() == self.score()
    
    def __str__(self):
        return 'Genome score ' + str(self.score())
    
    def __repr__(self):
         return str(self)
