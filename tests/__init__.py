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
		'type': bstruct.member_1(0),
		'a': bstruct.member_1(1),
		'b': bstruct.member_1(2),
		'c': bstruct.member_1(3),
		'd': bstruct.member_1(4),
	}
class jb(metaclass=bstruct.bstructmeta):
	dat = {
		'type': bstruct.member_1(0),
		'a': bstruct.member_2(1),
		'b': bstruct.member_2(3),
	}
class j(metaclass=bstruct.bstructmeta):
	dat = {
		'type': bstruct.member_1(0),
		'data': bstruct.member_binary(1),
	}
	conditional = {
		'type': {
			ord('A'): ja,
			ord('B'): jb,
		}
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


	def test_binary_a(self):
		ba = bytearray(b'\0'*50)

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
		ba = bytearray(b'\0'*50)

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
		ba = bytearray(b'\0'*20)
		ba[10] = ord('A')
		ba[11] = 0x23
		ba[12] = 0x34
		ba[13] = 0x45
		ba[14] = 0x56

		x = j(ba, 10)
		self.assertEqual(x.type.val, ord('A'))
		self.assertEqual(type(x), j)

		xx = x.condition_on('type')
		self.assertEqual(type(xx), ja)
		self.assertEqual(xx.type.val, ord('A'))
		self.assertEqual(xx.a.val, 0x23)
		self.assertEqual(xx.b.val, 0x34)
		self.assertEqual(xx.c.val, 0x45)
		self.assertEqual(xx.d.val, 0x56)

		self.assertEqual(x.type.val, ord('A'))
		self.assertEqual(type(x), j)
		self.assertEqual(x.data[0:4], b'\x23\x34\x45\x56')

		self.assertEqual(ba.hex(), '0000000000000000000041233445560000000000')



		x.type.val = ord('B')
		xx = x.condition_on('type')
		self.assertEqual(type(xx), jb)
		self.assertEqual(xx.type.val, ord('B'))
		self.assertEqual(xx.a.val, 0x3423)
		self.assertEqual(xx.b.val, 0x5645)

		self.assertEqual(x.type.val, ord('B'))
		self.assertEqual(type(x), j)
		self.assertEqual(x.data[0:4], b'\x23\x34\x45\x56')

		self.assertEqual(ba.hex(), '0000000000000000000042233445560000000000')

