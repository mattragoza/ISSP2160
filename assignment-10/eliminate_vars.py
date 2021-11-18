from itertools import product

T = 1
F = 0
B = [1,0]

def bool_product(n):
	return product(*[B]*n)

class number(object):

	def __init__(self, value, adds=0, muls=0):
		self.value = value
		self.adds = adds
		self.muls = muls
	
	def __add__(self, other):
		if other is 0: # summation
			return number(
				value=self.value,
				adds=self.adds,
				muls=self.muls
			)
		else:
			return number(
				value=self.value + other.value,
				adds = 1 + self.adds + other.adds,
				muls = self.muls + other.muls
			)

	def __mul__(self, other):
		return number(
			value=self.value * other.value,
			adds=self.adds + other.adds,
			muls=1 + self.muls + other.muls
		)

	def __radd__(self, other):
		return self.__add__(other)

	def __rmul__(self, other):
		return self.__mul__(other)

# local conditional probabilities
P_B = {T: number(0.001), F: number(0.999)}
P_E = {T: number(0.002), F: number(0.998)}

P_A_BE = {
	T: {
		T: {T: number(0.95),  F: number(0.05) },
		F: {T: number(0.94),  F: number(0.06) }
	},
	F: {
		T: {T: number(0.29),  F: number(0.71) },
		F: {T: number(0.001), F: number(0.999)}
	}
}

P_R_E = {
	T: {T: number(0.90), F: number(0.10)},
	F: {T: number(0.05), F: number(0.95)},
}

P_J_A = {
	T: {T: number(0.9),  F: number(0.1) },
	F: {T: number(0.05), F: number(0.95)},
}

P_M_A = {
	T: {T: number(0.7),  F: number(0.3) },
	F: {T: number(0.01), F: number(0.99)},
}

# first order factors
f1 = lambda m, a: P_M_A[a][m]
f2 = lambda j, a: P_J_A[a][j]
f3 = lambda a, e: P_A_BE[1][e][a]
f4 = lambda e: P_R_E[e][0]
f5 = lambda: P_B[1]
f6 = lambda e: P_E[e]

### VARIABLE ELIMINATION = M,J,A,E

# higher order factors
t1 = lambda e: f4(e) * f6(e)
t2 = lambda: sum(t1(e) for e in B)

ans1 = f5() * t2()

### VARIABLE ELIMINATION = A,M,E,J

# higher order factors
t3 = lambda m,j,a: f1(m,a) * f2(j,a)
t4 = lambda m,j,a,e: t3(m,j,a) * f3(a,e)
t5 = lambda m,j,e: sum(t4(m,j,a,e) for a in B)
t6 = lambda j,e: sum(t5(m,j,e) for m in B)
t7 = lambda j,e: t6(j,e) * f4(e) * f6(e)
t8 = lambda j: sum(t7(j,e) for e in B)
t9 = lambda: sum(t8(j) for j in B)

ans2 = f5() * t9()
assert ans2.value == ans1.value
print(ans1.adds, ans1.muls)
print(ans2.adds, ans2.muls)

def print_table(f, sol=' '*8, sep=' & ', eol=' \\\\\n'):
	n = f.__code__.co_argcount
	for x in bool_product(n):
		s = sol + sep.join(f'{a:d}' for a in x)
		s += sep + f'{f(*x).value:f}' + eol
		print(s, end='')

print_table(t2, sep='\t', sol='', eol='\n')

x = number(1)
y = sum(
	x*sum(
		sum(
			x*x for i in B
		)*sum(
			x*sum(x for i in B)*sum(x for i in B)*x
			for i in B
		)
		for i in B
	)
	for i in B
)
print(y.adds, y.muls)
