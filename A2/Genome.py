class Genome():
    def __init__(self, bin1, bin2, bin3):
        self.bin1 = bin1
        self.bin2 = bin2
        self.bin3 = bin3
        self.bin_score = self.bin1.score() + self.bin2.score() + self.bin3.score()
        
    def score(self):
        return self.bin_score
    
    def counts(self):
        number_list = {}
        for n in range(-9, 10):
            number_list[n] = numbers.count(n)
        return number_list
    
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
