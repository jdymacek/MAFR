import time

class Timer:
	def __init__(self):
		self._startTime = None
		self._elapsed = None


	def start(self):
		self._startTime = time.perf_counter()
		self._elapsed = None

	def stop(self):
		if self._startTime == None:
			return None
		self._elapsed = time.perf_counter() - self._startTime
		self._startTime = None
		return self._elapsed

	def print(self):
        if self._elapsed == None:
			print(f"Total Elapsed Time: None")
		print( f"Total Elapsed Time: {self._elapsed:0.4f}s")
