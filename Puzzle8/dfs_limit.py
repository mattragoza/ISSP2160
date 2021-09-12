#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:01:00 2019
vanilla breadth first search
- relies on  Puzzle8.py module

@author: milos
"""

import Puzzle8


#### ++++++++++++++++++++++++++++++++++++++++++++++++++++
#### breadth first search    


def print_stats(n_expanded, n_generated, max_queue_len, solution_len):
    print(f'# nodes expanded = {n_expanded}')
    print(f'# nodes generated = {n_generated}')
    print(f'Max queue length = {max_queue_len}')
    if solution_len is None:
        print('No solution')
    else:
        print(f'Solution path length = {solution_len}')
    print()


def check_cyclic_repeats(node):
    '''
    Check if the node's state is also in
    one of its parent nodes.
    '''
    parent = node.parent
    while parent:
        if node.state == parent.state:
            return True
        parent = parent.parent
    return False


def get_depth(node):
    '''
    Get number of ancestor nodes.
    '''
    return node.g


def check_min_depth(node, min_depth):
    '''
    Check if the node's state has been
    or WILL BE visited (i.e. in queue)
    at a shallower depth.
    '''
    if min_depth.in_hashp(node.state):
        return min_depth.get_hash_value(node.state) < get_depth(node)
    else:
        return False
        

def depth_first_search_limit(problem, limit):
    n_expanded, n_generated, max_queue_len, solution_len = 0, 0, 1, None
    queue = Puzzle8.deque([Puzzle8.TreeNode(problem, problem.initial_state)])
    min_depth = Puzzle8.HashTable()
    min_depth.add_hash(problem.initial_state, 0)
    while queue:
        curr = queue.pop()
        if curr.goalp():
            solution_path = curr.path()
            solution_len = len(solution_path)
            print_stats(n_expanded, n_generated, max_queue_len, solution_len)
            return solution_path
        elif get_depth(curr) <= limit and not check_cyclic_repeats(curr) and not check_min_depth(curr, min_depth):
            min_depth.add_hash(curr.state, get_depth(curr))
            neighbors = curr.generate_new_tree_nodes()
            n_expanded += 1
            n_generated += len(neighbors)
            queue.extend(neighbors)
            max_queue_len = max(len(queue), max_queue_len)

    print_stats(n_expanded, n_generated, max_queue_len, solution_len)
    return Puzzle8.NULL

  
problem = Puzzle8.Puzzle8Problem(Puzzle8.Example1) 
output = depth_first_search_limit(problem, limit=10)
print('Solution Example 1:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

problem = Puzzle8.Puzzle8Problem(Puzzle8.Example2) 
output = depth_first_search_limit(problem, limit=10)
print('Solution Example 2:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

problem = Puzzle8.Puzzle8Problem(Puzzle8.Example3) 
output = depth_first_search_limit(problem, limit=10)
print('Solution Example 3:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

#problem = Puzzle8.Puzzle8Problem(Puzzle8.Example4) 
#output = depth_first_search_limit(problem)
#print('Solution Example 4:')
#Puzzle8.print_path(output)

# Solution to Example 5 may take too long to calculate using vanilla bfs
#problem = Puzzle8.Puzzle8Problem(Puzzle8.Example5) 
#output = depth_first_search_limit(problem)
#print('Solution Example 5:')
#Puzzle8.print_path(output)
 
