#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:01:00 2019
implementation of the evaluation function driven search
@author: milos
"""

import Puzzle8, heuristic2
Puzzle8.h_function = heuristic2.h_function

 #### ++++++++++++++++++++++++++++++++++++++++++++++++++++
 #### evaluation function driven search

LATEX_MODE = True


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


def check_min_cost(node, min_cost):
    '''
    Check if the node's state has been
    visited via a lower cost path.
    '''
    if min_cost.in_hashp(node.state):
        return min_cost.get_hash_value(node.state) < node.g
    else:
        return False

 
def eval_function_driven_search_repeats(problem):
    n_expanded, n_generated, max_queue_len, solution_len = 0, 0, 1, None
    queue = Puzzle8.Priority_Queue()
    root = Puzzle8.TreeNode(problem, problem.initial_state)
    queue.add_to_queue(root)
    min_cost = Puzzle8.HashTable()
    min_cost.add_hash(problem.initial_state, 0)
    while not queue.is_empty():
        curr = queue.pop_queue()
        if curr.goalp():
            solution_path = curr.path()
            solution_len = len(solution_path)
            print_stats(n_expanded, n_generated, max_queue_len, solution_len)
            return solution_path
        elif not check_min_cost(curr, min_cost):
            min_cost.add_hash(curr.state, curr.g)
            neighbors = curr.generate_new_tree_nodes()
            n_expanded += 1
            n_generated += len(neighbors)
            for n in neighbors:
                queue.add_to_queue(n)
            max_queue_len = max(len(queue.queue), max_queue_len)

    print_stats(n_expanded, n_generated, max_queue_len, solution_len)
    return Puzzle8.NULL


problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example1)
output = eval_function_driven_search_repeats(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)

problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example2)
output = eval_function_driven_search_repeats(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)

problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example3)
output = eval_function_driven_search_repeats(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)

problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example4)
output = eval_function_driven_search_repeats(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)

problem = Puzzle8.Puzzle8_Problem(Puzzle8.Example5)
output = eval_function_driven_search_repeats(problem)
if not LATEX_MODE:
    print('Solution:')
    Puzzle8.print_path(output)
