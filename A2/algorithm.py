import threading
import time
from bin import *
import random

# Lambda function for current time in millis
current_milli_time = lambda: int(round(time.time() * 1000))

class Algorithm():

    def __init__(self, bin1, bin2, bin3, running_time_seconds):
        self.bin1 = bin1
        self.bin2 = bin2
        self.bin3 = bin3
        self.running_time_seconds = running_time_seconds
        self.bin_size = bin1.get_bin_size()

class Hill(Algorithm):

    def __init__(self, bin1, bin2, bin3, running_time_seconds):
        super().__init__(bin1, bin2, bin3, running_time_seconds)


    def run(self):
        
        end_time = current_milli_time() + self.running_time_seconds * 1000

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


            # If found swap, swap
            if best_score != start_score:
                Bin.swap(*best_swap)
                print(best_score)

            # Else terminate and restart
            else:
                return best_score

        return best_score




