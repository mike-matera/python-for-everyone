"""
CIS-15 Final 
Mike Matera
"""

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
		