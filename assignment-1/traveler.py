from collections import defaultdict
inf_dict = lambda x: defaultdict(lambda: float('inf'), {x: 0})

graph = {
	'S': 'AB',
	'A': 'CDS',
	'B': 'CS',
	'C': 'ABDEF',
	'D': 'ACF',
	'E': 'CFGH',
	'F': 'CDEH',
	'G': 'E',
	'H': 'EF',
}

class node(object):
	'''
	A search tree node.
	'''
	def __init__(self, state, parent=None):
		self.state = state
		self.parent = parent

	@property
	def depth(self):
		return self.parent.depth + 1 if self.parent else 0

	def expand(self, succ_fn, avoid_cycles=False, min_depth=None):
		depth = self.depth
		for neighbor in succ_fn(self.state):
			if avoid_cycles and self.is_ancestor(neighbor):
				continue
			if min_depth and min_depth[neighbor] <= self.depth + 1:
				continue
			yield node(neighbor, parent=self)
			if min_depth:
				# important: set min depth when we add to the queue,
				#   not when we visit/expand the node. assumes that
				#   we actually do visit every node that's returned
				#   here, i.e. no post-filtering is happening...
				min_depth[neighbor] = depth + 1

	def is_ancestor(self, state):
		if state == self.state:
			return True
		elif self.parent:
			return self.parent.is_ancestor(state)
		else:
			return False

	def __repr__(self):
		s = repr(self.parent) if self.parent else ''
		return s + self.state


def bfs(init_state, succ_fn, goal_fn, avoid_cycles=False, avoid_repeats=False):
	'''
	Perform a breadth-first search.
	'''
	traversal = []
	queue = [node(init_state)]
	min_depth = inf_dict(init_state) if avoid_repeats else None
	while queue and len(traversal) < 10:
		current_node = queue.pop(0)
		traversal.append(current_node)
		if goal_fn(current_node):
			return traversal, queue
		neighbor_nodes = current_node.expand(succ_fn, avoid_cycles, min_depth)
		queue.extend(neighbor_nodes)

	return traversal, queue

def dfs(init_state, succ_fn, goal_fn, avoid_cycles=False, avoid_repeats=False):
	'''
	Perform a depth-first search.
	'''
	traversal = []
	stack = [node(init_state)]
	min_depth = inf_dict(init_state) if avoid_repeats else None
	while stack and len(traversal) < 10:
		current_node = stack.pop(-1)
		traversal.append(current_node)
		if goal_fn(current_node):
			return traversal, stack
		neighbor_nodes = current_node.expand(succ_fn, avoid_cycles, min_depth)
		stack.extend(neighbor_nodes)

	return traversal, stack

init_state = 'S'
succ_fn = lambda x: sorted(graph[x])
goal_fn = lambda x: x.state == 'G'

t, q = bfs(init_state, succ_fn, goal_fn) 
print(' -> '.join(t_.state for t_ in t))

t, q = dfs(init_state, succ_fn, goal_fn, avoid_cycles=True) 
print(' -> '.join(t_.state for t_ in t))

t, q = bfs(init_state, succ_fn, goal_fn, avoid_cycles=True)  
print(' -> '.join(t_.state for t_ in t))

t, q = bfs(init_state, succ_fn, goal_fn, avoid_repeats=True) 
print(' -> '.join(t_.state for t_ in t))
