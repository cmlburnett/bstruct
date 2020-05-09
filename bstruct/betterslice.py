
class betterslice:
	"""
	Native slice() is a terminal class and cannot be inherited.
	I want some more features, so this is a "better" slice.
	"""

	def __init__(self, start, stop):
		if not isinstance(start, int): raise TypeError("Start must be an integer")
		if not isinstance(stop, int): raise TypeError("Stop must be an integer")
		if start > stop: raise ValueError("Stop cannot be before start")

		self._start = start
		self._stop = stop
		self._len = stop - start
		self._slice = slice(start, stop)

	@property
	def start(self): return self._start
	@property
	def stop(self): return self._stop
	@property
	def len(self): return self._len
	@property
	def slice(self): return self._slice

	def str(self): return "<betterslice [%d,%d]>" % (self._start, self._stop)
	def __repr__(self):
		return "betterslice(%d,%d)" % (self._start, self._stop)

	def __hash__(self):
		return hash( (self._start, self._stop) )

	def __len__(self):
		return self._len

	def __contains__(self, i):
		return self._start <= i and self._stop > i

	def overlaps(self, slc):
		if self._start in slc:
			return True
		if (self._stop-1) in slc:
			return True
		return False

	def is_adjacent(self, b):
		"""
		Two are adjacent if one starts after the other stops without gaps.
		"""
		if self.stop == b.start:
			return True
		if b.stop == self.start:
			return True

		return False

	def before(self, start):
		"""Non-overlapping slice before this slice with new start point"""
		return betterslice(start, self.start)

	def after(self, stop):
		"""Non-overlapping slice after this slice with new stop point"""
		return betterslice(self.stop, stop)

	def expand_before(self, start):
		"""Expand this slice to a new start point with same stop"""
		return betterslice(start, self.stop)
	def expand_after(self, stop):
		"""Expand this slice to a new stop point with same start"""
		return betterslice(self.start, stop)

	def __getitem__(self, i):
		if i >= 0:
			if i >= self._len:
				raise KeyError("Index %d too large" % i)

			return self._start + i
		else:
			if i + self._len < 0:
				raise KeyError("Index %d too large" % i)

			return self._stop + i

	def __iter__(self):
		for i in range(self._start, self._stop):
			yield i

	def __add__(self, b):
		return betterslice(self._start+b, self._stop+b)
	def __sub__(self, b):
		return betterslice(self._start-b, self._stop-b)
