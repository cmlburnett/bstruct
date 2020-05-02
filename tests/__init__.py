import bstruct
import unittest

class a(metaclass=bstruct.bstructmeta):
	dat = {
		'a': bstruct.member_1(0),
		'b': bstruct.member_1(1),
		'c': bstruct.member_1(2),
		'd': bstruct.member_1(3),
	}

class b(metaclass=bstruct.bstructmeta):
	dat = {
		'a': bstruct.member_2(0),
		'b': bstruct.member_2(2),
		'c': bstruct.member_2(4),
		'd': bstruct.member_2(6),
	}

class c(metaclass=bstruct.bstructmeta):
	dat = {
		'a': bstruct.member_1(0),
		'b': bstruct.member_1(4),
		'c': bstruct.member_1(8),
		'd': bstruct.member_1(12),
	}

class d(metaclass=bstruct.bstructmeta):
	dat = {
		'a': bstruct.member_8(0),
		'b': bstruct.member_8(8),
		'c': bstruct.member_8(16),
		'd': bstruct.member_8(24),
	}

class e(metaclass=bstruct.bstructmeta):
	dat = {
		'start': bstruct.member_ref(0),
		'end': bstruct.member_ref(2),
		'comment': bstruct.member_str('start', 'end'),
	}

class f(metaclass=bstruct.bstructmeta):
	dat = {
		'index_names': bstruct.member_ref(0),
		'num_names': bstruct.member_2(2),
		'names_jumptable': bstruct.member_jumptable('index_names', 'num_names', 'names'),
		'names': bstruct.member_list(e, 'names_jumptable'),
	}
	@staticmethod
	def lenplan(name):
		ret = 4

		ret += len(name.encode('utf8'))

		return ret

class g(metaclass=bstruct.bstructmeta):
	dat = {
		'magic': bstruct.member_str(0,8),
	}

class SimpleTests(unittest.TestCase):
	def test_1byte_a(self):
		ba = bytearray(b'\0'*20)

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
		ba = bytearray(b'\0'*20)

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
		ba = bytearray(b'\0'*20)

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
		ba = bytearray(b'\0'*20)

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
		ba = bytearray(b'\0'*20)

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
		ba = bytearray(b'\0'*20)

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
		ba = bytearray(b'\0'*20)

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
		ba = bytearray(b'\0'*20)

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
		ba = bytearray(b'\0'*20)

		x = g(ba, 5)

		self.assertEqual(len(x.magic.val), 8)
		self.assertEqual(x.magic.val, "\0"*8)

		x.magic.val = "fourfive"

		self.assertEqual(len(x.magic.val), 8)
		self.assertEqual(x.magic.val, "fourfive")
		self.assertEqual(ba.hex(), "0000000000666f75726669766500000000000000")



	def test_names_b(self):
		names = ['michael', 'Montgomery']

		ba = bytearray(b'\0'*50)

		x = f(ba, 0)

		self.assertEqual(x.index_names.val, 0)
		self.assertEqual(x.num_names.val, 0)

		x.index_names.val = 5
		x.num_names.val = 2

		sz = f.lenplan(names[0])
		strt = x.names_jumptable.sizeof

		x.names_jumptable[0] = (strt, strt+sz)
		strt += sz

		sz = f.lenplan(names[1])
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

