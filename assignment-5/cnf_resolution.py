
class cnf_symbol(object):
	def __init__(self, term, not_):
		self.term = term
		self.not_ = not_
	def __invert__(self):
		return cnf_symbol(self.term, not_=not self.not_)
	def __eq__(self, other):
		return self.term == other.term and self.not_ == other.not_
	def __repr__(self):
		return ('', '\\neg ')[self.not_] + self.term
	def __hash__(self):
		return hash((self.term, self.not_))

class cnf_node(object):
	def __init__(self, term1, term2):
		self.term1 = term1
		self.term2 = term2

	@classmethod
	def from_str(self, s):
		term1, term2 = s.split(' v ')
		if term1[0] == '!':
			term1 = cnf_symbol(term1[1:], not_=True)
		else:
			term1 = cnf_symbol(term1, not_=False)
		if term2[0] == '!':
			term2 = cnf_symbol(term2[1:], not_=True)
		else:
			term2 = cnf_symbol(term2, not_=False)
		return cnf_node(term1, term2)

	def __repr__(self):
		return f'${self.term1} \\lor {self.term2}$'

	def __add__(self, other):
		if self.term1 == ~other.term1:
			return cnf_node(self.term2, other.term2)
		elif self.term1 == ~other.term2:
			return cnf_node(self.term2, other.term1)
		elif self.term2 == ~other.term1:
			return cnf_node(self.term1, other.term2)
		elif self.term2 == ~other.term2:
			return cnf_node(self.term1, other.term1)
		else:
			raise ValueError('cannot resolve nodes')

	def __eq__(self, other):
		return (
			self.term1 == other.term1 and self.term2 == other.term2
		) or (
			self.term1 == other.term2 and self.term2 == other.term1
		)

	def __hash__(self):
		return hash(self.term1) + hash(self.term2)

KB = [
	cnf_node.from_str('!Y v !O'),
	cnf_node.from_str('Y v O'),
	cnf_node.from_str('Y v M'),
	cnf_node.from_str('O v H'),
	cnf_node.from_str('!M v H'),
	cnf_node.from_str('!H v G')
]
known = set(KB)
assert cnf_node.from_str('!Y v !O') in known

start_line =14
for i, n in enumerate(KB):
	print(
		f'\\item {n}\n\\hfill (And-elimination, from {start_line})')

i = 0
while i < len(KB):
	node_i = KB[i]
	for j in range(i, len(KB)):
		node_j = KB[j]
		try:
			new_node = node_i + node_j
			if new_node not in known:
				KB.append(new_node)
				known.add(new_node)
				print(f'\\item {new_node}\n\\hfill (Resolution, from {start_line+i+1}, {start_line+j+1})')
		except ValueError:
			pass
		try:
			new_node = node_j + node_i
			if new_node not in known:
				KB.append(new_node)
				known.add(new_node)
				print(f'\\item {new_node}\n\\hfill (Resolution, from {start_line+i+1}, {start_line+j+1})')
		except ValueError:
			pass

	i += 1
