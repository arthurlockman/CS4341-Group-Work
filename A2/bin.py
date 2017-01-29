
class Bin:

    def __init__(self, numbers):
        self.number_list = numbers

    def score(self):
        # Override this function
        raise

    def get_bin_size(self):
        return len(self.number_list)

    def add(self, number):
        self.number_list.append(number)
 
    def __str__(self):
        return str(self.number_list) + ': ' + str(self.score())
    
    def __repr__(self):
        return self.__str__()

    @classmethod
    def swap(cls, bin1, index1, bin2, index2):
        
        bin1_num = bin1.number_list[index1]
        bin2_num = bin2.number_list[index2]

        bin1.number_list[index1] = bin2_num
        bin2.number_list[index2] = bin1_num

class Bin1(Bin):

    def __init__(self, numbers):
        super().__init__(numbers)


    def score(self):

        # Adds even indexes, subtracts odd indexes
        tmp_list = []
        for i in range(len(self.number_list)):
            if i % 2 == 0:
                tmp_list.append(self.number_list[i])
            else:
                tmp_list.append(-1 * self.number_list[i])

        return sum(tmp_list)

class Bin2(Bin):

    def __init__(self, numbers):
        super().__init__(numbers)


    def score(self):

        score = 0
        
        for i in range(len(self.number_list) - 1):
            if self.number_list[i] == self.number_list[i+1]:
                score += 5
            elif self.number_list[i] < self.number_list[i+1]:
                score += 3
            else:
                score -= 10

        return score



class Bin3(Bin):

    primes = [2, 3, 5, 7]

    def __init__(self, numbers):
        super().__init__(numbers)


    def score(self):

        score = 0
        
        number_list_len = len(self.number_list)

        if number_list_len % 2 == 0:
            bottom_half_numbers = self.number_list[:number_list_len//2]
            top_half_numbers = self.number_list[number_list_len//2:]
        else: 
            bottom_half_numbers = self.number_list[:number_list_len//2]
            top_half_numbers = self.number_list[number_list_len//2+1:]

        # Score the bottom-haf numbers
        for number in bottom_half_numbers:
            if number < 0:
                score -= 2
            elif number in self.primes:
                score += 4
            else:
                score -= number

        # Score the top-half numbers
        for number in top_half_numbers:
            if number < 0:
                score += 2
            elif number in self.primes:
                score -= 4
            else:
                score += number

        return score



# UNIT TESTS
b1 = Bin1([1, 2, 3])
assert(b1.score() == 2)

b2 = Bin2([1, 2, 2, 1, 5])
assert(b2.score() == 1)

b3 = Bin3([1, -2, 4, 3, -7])
assert(b3.score() == -5)

b3.add(5)
assert(b3.score() == -13)

