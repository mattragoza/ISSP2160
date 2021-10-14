#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:01:00 2019
implementation of the evaluation function driven search
@author: milos
"""

import Puzzle8

 #### ++++++++++++++++++++++++++++++++++++++++++++++++++++
 #### evaluation function driven search

LATEX_MODE = False


def print_stats(n_expanded, n_generated, max_queue_len, solution_len):
    if LATEX_MODE:
        import os
        name = os.path.basename(__file__)
        print(f'\\texttt{{{name}}} & {n_expanded} & {n_generated} & {max_queue_len} & {solution_len} \\\\')
    else:
        print(f'# nodes expanded = {n_expanded}')
        print(f'# nodes generated = {n_generated}')
        print(f'Max queue length = {max_queue_len}')
        if solution_len is None:
            print('No solution')
        else:
            print(f'Solution path length = {solution_len}')
        print()

 
def eval_function_driven_search(problem):
    n_expanded, n_generated, max_queue_len, solution_len = 0, 0, 1, None
    queue = Puzzle8.Priority_Queue()
    root = Puzzle8.TreeNode(problem, problem.initial_state)
    queue.add_to_queue(root)   
    while not queue.is_empty():
        curr = queue.pop_queue()
        if curr.goalp():
            solution_path = curr.path()
            solution_len = len(solution_path)
            print_stats(n_expanded, n_generated, max_queue_len, solution_len)
            return solution_path
        else:
            neighbors = curr.generate_new_tree_nodes()
            n_expanded += 1
            n_generated += len(neighbors)
            for n in neighbors:
                queue.add_to_queue(n)
            max_queue_len = max(len(queue.queue), max_queue_len)

    print_stats(n_expanded, n_generated, max_queue_len, solution_len)
    return Puzzle8.NULL


problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example1)
output = eval_function_driven_search(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)

problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example2)
output = eval_function_driven_search(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)

problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example3)
output = eval_function_driven_search(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)

problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example4)
output = eval_function_driven_search(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)

problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example5)
output = eval_function_driven_search(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)
