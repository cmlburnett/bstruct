import bstruct
import unittest
import struct

class mybytearray(bytearray):
	"""
	Wrapper so I can print indices to see it work
	"""
	def __getitem__(self, k):
		v = super().__getitem__(k)
		#print(['get', k, v])
		return v
	def __setitem__(self, k,v):
		#print(['set', k, v])
		super().__setitem__(k,v)


class a(metaclass=bstruct.bstructmeta):
	dat = {
		'a': bstruct.member_1I(0),
		'b': bstruct.member_1I(1),
		'c': bstruct.member_1I(2),
		'd': bstruct.member_1I(3),
	}

class b(metaclass=bstruct.bstructmeta):
	dat = {
		'a': bstruct.member_2I(0),
		'b': bstruct.member_2I(2),
		'c': bstruct.member_2I(4),
		'd': bstruct.member_2I(6),
	}

class c(metaclass=bstruct.bstructmeta):
	dat = {
		'a': bstruct.member_1I(0),
		'b': bstruct.member_1I(4),
		'c': bstruct.member_1I(8),
		'd': bstruct.member_1I(12),
	}

class d(metaclass=bstruct.bstructmeta):
	dat = {
		'a': bstruct.member_8I(0),
		'b': bstruct.member_8I(8),
		'c': bstruct.member_8I(16),
		'd': bstruct.member_8I(24),
	}

class e(metaclass=bstruct.bstructmeta):
	dat = {
		'start': bstruct.member_ref(0),
		'end': bstruct.member_ref(2),
		'comment': bstruct.member_str('start', 'end'),
	}
	@staticmethod
	def lenplan(name):
		ret = 4

		ret += len(name.encode('utf8'))

		return ret

class f(metaclass=bstruct.bstructmeta):
	dat = {
		'index_names': bstruct.member_ref(0),
		'num_names': bstruct.member_2I(2),
		'names_jumptable': bstruct.member_jumptable('index_names', 'num_names', 'names'),
		'names': bstruct.member_list(e, 'names_jumptable'),
	}
	@staticmethod
	def lenplan(names):
		ret = 4

		ret += 4 * len(names)
		ret += sum([e.lenplan(_) for _ in names])

		return ret

class g(metaclass=bstruct.bstructmeta):
	dat = {
		'magic': bstruct.member_str(0,8),
	}

class h(metaclass=bstruct.bstructmeta):
	dat = {
		'raw': bstruct.member_binary(0),
	}

class i(metaclass=bstruct.bstructmeta):
	dat = {
		'recs': bstruct.member_binary_record(0, 5),
	}

class ja(metaclass=bstruct.bstructmeta):
	dat = {
		'type': bstruct.member_str(0, 1),
		'a': bstruct.member_1I(1),
		'b': bstruct.member_1I(2),
		'c': bstruct.member_1I(3),
		'd': bstruct.member_1I(4),
	}
class jb(metaclass=bstruct.bstructmeta):
	dat = {
		'type': bstruct.member_str(0, 1),
		'a': bstruct.member_2I(1),
		'b': bstruct.member_2I(3),
	}
class j(metaclass=bstruct.bstructmeta):
	dat = {
		'type': bstruct.member_str(0, 1),
		'data': bstruct.member_binary(1),
	}
	conditional = {
		'type': {
			'A': ja,
			'B': jb,
		}
	}

class k(metaclass=bstruct.bstructmeta):
	dat = {
		'type': bstruct.member_str(0, 1),
		'data': bstruct.member_substruct(10, d),
	}

class m1(metaclass=bstruct.bstructmeta):
	dat = {
		'num_arr': bstruct.member_1I(0),
		'arr': bstruct.member_1I_array(1),
	}
class m2(metaclass=bstruct.bstructmeta):
	dat = {
		'num_arr': bstruct.member_1I(0),
		'arr': bstruct.member_2I_array(1),
	}
class m3(metaclass=bstruct.bstructmeta):
	dat = {
		'num_arr': bstruct.member_1I(0),
		'arr': bstruct.member_4I_array(1),
	}
class m4(metaclass=bstruct.bstructmeta):
	dat = {
		'num_arr': bstruct.member_1I(0),
		'arr': bstruct.member_8I_array(1),
	}
class m5(metaclass=bstruct.bstructmeta):
	dat = {
		'num_arr': bstruct.member_1I(0),
		'arr': bstruct.member_4F_array(1),
	}
class m6(metaclass=bstruct.bstructmeta):
	dat = {
		'num_arr': bstruct.member_1I(0),
		'arr': bstruct.member_8F_array(1),
	}

