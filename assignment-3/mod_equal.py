import sys

graph = {
	't': [('v', 12)],
	'u': [('v', 3), ('w', 3)],
	'v': [('t', 12), ('u', 3)],
	'w': [('u', 3), ('z', 4)],
	'x': [('z', 3)],
	'y': [('z', 5)],
	'z': [('w', 4), ('x', 3), ('y', 5)],
}

def mod_equal(x, y, n):
	'''
	Return whether x and y have the
	same remainder when divided by n.

	In other words, return whether the
	difference between x and y is an
	integer multiple of n.
	'''
	return x % n == y % n

if __name__ == '__main__':
	x, y, n = map(int, sys.argv[1:])
	print(mod_equal(x, y, n))
