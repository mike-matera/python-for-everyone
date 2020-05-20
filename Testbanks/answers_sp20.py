"""
CIS-15 Final 
Mike Matera
"""

import math 

def decoder_ring(f, i):
	"""The decoder ring."""
	with open(f) as fh:
		fh.seek((i-1) * 2)
		return fh.read(1)

def file_fibo(f):
	"""Do the fib"""
	with open(f) as fh:
		nums = [int(x) for x in fh]
	
	nums.insert(0, nums[0] + nums[1])
	nums = [str(x) for x in nums]

	with open(f, 'w') as fh:
		fh.write('\n'.join(nums) + "\n")

def file_sums(f):
	"""Check the file."""
	s = 0
	with open(f) as fh:
		for num in fh:
			s += float(num)
	return s > 100

def arg_reverser(a, b, c):
	"""Reverse arguments."""
	return c, b, a 

def compute_sinc(x):
	"""Compute sin(x)/x"""
	return math.sin(x) / x 

def adding_machine():
	"""The adding_machine function."""
	s = 0
	for _ in range(3):
		s += float(input())
	return s 

def triangle_area(b, h):
	"""Compute the area of a triangle.""" 
	return (b * h) / 2 

def average_list(l):
	"""Average a list."""
	return sum(l) / len(l) 

def running_sum(nums, limit):
	"""Compute the running sum."""
	sums = 0
	while True:
		sums += float(input('Give me a number:'))
		if sums >= limit:
			return sums

def list_filter(nums, limit):
	"""Filter this list."""
	output = []
	for num in nums:
		if num < limit:
			output.append(num)
	return output

def letter_count(phrase):
	"""Count the letters in the phrase."""
	rval = {}
	for letter in phrase.lower():
		if letter.isalpha():
			if letter not in rval:
				rval[letter] = 1
			else:
				rval[letter] += 1
	return rval

class Counter:
	"""A Counter Class"""

	def __init__(self, start_num):
		"""Initialize the class."""
		self.start = start_num
		self.count = start_num 

	def plus_one(self):
		"""Add one."""
		self.count += 1 

	def minus_one(self):
		"""Subtract one."""
		self.count -= 1 

	def reset_count(self):
		"""Reset"""
		self.count = self.start
