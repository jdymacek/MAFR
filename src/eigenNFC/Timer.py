import time

class Timer:
    def __init__(self):
        self._startTime = None
        self._elapsed = None
        self._startCPUTime = None
        self._elapsedCPU = None

    def start(self):
        self._startTime = time.perf_counter()
        self._startCPUTime = time.process_time()
        self._elapsed = None
        self._elapsedCPU = None

    def stop(self):
        if self._startTime == None:
            return None
        self._elapsed = time.perf_counter() - self._startTime
        self._elapsedCPU = time.process_time() - self.startCPUTime
        self._startCPUTime = None
        self._startTime = None
        return self._elapsed, self._elapsedCPU

    def print(self):
        if self._elapsed == None:
            print(f"Elapsed Time: None")
        print( f"Elapsed Time:\t{self._elapsed:0.4f}\t{self._elapsedCPU:0.4f}")
