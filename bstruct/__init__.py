"""
bstruct -- binary struct
This overlays a custom struct-like class over binary data to read/write from the binary data without an intermediate storage.
This can be used with a bytearray() or an mmap'ed file to directly modify binary data.

A class is declared using the metaclass "bstructmeta" and the class defines a dictionary named dat that defines the struct.

	import bstruct
	class foo(metaclass=bstruct.bstructmeta):
		dat = {
			'magic': bstruct.member_4(0),
			'length': bstruct.member_8(4),
		}

This creates a two-member struct that includs a 4-byte magic number and an 8-byte length number.
Use of the metaclass creates all of the properties and back-end work to manipulate the binary data.

	# Create a 20 byte null spacej
	b = bytearray(b'\0'*20)
	# Start struct at byte five
	f = foo(b, 5)

	f.magic.val = 42
	f.length.val = 2346298

	print(b.hex())

This outputs in hex:

	00000000002a0000003acd230000000000000000

Index with where struct members are found:
	00112233445566778899AABBCCDDEEFF00112233
	          | magic |   length   |

Note that 42 = 0x0000002A in little endian is 2a000000
and that 2346298 = 0x000000000023CD3A in little endian is 3acd230000000000

Member types:
	member_1				1-byte integer
	member_2				2-byte integer
	member_4				4-byte integer
	member_8				8-byte integer
	member_binary			Arbitrary binary data access as list index [] access
	member_binary_record	Arbitrary data access in blocks of binary blobs as "records"
	member_ref				Same as a 2-byte integer, but interpreted as a byte index indirect reference
	member_jumptable		Jump table list of 2-tuple of (start,end) byte indices
	member_list				List of structs with (start,end) boundaries in jumptable

To use, struct class should use metaclass bstructmeta.
This defines __init__ method, if not present in the struct class.
The class should define a dat dictionary that maps member names to member_* instances.
The metaclass generates properties for each of these members that directly accesses binary data.

Optionally, a conditional dictionary can be defined to map member values to sub-struct type that "remaps" the struct to interpret the binary data differently.
This permits a union of different structs over the same data.
No one type is "correct" and both can actively be used to read/write the data.
At this time, conditional values must be fixed values.
"""

import struct

from .betterslice import betterslice

def offslice(s, offset):
	"""
	Cannot derive from slice(), so must make a function to add ability to shift slice offset
	"""
	return slice(s.start+offset, s.stop+offset)



class member:
	""" Base class for members just to have one """
	pass

class member_binary(member):
	"""
	Plain binary access of specified length
	"""
	def __init__(self, offset):
		self._offset = offset

	def __getitem__(self, idx):
		if isinstance(idx, int):
			o = self.ins.offset + self._offset + idx
			return self.ins.fw[o]
		elif isinstance(idx, slice):
			return self.ins.fw[offslice(idx, self._offset + self.ins.offset)]
		else:
			raise NotImplementedError

	def __setitem__(self, idx, val):
		if isinstance(idx, int):
			o = self.ins.offset + self._offset + idx
			self.ins.fw[o] = val
		elif isinstance(idx, slice):
			self.ins.fw[offslice(idx, self._offset + self.ins.offset)] = val
		else:
			raise NotImplementedError


class member_binary_record(member):
	"""
	Plain binary access with specified record size.
	Access is by record index rather than bytes.
	"""
	def __init__(self, offset, size):
		self._offset = offset
		self._size = size

	@property
	def size(self): return self._size
	@size.setter
	def size(self, val): self._size = val

	def __getitem__(self, idx):
		if isinstance(idx, int):
			if idx < 0:
				raise ValueError('No end-bound on records so cannot use negative indices: %d' % idx)
			s = slice(self.ins.offset + self._offset + self.size*idx, 0)
			s = slice(s.start, s.start + self.size)
			return self.ins.fw[s]
		elif isinstance(idx, slice):
			if idx.step is None:
				return tuple([self[_] for _ in range(idx.start, idx.stop)])
			else:
				return tuple([self[_] for _ in range(idx.start, idx.stop, idx.step)])
		else:
			raise NotImplementedError

	def __setitem__(self, idx, val):
		if isinstance(idx, int):
			if idx < 0:
				raise ValueError('No end-bound on records so cannot use negative indices: %d' % idx)
			s = slice(self.ins.offset + self._offset + self.size*idx, 0)
			s = slice(s.start, s.start + self.size)
			self.ins.fw[s] = val
		elif isinstance(idx, slice):
			if idx.step is None:
				cnt = 0
				for i in range(idx.start, idx.stop):
					self[i] = val[cnt]
					cnt += 1
			else:
				cnt = 0
				for i in range(idx.start, idx.stop, idx.step):
					self[i] = val[cnt]
					cnt += 1
		else:
			raise NotImplementedError

