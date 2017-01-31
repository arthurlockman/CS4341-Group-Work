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
        top_genome = self.numbers()[0:split_index]
        bottom_genome = other.numbers()[split_index:len(other.numbers())-1]
        new_genome = top_genome.extend(bottom_genome)
        new_genome_counts = {}
        for n in range(-9, 10):
            new_genome_counts[n] = new_genome.count(n)
        # TODO: Remove duplicate counts
        return Genome(new_genome)
    
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
