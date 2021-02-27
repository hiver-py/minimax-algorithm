import time



class Stopwatch:
    def __init__(self, num_seconds):
        self.start_time = time.time()
        self.end_time = self.start_time + num_seconds
    

    def check(self):
        if time.time() > self.end_time:
            raise TimeoutError()
