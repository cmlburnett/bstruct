
class interval:
	"""
	Native slice() is a terminal class and cannot be inherited.
	I want some more features, so this is a "better" slice.

	Functions slighly different from ranges and slices where as the end is not included.
	In an interval, the stop index is included in the range.
	So in Python, foo[0:3] gets you indices 0, 1, and 2.
	With interval, interval(0,3) gets you 0, 1, 2, and 3.
	"""

	def __init__(self, start, stop):
		if not isinstance(start, int): raise TypeError("Start must be an integer")
		if not isinstance(stop, int): raise TypeError("Stop must be an integer")
		if start > stop: raise ValueError("Stop cannot be before start")

		self._start = start
		self._stop = stop
		self._len = stop - start + 1
		self._slice = slice(start, stop+1)

	@property
	def start(self): return self._start
	@property
	def stop(self): return self._stop
	@property
	def len(self): return self._len
	@property
	def slice(self): return self._slice

	def str(self): return "<interval [%d,%d]>" % (self._start, self._stop)
	def __repr__(self):
		return "interval(%d,%d)" % (self._start, self._stop)

	def __hash__(self):
		return hash( (self._start, self._stop) )

	def __len__(self):
		return self._len

	def __contains__(self, i):
		return self._start <= i and self._stop >= i

	def overlaps(self, slc):
		if self._start in slc:
			return True
		if self._stop in slc:
			return True
		return False

	def is_adjacent(self, b):
		"""
		Two are adjacent if one starts after the other stops without gaps.
		"""
		if self.stop+1 == b.start:
			return True
		if b.stop+1 == self.start:
			return True

		return False

	def before(self, start):
		"""Non-overlapping interval before this with new start point"""
		return interval(start, self.start-1)

	def after(self, stop):
		"""Non-overlapping interval after this with new stop point"""
		return interval(self.stop+1, stop)

	def expand_before(self, start):
		"""Expand this interval to a new start point with same stop"""
		return interval(start, self.stop)
	def expand_after(self, stop):
		"""Expand this interval to a new stop point with same start"""
		return interval(self.start, stop)

	def shift(self, val):
		"""
		Shift the interval by adding/subtracting @val from the start and stop
		Can be done using binary operators + and -, but this is done as a function call, which can be easier some times.
		"""
		return interval(self._start+val, self._stop+val)

	def __getitem__(self, i):
		if i >= 0:
			if i >= self._len:
				raise KeyError("Index %d too large" % i)

			return self._start + i
		else:
			if i + self._len < 0:
				raise KeyError("Index %d too large" % i)

			return self._stop + 1 + i

	def __iter__(self):
		for i in range(self._start, self._stop+1):
			yield i

	def __add__(self, val):
		return self.shift(val)
	def __sub__(self, val):
		return self.shift(-val)

