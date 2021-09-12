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
        

def breadth_first_search(problem):
    queue = Puzzle8.deque([Puzzle8.TreeNode(problem, problem.initial_state)])
    while queue:
        curr = queue.popleft()
        if curr.goalp():
            return curr.path()
        else:
            queue.extend(curr.generate_new_tree_nodes())         
    print('No solution')
    return NULL

  
problem = Puzzle8.Puzzle8Problem(Puzzle8.Example1) 
output = breadth_first_search(problem)
print('Solution Example 1:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

problem = Puzzle8.Puzzle8Problem(Puzzle8.Example2) 
output = breadth_first_search(problem)
print('Solution Example 2:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

problem = Puzzle8.Puzzle8Problem(Puzzle8.Example3) 
output = breadth_first_search(problem)
print('Solution Example 3:')
Puzzle8.print_path(output)

wait = input("PRESS ENTER TO CONTINUE.")

problem = Puzzle8.Puzzle8Problem(Puzzle8.Example4) 
output = breadth_first_search(problem)
print('Solution Example 4:')
Puzzle8.print_path(output)

# Solution to Example 5 may take too long to calculate using vanilla bfs
# problem = Puzzle8.Puzzle8Problem(Puzzle8.Example5) 
# output = breadth_first_search(problem)
# print('Solution Example 5:')
# Puzzle8.print_path(output)
 