class member_struct(member):
	"""
	Basic member that uses struct library to ser/deser binary
	"""
	@property
	def val(self):
		"""
		Gets the value from binary as an integer
		"""
		ret = struct.unpack(self.structstr, self.ins.fw[self.abs_slice])[0]
		return ret
	@val.setter
	def val(self, v):
		"""
		Sets the value from an integer to binary
		"""
		self.ins.fw[self.abs_slice] = struct.pack(self.structstr, v)

	@property
	def index(self):
		"""
		Gets the index 2-tuple of this member
		"""
		return tuple(range(self._s.stop)[self._s])

	@property
	def abs_index(self):
		"""
		Gets absolute index 2-tuple of this member
		"""
		return tuple(range(self.abs_clie.stop)[self.abs_slice])

	@property
	def slice(self):
		"""
		Gets the index of this member as a slice
		"""
		return self._s

	@property
	def abs_slice(self):
		"""
		Gets the absolute index of this member as a slice.
		"""
		return offslice(self._s, self.ins.offset)

class member_1(member_struct):
	""" One byte struct member """
	def __init__(self, offset):
		self.offset = offset
		self.len = 1
		self.structstr = "<B"
		self._s = slice(self.offset, self.offset+self.len)

class member_2(member_struct):
	""" Two byte struct member """
	def __init__(self, offset):
		self.offset = offset
		self.len = 2
		self.structstr = "<H"
		self._s = slice(self.offset, self.offset+self.len)

class member_4(member_struct):
	""" Four byte struct member """
	def __init__(self, offset):
		self.offset = offset
		self.len = 4
		self.structstr = "<I"
		self._s = slice(self.offset, self.offset+self.len)

class member_8(member_struct):
	""" Eight byte struct member """
	def __init__(self, offset):
		self.offset = offset
		self.len = 8
		self.structstr = "<Q"
		self._s = slice(self.offset, self.offset+self.len)

class member_ref(member_2):
	"""
	Reference member refers to other members of a struct.
	"""
	pass


class member_str(member):
	"""
	Mmeber that handles strings stored as UTF-8 binary.
	"""
	def __init__(self, start, end):
		self.ref_start = start
		self.ref_end = end

	@property
	def of_s(self):
		if isinstance(self.ref_start, int):
			return self.ref_start
		else:
			return getattr(self.ins, self.ref_start).val
	@property
	def of_e(self):
		if isinstance(self.ref_end, int):
			return self.ref_end
		else:
			return getattr(self.ins, self.ref_end).val

	@property
	def val(self):
		s = slice(self.of_s, self.of_e)
		return self.ins.fw[offslice(s, self.ins.offset)].decode('utf8')

	@val.setter
	def val(self, val):
		ln = self.of_e - self.of_s

		# Convert to binary if not yet
		if isinstance(val, str):
			dat = val.encode('utf8')
		elif isinstance(val, bytes):
			dat = val
		else:
			raise TypeError("Unable to copy '%s' into string" % (str(val),))

		# Make sure string is the right fit
		if len(dat) != ln:
			raise ValueError("String is %d long, space is for %d" % (len(dat), ln))

		# Copy string
		s = slice(self.of_s, self.of_e)
		self.ins.fw[offslice(s, self.ins.offset)] = dat

class member_jumptable(member):
	"""
	Jumptable member.
	This is a list of 2-byte byte index of the members in a list.
	Informatio needed is
	- member name containing the offset of the jump table
	- member name containing the length of the jump table
	- member name that is an array structs to jump to
	"""
	def __init__(self, offset_ref, ln, lst):
		"""
		@offset_ref -- member name containing the index reference to the jump table
		@ln -- member name containing the length of jump table (4 bytes per entry; 2 for start, 2 for end)
		@lst -- member name containing the list of struct entries to jump into
		"""
		self._offset_ref = offset_ref
		self._ln = ln
		self._lst = lst

	def __len__(self):
		"""
		Length of the jump table in terms of number of entries (each entry is 4 bytes)
		"""
		return getattr(self.ins, self._ln).val

	@property
	def offset(self):
		"""
		Gets the offset that this jumptable is at.
		"""
		return getattr(self.ins, self._offset_ref).val

	@property
	def sizeof(self):
		"""
		Size of the jump table in bytes. 4 bytes per entry.
		"""
		return len(self) * 4

	def __getitem__(self, idx):
		"""
		Gets the index in the jumptable of the @idx'th entry in the jump table.
		This offset returned is then used to find the sub-struct in a list following the jump table.
		This offset is relative to the start of the jump table, so absolute offset found by getting @offset value and adding to what is returned.
		"""
		ln = len(self)

		# Handle int and slice, including negative indexes
		indices = list(range(ln))[idx]

		if isinstance(indices, int):
			idx = indices
			of = self.offset
			# Make a slice object
			s = slice(of + 4*idx, of + 4*idx + 4)
			# Return the offset to jump to for the @idx entry
			return struct.unpack("<HH", self.ins.fw[offslice(s, self.ins.offset)])
		else:
			ret = []

			# Get offset start of the jump table
			of = self.offset
			for idx in indices:
				# Make a slice object
				s = slice(of + 4*idx, of + 4*idx + 4)
				# Return the offset to jump to for the @idx entry
				ret.append( struct.unpack("<HH", self.ins.fw[offslice(s, self.ins.offset)]) )

			return ret

	def __setitem__(self, idx, val):
		"""
		Sets the index in the jumptable of the @idx'th entry in the jump table.
		"""

		if isinstance(idx, int):
			pass
		else:
			raise TypeError("Must supply only an integer when setting")

		# Convert negative indices to positive
		if idx < 0:
			ln = len(self)
			idx += ln

		ln = len(self)
		if idx > ln:
			raise IndexError('Access index %d beyond jump table length %d' % (idx,ln))

		if isinstance(self._offset_ref, int):
			# Get offset start of the jump table
			of = self._offset_ref
		elif isinstance(self._offset_ref, str):
			# Get offset start of the jump table
			of = getattr(self.ins, self._offset_ref).val
		else:
			raise TypeError("Unknown type '%s'" % type(self._offset_ref))

		# Make a slice object
		s = slice(of + 4*idx, of + 4*idx + 4)
		# Update the jump table entry with the offset @val
		self.ins.fw[offslice(s, self.ins.offset)] = struct.pack("<HH", *val)


