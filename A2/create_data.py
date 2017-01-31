import random
import sys

def main():
    
    filename = sys.argv[1]
    size = int(sys.argv[2])

    with open(filename, 'w') as f:

        for i in range(size):
            f.write(str(random.randint(-9, 9)) + ' ')

if __name__ == '__main__':
    main()