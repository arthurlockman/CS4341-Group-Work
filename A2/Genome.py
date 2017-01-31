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

    def score(self):
        return self.bin_score
    
    def counts(self):
        number_list = {}
        for n in range(-9, 10):
            number_list[n] = numbers.count(n)
        return number_list
    
    def numbers(self):
        return self.number_list
        
    def crossover(self, other):
        """
        Crossover this genome with another, return result.
        """
        # Random split index
        split_index = random.randint(0, len(self.numbers()) - 1)
        top_genome_1 = self.numbers()[0:split_index]
        bottom_genome_1 = other.numbers()[split_index:len(other.numbers())-1]
        top_genome_2 = other.numbers()[0:split_index]
        bottom_genome_2 = self.numbers()[split_index:len(other.numbers())-1]
        new_genome_1 = top_genome_1.extend(bottom_genome_1)
        new_genome_2 = top_genome_2.extend(bottom_genome_2)
        new_genome_counts_1 = {}
        new_genome_counts_2 = {}
        for n in range(-9, 10):
            new_genome_counts_1[n] = new_genome_1.count(n)
            new_genome_counts_2[n] = new_genome_2.count(n)
        # TODO: Remove duplicate counts
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