class member_list(member):
	"""
	Member is a list of entries of the specified item class, managed by a jump table.
	"""
	def __init__(self, itemcls, jumptable_ref):
		"""
		@itemcls -- Struct class to invoke to manage an individual item in the list.
		@jumptable_ref -- Jump table that manages the list
		"""
		self._itemcls = itemcls
		self._jumptable_ref = jumptable_ref


	def __getitem__(self, idx):
		"""
		Get the @idx'th item as an instance of the sub-struct class.
		"""
		if isinstance(idx, int):
			pass
		elif isinstance(idx, slice):
			return [self[i] for i in range(idx.start, idx.stop)]
		else:
			raise TypeError("Must supply only an integer when setting")

		# Access the jump table and get the index
		jt = getattr(self.ins, self._jumptable_ref)

		# Handle negative indexes
		if idx < 0:
			idx += len(jt)
		off = jt[idx]

		# offset for the class requires knowing the offset of the parent struct
		# the offset of the jump table within the struct, and the offset
		# within the jump table (hence 3 terms due to relativity of offsets)
		return self._itemcls(self.ins.fw, self.ins.offset + jt.offset + off[0])

	# NB: set is not supported, use the struct class to update the list item

class bstructmeta(type):
	"""
	Metaclass to handle programmatically creating properties of the struct.
	Seems more appropriate to do this as a metaclass than with either inheritance
	 or boilerplate copy/paste for each struct class.
	"""

	class fancyprop:
		"""
		Property that passes instance of object to the struct (cannot do this at
		declare time for the class).
		"""

		def __init__(self, s):
			self._s = s

		def __get__(self, ins, own=None):
			""" Pass attribute access to the struct """
			self._s.ins = ins
			return self._s

		def __set__(self, ins, val):
			""" probably common to forget .val to access the struct member property """
			raise Exception("Cannot set this property, access using .val")

	def __new__(cls, name, bases, dct):
		# Create an initializer to avoid copy/pasting this unless already created
		# Avoids copy/paste of this boilerplate
		if '__init__' not in dct:
			def _init(self,fw,offset):
				self.fw = fw
				self.offset = offset
			dct['__init__'] = _init

		# If a conditional dictionary exists and a condition_on function is not defined, then define one
		if 'condition_on' not in dct and 'conditional' in dct:
			def _condition_on(self, mname):
				# Get dictionary that maps member names to values
				cd = dct['conditional']
				# Member name needs to be in the dictionary
				if mname in cd:
					# Get the value in struct
					val = getattr(self, mname).val
					# Search for value in the dictionary
					# TODO: expand ability here beyond fixed values
					if val in dct['conditional'][mname]:
						# Get sub-struct class and instantiate at same offset
						subcls = dct['conditional'][mname][val]
						return subcls(self.fw, self.offset)
					else:
						raise ValueError("Conditional on member '%s' has value '%s' that is not in the conditional list" % (mname,val))
				else:
					raise KeyError("No conditional for member '%s'" % (mname,))

			dct['condition_on'] = _condition_on

		if 'dat' not in dct:
			raise TypeError("Class '%s' does not have a 'dat' item listing members" % (str(cls),))

		# Iterate over struct members and create properties
		for k,v in dct['dat'].items():
			dct[k] = bstructmeta.fancyprop(v)

		# Create class
		return super().__new__(cls,name,bases,dct)

