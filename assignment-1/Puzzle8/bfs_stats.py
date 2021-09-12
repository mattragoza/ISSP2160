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
        

def breadth_first_search_stats(problem):
    n_expanded, n_generated, max_queue_len, solution_len = 0, 0, 1, None
    queue = Puzzle8.deque([Puzzle8.TreeNode(problem, problem.initial_state)])
    while queue:
        curr = queue.popleft()
        if curr.goalp():
            solution_path = curr.path()
            solution_len = len(solution_path)
            print_stats(n_expanded, n_generated, max_queue_len, solution_len)
            return solution_path
        else:
            neighbors = curr.generate_new_tree_nodes()
            n_expanded += 1
            n_generated += len(neighbors)
            queue.extend(neighbors)
            max_queue_len = max(len(queue), max_queue_len)

    print_stats(n_expanded, n_generated, max_queue_len, solution_len)
    return Puzzle8.NULL

  
problem = Puzzle8.Puzzle8Problem(Puzzle8.Example1) 
output = breadth_first_search_stats(problem)
print('Solution Example 1:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

problem = Puzzle8.Puzzle8Problem(Puzzle8.Example2) 
output = breadth_first_search_stats(problem)
print('Solution Example 2:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

problem = Puzzle8.Puzzle8Problem(Puzzle8.Example3) 
output = breadth_first_search_stats(problem)
print('Solution Example 3:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

problem = Puzzle8.Puzzle8Problem(Puzzle8.Example4) 
output = breadth_first_search_stats(problem)
print('Solution Example 4:')
Puzzle8.print_path(output)

# Solution to Example 5 may take too long to calculate using vanilla bfs
# problem = Puzzle8.Puzzle8Problem(Puzzle8.Example5) 
# output = breadth_first_search_stats(problem)
# print('Solution Example 5:')
# Puzzle8.print_path(output)
 