class SimpleTests(unittest.TestCase):
	def test_1byte_a(self):
		ba = mybytearray(b'\0'*20)

		x = a(ba, 0)

		self.assertEqual(x.a.val, 0)
		self.assertEqual(x.b.val, 0)
		self.assertEqual(x.c.val, 0)
		self.assertEqual(x.d.val, 0)

		x.a.val = 10
		x.b.val = 20
		x.c.val = 30
		x.d.val = 40

		self.assertEqual(x.a.val, 10)
		self.assertEqual(x.b.val, 20)
		self.assertEqual(x.c.val, 30)
		self.assertEqual(x.d.val, 40)

		# Make sure it serializes correctly
		self.assertEqual(ba.hex(), '0a141e2800000000000000000000000000000000')

	def test_1byte_b(self):
		ba = mybytearray(b'\0'*20)

		x = a(ba, 10)

		self.assertEqual(x.a.val, 0)
		self.assertEqual(x.b.val, 0)
		self.assertEqual(x.c.val, 0)
		self.assertEqual(x.d.val, 0)

		x.a.val = 10
		x.b.val = 20
		x.c.val = 30
		x.d.val = 40

		self.assertEqual(x.a.val, 10)
		self.assertEqual(x.b.val, 20)
		self.assertEqual(x.c.val, 30)
		self.assertEqual(x.d.val, 40)

		# Make sure it serializes correctly
		self.assertEqual(ba.hex(), '000000000000000000000a141e28000000000000')


	def test_2byte_a(self):
		ba = mybytearray(b'\0'*20)

		x = b(ba, 0)

		self.assertEqual(x.a.val, 0)
		self.assertEqual(x.b.val, 0)
		self.assertEqual(x.c.val, 0)
		self.assertEqual(x.d.val, 0)

		x.a.val = 10
		x.b.val = 20
		x.c.val = 30
		x.d.val = 40

		self.assertEqual(x.a.val, 10)
		self.assertEqual(x.b.val, 20)
		self.assertEqual(x.c.val, 30)
		self.assertEqual(x.d.val, 40)

		# Make sure it serializes correctly
		self.assertEqual(ba.hex(), '0a0014001e002800000000000000000000000000')

	def test_2byte_b(self):
		ba = mybytearray(b'\0'*20)

		x = b(ba, 10)

		self.assertEqual(x.a.val, 0)
		self.assertEqual(x.b.val, 0)
		self.assertEqual(x.c.val, 0)
		self.assertEqual(x.d.val, 0)

		x.a.val = 10
		x.b.val = 20
		x.c.val = 30
		x.d.val = 40

		self.assertEqual(x.a.val, 10)
		self.assertEqual(x.b.val, 20)
		self.assertEqual(x.c.val, 30)
		self.assertEqual(x.d.val, 40)

		# Make sure it serializes correctly
		self.assertEqual(ba.hex(), '000000000000000000000a0014001e0028000000')


	def test_4byte_a(self):
		ba = mybytearray(b'\0'*20)

		x = c(ba, 0)

		self.assertEqual(x.a.val, 0)
		self.assertEqual(x.b.val, 0)
		self.assertEqual(x.c.val, 0)
		self.assertEqual(x.d.val, 0)

		x.a.val = 10
		x.b.val = 20
		x.c.val = 30
		x.d.val = 40

		self.assertEqual(x.a.val, 10)
		self.assertEqual(x.b.val, 20)
		self.assertEqual(x.c.val, 30)
		self.assertEqual(x.d.val, 40)

		# Make sure it serializes correctly
		self.assertEqual(ba.hex(), '0a000000140000001e0000002800000000000000')

	def test_4byte_b(self):
		ba = mybytearray(b'\0'*20)

		x = c(ba, 2)

		self.assertEqual(x.a.val, 0)
		self.assertEqual(x.b.val, 0)
		self.assertEqual(x.c.val, 0)
		self.assertEqual(x.d.val, 0)

		x.a.val = 10
		x.b.val = 20
		x.c.val = 30
		x.d.val = 40

		self.assertEqual(x.a.val, 10)
		self.assertEqual(x.b.val, 20)
		self.assertEqual(x.c.val, 30)
		self.assertEqual(x.d.val, 40)

		# Make sure it serializes correctly
		self.assertEqual(ba.hex(), '00000a000000140000001e000000280000000000')


	def test_str_a(self):
		ba = mybytearray(b'\0'*20)

		x = e(ba, 0)

		self.assertEqual(x.start.val, 0)
		self.assertEqual(x.end.val, 0)
		self.assertEqual(x.comment.val, "")

		x.start.val = 10
		x.end.val = 15
		x.comment.val = "hello"

		self.assertEqual(x.start.val, 10)
		self.assertEqual(x.end.val, 15)
		self.assertEqual(x.comment.val, "hello")
		self.assertEqual(ba.hex(), '0a000f0000000000000068656c6c6f0000000000')

	def test_str_b(self):
		ba = mybytearray(b'\0'*20)

		x = e(ba, 5)

		self.assertEqual(x.start.val, 0)
		self.assertEqual(x.end.val, 0)
		self.assertEqual(x.comment.val, "")

		x.start.val = 10
		x.end.val = 15
		x.comment.val = "hello"

		self.assertEqual(x.start.val, 10)
		self.assertEqual(x.end.val, 15)
		self.assertEqual(x.comment.val, "hello")
		self.assertEqual(ba.hex(), '00000000000a000f0000000000000068656c6c6f')

	def test_str_c(self):
		ba = mybytearray(b'\0'*20)

		x = g(ba, 5)

		self.assertEqual(len(x.magic.val), 8)
		self.assertEqual(x.magic.val, "\0"*8)

		x.magic.val = "fourfive"

		self.assertEqual(len(x.magic.val), 8)
		self.assertEqual(x.magic.val, "fourfive")
		self.assertEqual(ba.hex(), "0000000000666f75726669766500000000000000")


	def test_names_b(self):
		names = ['michael', 'Montgomery']

		ba = mybytearray(b'\0'*50)

		x = f(ba, 0)

		self.assertEqual(x.index_names.val, 0)
		self.assertEqual(x.num_names.val, 0)

		x.index_names.val = 5
		x.num_names.val = 2

		sz = e.lenplan(names[0])
		strt = x.names_jumptable.sizeof

		x.names_jumptable[0] = (strt, strt+sz)
		strt += sz

		sz = e.lenplan(names[1])
		x.names_jumptable[1] = (strt, strt+sz)

		x.names[0].start.val = 4
		x.names[0].end.val = 4 + len(names[0])
		x.names[0].comment.val = names[0]

		x.names[1].start.val = 4
		x.names[1].end.val = 4 + len(names[1])
		x.names[1].comment.val = names[1]



		self.assertEqual(x.index_names.val, 5)
		self.assertEqual(x.num_names.val, 2)

		# Length of jump table is 8 (4 bytes per entry, 2 entries)
		#   First name sub-struct is 4+len("michael")==11
		#   Second name sub-struct is 4+len("Montgomery")==14
		# and they are stored sequentially
		self.assertEqual(x.names_jumptable[0], (8,19))
		self.assertEqual(x.names_jumptable[1], (19,33))

		self.assertEqual(x.names[0].start.val, 4)
		self.assertEqual(x.names[0].end.val, 11)
		self.assertEqual(x.names[0].comment.val, names[0])

		self.assertEqual(x.names[1].start.val, 4)
		self.assertEqual(x.names[1].end.val, 14)
		self.assertEqual(x.names[1].comment.val, names[1])

		self.assertEqual(ba.hex(), '0500020000080013001300210004000b006d69636861656c04000e004d6f6e74676f6d657279000000000000000000000000')

	def test_names_c(self):
		names = ['michael', 'Montgomery', 'Popsicle']

		ba = mybytearray(b'\0'*75)
		x = f(ba, 10)
		x.index_names.val = 4
		x.num_names.val = 0

		self.assertEqual(x.index_names.val, 4)
		self.assertEqual(x.num_names.val, 0)
		self.assertEqual(len(x.names), 0)
		self.assertEqual(len(x.names_jumptable), 0)

		### 0 ###
		ln = e.lenplan(names[0])
		self.assertEqual(ln, 4+len(names[0]))

		idx = x.names.add(ln)
		self.assertEqual(idx, 0)
		self.assertEqual(x.num_names.val, 1)
		self.assertEqual(len(x.names), 1)
		self.assertEqual(len(x.names_jumptable), 1)

		self.assertEqual(x.names_jumptable.offset, 4)
		self.assertEqual(x.names_jumptable[0], (4, 15))

		x.names[0].start.val = 4
		x.names[0].end.val = 4 + len(names[0])
		x.names[0].comment.val = names[0].encode('ascii')

		self.assertEqual(x.names[0].start.val, 4)
		self.assertEqual(x.names[0].end.val, 11)
		self.assertEqual(x.names[0].comment.val, names[0])
		self.assertEqual(ba.hex(), '000000000000000000000400010004000f0004000b006d69636861656c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')


		### 1 ###
		ln = e.lenplan(names[1])
		self.assertEqual(ln, 4+len(names[1]))

		idx = x.names.add(ln)
		self.assertEqual(x.num_names.val, 2)
		self.assertEqual(idx, 1)

		self.assertEqual(x.names_jumptable.offset, 4)
		self.assertEqual(x.names_jumptable[0], (8, 19))
		self.assertEqual(x.names_jumptable[1], (19, 33))
		self.assertEqual(ba.hex(), '0000000000000000000004000200080013001300210004000b006d69636861656c000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

		x.names[1].start.val = 4
		x.names[1].end.val = 4 + len(names[1])
		x.names[1].comment.val = names[1].encode('ascii')

		self.assertEqual(x.names[0].start.val, 4)
		self.assertEqual(x.names[0].end.val, 4 + len(names[0]))
		self.assertEqual(x.names[0].comment.val, names[0])
		self.assertEqual(x.names[1].start.val, 4)
		self.assertEqual(x.names[1].end.val, 4 + len(names[1]))
		self.assertEqual(x.names[1].comment.val, names[1])
		self.assertEqual(ba.hex(), '0000000000000000000004000200080013001300210004000b006d69636861656c04000e004d6f6e74676f6d65727900000000000000000000000000000000000000000000000000000000')



		### 2 ###
		ln = e.lenplan(names[2])
		self.assertEqual(ln, 4+len(names[2]))

		idx = x.names.add(ln)
		self.assertEqual(x.num_names.val, 3)
		self.assertEqual(idx, 2)

		self.assertEqual(x.names_jumptable.offset, 4)
		self.assertEqual(x.names_jumptable[0], (12, 23))
		self.assertEqual(x.names_jumptable[1], (23, 37))
		self.assertEqual(x.names_jumptable[2], (37, 49))
		self.assertEqual(ba.hex(), '00000000000000000000040003000c001700170025002500310004000b006d69636861656c04000e004d6f6e74676f6d657279000000000000000000000000000000000000000000000000')

		x.names[2].start.val = 4
		x.names[2].end.val = 4 + len(names[2])
		x.names[2].comment.val = names[2].encode('ascii')

		self.assertEqual(x.names[0].start.val, 4)
		self.assertEqual(x.names[0].end.val, 4 + len(names[0]))
		self.assertEqual(x.names[0].comment.val, names[0])
		self.assertEqual(x.names[1].start.val, 4)
		self.assertEqual(x.names[1].end.val, 4 + len(names[1]))
		self.assertEqual(x.names[1].comment.val, names[1])
		self.assertEqual(x.names[2].start.val, 4)
		self.assertEqual(x.names[2].end.val, 4 + len(names[2]))
		self.assertEqual(x.names[2].comment.val, names[2])
		self.assertEqual(ba.hex(), '00000000000000000000040003000c001700170025002500310004000b006d69636861656c04000e004d6f6e74676f6d65727904000c00506f707369636c65000000000000000000000000')

	def test_names_d(self):
		"""
		Identical to test_names_c but without all the clutter as the insanity of asserts are not normally there and loops unrolled.
		Everything should be the same otherwise as a single loop to set the names.
		"""

		names = ['michael', 'Montgomery', 'Popsicle']

		ba = mybytearray(b'\0'*75)
		x = f(ba, 10)
		x.index_names.val = 4
		x.num_names.val = 0

		for i in range(len(names)):
			name = names[i]
			x.names.add(e.lenplan(name))
			x.names[i].start.val = 4
			x.names[i].end.val = 4 + len(name)
			x.names[i].comment.val = name

		self.assertEqual(ba.hex(), '00000000000000000000040003000c001700170025002500310004000b006d69636861656c04000e004d6f6e74676f6d65727904000c00506f707369636c65000000000000000000000000')

	def test_names_e(self):
		"""
		Test names with offset to fall on page boundaries.
		"""

		names = ['michael', 'Montgomery', 'Popsicle']

		# Page 0 -- zeros
		# Page 1 -- f struct and jump table
		# Page 2 -- names
		# Page 3 -- zeros
		ba = mybytearray(b'\0'*4096*4)
		x = f(ba, 4096)
		x.index_names.val = 4
		x.num_names.val = 0


		### 0 ###
		ln = e.lenplan(names[0])
		idx = x.names.add(ln, start=4096-f.lenplan([]))
		x.names[0].start.val = 4
		x.names[0].end.val = 4 + len(names[0])
		x.names[0].comment.val = names[0]

		# Pages 0 & 3 are zero
		self.assertEqual(ba[0:4096], b'\0'*4096)
		self.assertEqual(ba[4096*1:4096*1+50].hex(), '04000100fc0f0710000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		self.assertEqual(ba[4096*2:4096*2+20].hex(), '04000b006d69636861656c000000000000000000')
		self.assertEqual(ba[4096*3:], b'\0'*4096)


		### 1 ###
		ln = e.lenplan(names[1])
		idx = x.names.add(ln)
		x.names[1].start.val = 4
		x.names[1].end.val = 4 + len(names[1])
		x.names[1].comment.val = names[1]

		# Pages 0 & 3 are zero
		self.assertEqual(ba[0:4096], b'\0'*4096)
		self.assertEqual(ba[4096*1:4096*1+50].hex(), '04000200fc0f0710071015100000000000000000000000000000000000000000000000000000000000000000000000000000')
		self.assertEqual(ba[4096*2:4096*2+30].hex(), '04000b006d69636861656c04000e004d6f6e74676f6d6572790000000000')
		self.assertEqual(ba[4096*3:], b'\0'*4096)


		### 2 ###
		ln = e.lenplan(names[2])
		idx = x.names.add(ln)
		x.names[2].start.val = 4
		x.names[2].end.val = 4 + len(names[2])
		x.names[2].comment.val = names[2]

		# Pages 0 & 3 are zero
		self.assertEqual(ba[0:4096], b'\0'*4096)
		self.assertEqual(ba[4096*1:4096*1+50].hex(), '04000300fc0f0710071015101510211000000000000000000000000000000000000000000000000000000000000000000000')
		self.assertEqual(ba[4096*2:4096*2+40].hex(), '04000b006d69636861656c04000e004d6f6e74676f6d65727904000c00506f707369636c65000000')
		self.assertEqual(ba[4096*3:], b'\0'*4096)

	def test_names_f(self):
		"""
		Test names with offset and spilling over pages.
		This should work with any page size and using small pages to avoid dealing with unnecessarily large strings.
		"""

		name = 'michael'

		ba = mybytearray(b'\0'*4096)
		x = f(ba, 0)
		x.index_names.val = 4
		x.num_names.val = 0

		# Start of list is 12 bytes, page size is 12 bytes
		# With each entry of 4 bytes, a page size of 12 bytes means 3 entries can be added without having to shift list entries
		expected = []
		expected.append('04000100080013000000000004000b006d69636861656c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('040002000800130013001e0004000b006d69636861656c04000b006d69636861656c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('0400030014001f001f002a002a003500000000000000000004000b006d69636861656c04000b006d69636861656c04000b006d69636861656c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('0400040014001f001f002a002a003500350040000000000004000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('0400050014001f001f002a002a0035003500400040004b0004000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('0400060020002b002b0036003600410041004c004c00570057006200000000000000000004000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('0400070020002b002b0036003600410041004c004c0057005700620062006d000000000004000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('0400080020002b002b0036003600410041004c004c0057005700620062006d006d00780004000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('040009002c0037003700420042004d004d0058005800630063006e006e0079007900840084008f00000000000000000004000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
		expected.append('04000a002c0037003700420042004d004d0058005800630063006e006e0079007900840084008f008f009a000000000004000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c04000b006d69636861656c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

		for i in range(10):
			ln = e.lenplan(name)
			# Start at 12 bytes, and need to subtract off the length of the struct (thus the first list item starts on a page boundary of 12)
			idx = x.names.add(ln, start=12-f.lenplan([]), page=12)
			x.names[idx].start.val = 4
			x.names[idx].end.val = 4 + len(name)
			x.names[idx].comment.val = name

			self.assertEqual(ba.hex()[0:500], expected[i], "Iteration i==%d"%i)

	def test_binary_a(self):
		ba = mybytearray(b'\0'*50)

		x = h(ba, 10)

		self.assertEqual(x.raw[0], 0)
		x.raw[0] = ord(b'\xfe')
		self.assertEqual(x.raw[0], ord(b'\xfe'))

		self.assertEqual(ba.hex(), '00000000000000000000fe000000000000000000000000000000000000000000000000000000000000000000000000000000')


		self.assertEqual(x.raw[0:5], b'\xfe\0\0\0\0')
		x.raw[0:5] = 'ascii'.encode('ascii')
		self.assertEqual(x.raw[0:5], 'ascii'.encode('ascii'))

		self.assertEqual(ba.hex(), '0000000000000000000061736369690000000000000000000000000000000000000000000000000000000000000000000000')

	def test_binary_b(self):
		ba = mybytearray(b'\0'*50)

		x = i(ba, 10)

		self.assertEqual(x.recs.size, 5)

		for _ in range(8):
			self.assertEqual(x.recs[_], b'\0'*5)

		x.recs[0] = 'ascii'.encode('ascii')
		x.recs[1] = 'world'.encode('ascii')

		self.assertEqual(x.recs[0], 'ascii'.encode('ascii'))
		self.assertEqual(x.recs[1], 'world'.encode('ascii'))
		self.assertEqual(x.recs[0:2], ('ascii'.encode('ascii'), 'world'.encode('ascii')))

		self.assertEqual(ba.hex(), '000000000000000000006173636969776f726c64000000000000000000000000000000000000000000000000000000000000')


		x.recs[2:4] = ('hello'.encode('ascii'), 'flour'.encode('ascii'))
		self.assertEqual(x.recs[2], 'hello'.encode('ascii'))
		self.assertEqual(x.recs[3], 'flour'.encode('ascii'))
		self.assertEqual(x.recs[0:4], ('ascii'.encode('ascii'), 'world'.encode('ascii'), 'hello'.encode('ascii'), 'flour'.encode('ascii')))

		self.assertEqual(ba.hex(), '000000000000000000006173636969776f726c6468656c6c6f666c6f75720000000000000000000000000000000000000000')


	def test_cond_a(self):
		ba = mybytearray(b'\0'*20)
		ba[10] = ord('A')
		ba[11] = 0x23
		ba[12] = 0x34
		ba[13] = 0x45
		ba[14] = 0x56

		x = j(ba, 10)
		self.assertEqual(x.type.val, 'A')
		self.assertEqual(type(x), j)

		xx = x.condition_on('type')
		self.assertEqual(type(xx), ja)
		self.assertEqual(xx.type.val, 'A')
		self.assertEqual(xx.a.val, 0x23)
		self.assertEqual(xx.b.val, 0x34)
		self.assertEqual(xx.c.val, 0x45)
		self.assertEqual(xx.d.val, 0x56)

		self.assertEqual(x.type.val, 'A')
		self.assertEqual(type(x), j)
		self.assertEqual(x.data[0:4], b'\x23\x34\x45\x56')

		self.assertEqual(ba.hex(), '0000000000000000000041233445560000000000')



		x.type.val = 'B'
		xx = x.condition_on('type')
		self.assertEqual(type(xx), jb)
		self.assertEqual(xx.type.val, 'B')
		self.assertEqual(xx.a.val, 0x3423)
		self.assertEqual(xx.b.val, 0x5645)

		self.assertEqual(x.type.val, 'B')
		self.assertEqual(type(x), j)
		self.assertEqual(x.data[0:4], b'\x23\x34\x45\x56')

		self.assertEqual(ba.hex(), '0000000000000000000042233445560000000000')

	def test_sub_a(self):
		ba = mybytearray(b'\0'*50)

		x = k(ba, 0)
		x.type.val = 'A'
		x.data.a.val = 10
		x.data.b.val = 20
		x.data.c.val = 30
		x.data.d.val = 40

		self.assertEqual(x.type.val, 'A')
		self.assertEqual(x.data.a.val, 10)
		self.assertEqual(x.data.b.val, 20)
		self.assertEqual(x.data.c.val, 30)
		self.assertEqual(x.data.d.val, 40)

		self.assertEqual(ba.hex(), '410000000000000000000a0000000000000014000000000000001e0000000000000028000000000000000000000000000000')

	def test_array_1I(self):
		ba = mybytearray(b'\0'*20)

		x = m1(ba, 0)
		self.assertEqual(x.arr._struct_char, 'B')

		x.num_arr.val = 3
		x.arr[0] = 10
		x.arr[1] = 20
		x.arr[2] = 30

		self.assertEqual(x.num_arr.val, 3)
		self.assertEqual(x.arr[0], 10)
		self.assertEqual(x.arr[1], 20)
		self.assertEqual(x.arr[2], 30)

		self.assertEqual(ba.hex(), '030a141e00000000000000000000000000000000')
		self.assertEqual(ba.hex(), struct.pack("<BBBB", 3, 10,20,30).hex() + "00"*16)

	def test_array_2I(self):
		ba = mybytearray(b'\0'*20)

		x = m2(ba, 0)
		self.assertEqual(x.arr._struct_char, 'H')

		x.num_arr.val = 3
		x.arr[0] = 10
		x.arr[1] = 20
		x.arr[2] = 30

		self.assertEqual(x.num_arr.val, 3)
		self.assertEqual(x.arr[0], 10)
		self.assertEqual(x.arr[1], 20)
		self.assertEqual(x.arr[2], 30)

		self.assertEqual(ba.hex(), '030a0014001e0000000000000000000000000000')
		self.assertEqual(ba.hex(), struct.pack("<BHHH", 3, 10,20,30).hex() + "00"*13)

	def test_array_4I(self):
		ba = mybytearray(b'\0'*20)

		x = m3(ba, 0)
		self.assertEqual(x.arr._struct_char, 'I')

		x.num_arr.val = 3
		x.arr[0] = 10
		x.arr[1] = 20
		x.arr[2] = 30

		self.assertEqual(x.num_arr.val, 3)
		self.assertEqual(x.arr[0], 10)
		self.assertEqual(x.arr[1], 20)
		self.assertEqual(x.arr[2], 30)

		self.assertEqual(ba.hex(), '030a000000140000001e00000000000000000000')
		self.assertEqual(ba.hex(), struct.pack("<BIII", 3, 10,20,30).hex() + "00"*7)

	def test_array_8I(self):
		ba = mybytearray(b'\0'*20)

		x = m4(ba, 0)
		self.assertEqual(x.arr._struct_char, 'Q')

		x.num_arr.val = 3
		x.arr[0] = 10
		x.arr[1] = 20
		x.arr[2] = 30

		self.assertEqual(x.num_arr.val, 3)
		self.assertEqual(x.arr[0], 10)
		self.assertEqual(x.arr[1], 20)
		self.assertEqual(x.arr[2], 30)

		self.assertEqual(ba.hex(), '030a0000000000000014000000000000001e00000000000000')
		self.assertEqual(ba.hex(), struct.pack("<BQQQ", 3, 10,20,30).hex())

	def test_array_4F(self):
		ba = mybytearray(b'\0'*20)

		x = m5(ba, 0)
		self.assertEqual(x.arr._struct_char, 'f')

		vals = [1.5555000305175781, 3.140000104904175, -10.823530197143555]

		x.num_arr.val = 3
		x.arr[0] = vals[0]
		x.arr[1] = vals[1]
		x.arr[2] = vals[2]

		self.assertEqual(x.num_arr.val, 3)
		self.assertEqual(x.arr[0], vals[0])
		self.assertEqual(x.arr[1], vals[1])
		self.assertEqual(x.arr[2], vals[2])

		self.assertEqual(ba.hex(), '03a01ac73fc3f548402e2d2dc100000000000000')
		self.assertEqual(ba.hex(), struct.pack("<Bfff", 3, *vals).hex() + "00"*7)

	def test_array_8I(self):
		ba = mybytearray(b'\0'*20)

		x = m6(ba, 0)
		self.assertEqual(x.arr._struct_char, 'd')

		vals = [1.5555000305175781, 3.140000104904175, -10.823530197143555]

		x.num_arr.val = 3
		x.arr[0] = vals[0]
		x.arr[1] = vals[1]
		x.arr[2] = vals[2]

		self.assertEqual(x.num_arr.val, 3)
		self.assertEqual(x.arr[0], vals[0])
		self.assertEqual(x.arr[1], vals[1])
		self.assertEqual(x.arr[2], vals[2])

		self.assertEqual(ba.hex(), '030000000054e3f83f00000060b81e0940000000c0a5a525c0')
		self.assertEqual(ba.hex(), struct.pack("<Bddd", 3, *vals).hex())


class intervalTests(unittest.TestCase):
	def test_basic(self):
		bs = bstruct.interval(5,10)
		self.assertEqual(bs.start, 5)
		self.assertEqual(bs.stop, 10)
		self.assertEqual(bs.len, 6)
		self.assertEqual(bs.slice, slice(5,11))
		self.assertEqual(list(bs), [5,6,7,8,9,10])

		# Don't really care how hash works, but want to ensure hash(bs) succeeds
		self.assertEqual(hash(bs), hash( (bs.start, bs.stop) ))

		self.assertFalse(4 in bs)
		self.assertTrue(5 in bs)
		self.assertTrue(6 in bs)
		self.assertTrue(7 in bs)
		self.assertTrue(8 in bs)
		self.assertTrue(9 in bs)
		self.assertTrue(10 in bs)
		self.assertFalse(11 in bs)

		self.assertEqual(bs[0], 5)
		self.assertEqual(bs[1], 6)
		self.assertEqual(bs[2], 7)
		self.assertEqual(bs[3], 8)
		self.assertEqual(bs[4], 9)
		self.assertEqual(bs[5], 10)
		self.assertEqual(bs[-1], 10)
		self.assertEqual(bs[-2], 9)
		self.assertEqual(bs[-3], 8)
		self.assertEqual(bs[-4], 7)
		self.assertEqual(bs[-5], 6)
		self.assertEqual(bs[-6], 5)

		# Check that bs[6] and bs[-7] raise exception and do bs[7] and bs[-8] for good measure
		self.assertRaises(KeyError, bs.__getitem__, 6)
		self.assertRaises(KeyError, bs.__getitem__, 7)
		self.assertRaises(KeyError, bs.__getitem__, -7)
		self.assertRaises(KeyError, bs.__getitem__, -8)

	def test_null(self):
		bs = bstruct.interval(5,5)
		self.assertEqual(bs.start, 5)
		self.assertEqual(bs.stop, 5)
		self.assertEqual(bs.len, 1)
		self.assertEqual(bs.slice, slice(5,6))
		self.assertEqual(list(bs), [5])

		bs = bstruct.interval(5,6)
		self.assertEqual(bs.start, 5)
		self.assertEqual(bs.stop, 6)
		self.assertEqual(bs.len, 2)
		self.assertEqual(bs.slice, slice(5,7))
		self.assertEqual(list(bs), [5,6])

		# Invalid values
		self.assertRaises(TypeError, bstruct.interval, 0, "stop is string")
		self.assertRaises(TypeError, bstruct.interval, "start is string", 0)
		self.assertRaises(ValueError, bstruct.interval, 5, 4)

	def test_add(self):
		bs = bstruct.interval(5,10)
		bs = bs + 10

		self.assertEqual(bs.start, 15)
		self.assertEqual(bs.stop, 20)
		self.assertEqual(bs.len, 6)
		self.assertEqual(bs.slice, slice(15,21))
		self.assertEqual(list(bs), [15,16,17,18,19,20])

		self.assertFalse(14 in bs)
		self.assertTrue(15 in bs)
		self.assertTrue(16 in bs)
		self.assertTrue(17 in bs)
		self.assertTrue(18 in bs)
		self.assertTrue(19 in bs)
		self.assertTrue(20 in bs)
		self.assertFalse(21 in bs)

	def test_sub(self):
		bs = bstruct.interval(25,30)
		bs = bs - 10

		self.assertEqual(bs.start, 15)
		self.assertEqual(bs.stop, 20)
		self.assertEqual(bs.len, 6)
		self.assertEqual(bs.slice, slice(15,21))
		self.assertEqual(list(bs), [15,16,17,18,19,20])

		self.assertFalse(14 in bs)
		self.assertTrue(15 in bs)
		self.assertTrue(16 in bs)
		self.assertTrue(17 in bs)
		self.assertTrue(18 in bs)
		self.assertTrue(19 in bs)
		self.assertTrue(20 in bs)
		self.assertFalse(21 in bs)

	def test_overlap(self):
		a = bstruct.interval(15,20)

		# Could do this will loops, but better to just hard code things so its clear

		# Clearly not overlap
		self.assertFalse(a.overlaps( bstruct.interval(0,5)))
		self.assertFalse(a.overlaps( bstruct.interval(9,14)))

		# Increment ranges to test each possibility
		# - No overlap
		# - overlap ends
		# - encompass the entire range
		# - overlap other ends
		# - No overlap
		self.assertFalse(a.overlaps( bstruct.interval(10,11)))
		self.assertFalse(a.overlaps( bstruct.interval(10,12)))
		self.assertFalse(a.overlaps( bstruct.interval(10,13)))
		# stop value is in the iterated range
		# so interval(15,20) and interval(10,14) are adjacent and NOT overlapping
		self.assertFalse(a.overlaps( bstruct.interval(10,14)))
		self.assertTrue(a.overlaps( bstruct.interval(10,15)))
		self.assertTrue(a.overlaps( bstruct.interval(10,16)))
		self.assertTrue(a.overlaps( bstruct.interval(10,20)))
		self.assertTrue(a.overlaps( bstruct.interval(10,30)))
		self.assertTrue(a.overlaps( bstruct.interval(11,30)))
		self.assertTrue(a.overlaps( bstruct.interval(12,30)))
		self.assertTrue(a.overlaps( bstruct.interval(13,30)))
		self.assertTrue(a.overlaps( bstruct.interval(14,30)))
		self.assertTrue(a.overlaps( bstruct.interval(15,30)))
		self.assertTrue(a.overlaps( bstruct.interval(16,30)))
		self.assertTrue(a.overlaps( bstruct.interval(17,30)))
		self.assertTrue(a.overlaps( bstruct.interval(18,30)))
		self.assertTrue(a.overlaps( bstruct.interval(19,30)))
		self.assertTrue(a.overlaps( bstruct.interval(20,30)))
		# stop value is not actually in the iterated range
		# so interval(15,20) and interval(21,30) are adjacent and NOT overlapping
		self.assertFalse(a.overlaps( bstruct.interval(21,30)))
		self.assertFalse(a.overlaps( bstruct.interval(22,30)))
		self.assertFalse(a.overlaps( bstruct.interval(23,30)))

	def test_beforeafter(self):
		a = bstruct.interval(15,20)

		b = a.before(10)

		# Ensure immutability on @a
		self.assertEqual(a.start, 15)
		self.assertEqual(a.stop, 20)
		self.assertEqual(b.start, 10)
		self.assertEqual(b.stop, 14)
		self.assertFalse(a.overlaps(b))
		self.assertTrue(a.is_adjacent(b))

		c = a.after(25)
		# Ensure immutability on @a
		self.assertEqual(a.start, 15)
		self.assertEqual(a.stop, 20)
		self.assertEqual(c.start, 21)
		self.assertEqual(c.stop, 25)
		self.assertFalse(a.overlaps(c))
		self.assertTrue(a.is_adjacent(c))

		d = a.expand_before(10)

		# Ensure immutability on @a
		self.assertEqual(a.start, 15)
		self.assertEqual(a.stop, 20)
		self.assertEqual(d.start, 10)
		self.assertEqual(d.stop, 20)
		self.assertTrue(a.overlaps(d))
		self.assertFalse(a.is_adjacent(d))

		e = a.expand_after(25)
		# Ensure immutability on @a
		self.assertEqual(a.start, 15)
		self.assertEqual(a.stop, 20)
		self.assertEqual(e.start, 15)
		self.assertEqual(e.stop, 25)
		self.assertTrue(a.overlaps(e))
		self.assertFalse(a.is_adjacent(e))

