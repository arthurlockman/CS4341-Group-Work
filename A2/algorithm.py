import threading

class Algorithm(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        print('Running...')