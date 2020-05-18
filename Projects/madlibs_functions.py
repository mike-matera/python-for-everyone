"""
CIS-15 Madlibs Functions
Mike Matera
"""

import sys 

def read_madlib_file(filename):
	"""Read a madlib file."""
	with open(filename) as f:
		m = f.readline().strip()
		t1 = f.readline().strip()
		t2 = f.readline().strip()
		t3 = f.readline().strip()
	return m, t1, t2, t3 

def ask_one_word(prompt):
	"""Get a word from the user."""
	return input(prompt)

def display_madlib(madlib_complete):
	"""Display the madlib"""
	print(madlib_complete)
	with open('madlib.out', 'w') as f:
		f.write(madlib_complete)

def main():
	print(f'Opening {sys.argv[1]}')
	m, t1, t2, t3 = read_madlib_file(sys.argv[1])

	w1 = ask_one_word(f'Please enter a(n) {t1}: ')
	w2 = ask_one_word(f'Please enter a(n) {t2}: ')
	w3 = ask_one_word(f'Please enter a(n) {t3}: ')

	display_madlib(m.format(w1, w2, w3))


if __name__ == '__main__':
	main()