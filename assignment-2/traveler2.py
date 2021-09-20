import heapq

graph = {
	'S': [('A', 3), ('D', 4)],
	'A': [('B', 4), ('D', 5), ('S', 3)],
	'B': [('A', 4), ('C', 4), ('E', 5)],
	'C': [('B', 4), ('F', 5), ('G', 3)],
	'D': [('A', 5), ('E', 2), ('S', 4)],
	'E': [('D', 2), ('B', 5), ('F', 4)],
	'F': [('C', 5), ('E', 4)],
	'G': [('C', 3)],
}

dist = {
	'S': 10,
	'A': 10,
	'B': 7,
	'C': 2,
	'D': 9,
	'E': 6,
	'F': 2,
	'G': 0,
}

class node(object):
	'''
	A search tree node.
	'''
	def __init__(self, state, eval_fn, g, h, parent=None):
		self.state = state
		self.eval_fn = eval_fn
		self.g = g # cost from start to node
		self.h = h # cost from node to goal
		self.parent = parent

	@property
	def f(self):
		return self.eval_fn(self.g, self.h)

	def expand(self, succ_fn, heur_fn):
		for neighbor, cost in succ_fn(self.state):
			g = self.g + cost
			h = heur_fn(neighbor)
			yield node(neighbor, self.eval_fn, g, h, parent=self)

	def __repr__(self):
		s = repr(self.parent) if self.parent else ''
		return s + self.state

	def __lt__(self, other):
		return (self.f, self.state) < (other.f, other.state)


def efs(init_state, succ_fn, goal_fn, heur_fn, eval_fn):
	'''
	Perform evaluation function-driven search.
	'''
	traversal = []
	queue = [node(init_state, eval_fn, 0, heur_fn(init_state))]
	while queue:
		current_node = heapq.heappop(queue)
		traversal.append(current_node)
		if goal_fn(current_node):
			return traversal, queue
		for n in current_node.expand(succ_fn, heur_fn):
			heapq.heappush(queue, n)

	return traversal, queue

init_state = 'S'
succ_fn = graph.__getitem__
goal_fn = lambda x: x.state == 'G'
heur_fn = dist.__getitem__

delim = '\\rightarrow'

t, q = efs(init_state, succ_fn, goal_fn, heur_fn, lambda g,h: g) 
print(f' {delim} '.join(t_.state for t_ in t), t[-1].g)

t, q = efs(init_state, succ_fn, goal_fn, heur_fn, lambda g,h: h) 
print(f' {delim} '.join(t_.state for t_ in t), t[-1].g)

t, q = efs(init_state, succ_fn, goal_fn, heur_fn, lambda g,h: g+h) 
print(f' {delim} '.join(t_.state for t_ in t), t[-1].g)
