#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 12:52:09 2019
Puzzle 8 problem. 
This module includes: 
     - Puzzle 8 problem definition
     - Search Tree
     - hash table implementation
     - 5 Examples of increasing complexity
@author: milos

"""
from collections import deque
from random import *


NO_MOVE = -1
NULL = -1


class Puzzle8Problem(object):
    '''
    Definition of the Puzzle 8 problem.
    '''
    initial_state = ''
    move_cost = 1
    end_state = (1,2,3,4,5,6,7,8,0) # defines goal state
    valid_moves = [
         [NO_MOVE,3,NO_MOVE,1],
		 [NO_MOVE,4,0,2],
		 [NO_MOVE,5,1,NO_MOVE],
		 [0,6,NO_MOVE,4],
		 [1,7,3,5],
		 [2,8,4,NO_MOVE],
		 [3,NO_MOVE,NO_MOVE,7],
		 [4,NO_MOVE,6,8],
		 [5,NO_MOVE,7,NO_MOVE]
     ]
    
    def __init__(self, init_state=(1,2,3,4,5,6,7,8,0)):
        self.initial_state = init_state
        
    def shuffle_state(self, k):
        pick = self.end_state
        for i in range(k):
           new = self.generate_all_neighbor_states(pick)
           pick, cost = random.sample(new, 1)[0]
           print(pick)
        return pick

    def goal_condition(self, state):
        return (state == self.end_state)
        
    def generate_all_neighbor_states(self, state):
        res = []
        zero_position = state.index(0)
        for i in range(4):
            next_position = self.valid_moves[zero_position][i]
            if next_position != NO_MOVE:
                new_state = list(state)
                # swap tile at next_position with zero_position
                new_state[zero_position], new_state[next_position] = \
                    state[next_position], state[zero_position]
                # print(new_state)
                res.append([tuple(new_state), self.move_cost])
        return res
    
    def h_function(self, state):
        return 0


class TreeNode(object):
    '''
    A node of the search tree.
    '''
    def __init__(self, problem, state, parent=0, g_value=0):
       self.problem = problem
       self.state = state
       self.parent = parent

       # values of f, g and h functions related to path
       self.g = g_value
       self.h = problem.h_function(state)
       self.f = self.g + self.h
    
    def goalp(self):
        '''
        Check if the node is a goal.
        '''
        return self.problem.goal_condition(self.state)
    
    def generate_new_tree_nodes(self):
        '''
        Generates a list of new tree nodes
        to be added to the search fringe.
        '''   
        new_neighbors = self.problem.generate_all_neighbor_states(self.state)
        res = []
        for new_state in new_neighbors:
            new_node = TreeNode(
                self.problem, new_state[0], self, self.g + new_state[1]
            )
            res.append(new_node)           
        return res
    
    def print_state(self):
        '''
        Prints the state associated with the node.
        '''
        for j in range(0, 9, 3):
            print((self.state[j], self.state[j+1], self.state[j+2]))
        print()
    
    def path(self):
        '''
        Returns a path (an ordered list of tree
        nodes) from the root to this node.
        '''
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    

class HashTable(object):
    '''
    HashTable can be used to store Puzzle 8 states.
    Use it to check for state repeats.
    '''
    def __init__(self):
        self.hash = {}
      
    def in_hashp(self, item):
        return item in self.hash
      
    def add_hash(self, item, value=0):
        self.hash[item] = value
          
    def get_hash_value(self, item):
        if item in self.hash:
            return self.hash[item]
        else:
            return -1

    def delete_hash(self):
        del self.hash
        self.hash = {}


def print_path(path):
    for node in path:
        node.print_state()


Example1 = (1,2,3,4,6,0,7,5,8)
Example2 = (2,3,0,1,5,6,4,7,8)
Example3 = (4,1,2,7,6,3,0,5,8)
Example4 = (4,1,2,7,6,3,5,8,0)
Example5 = (5,3,0,4,7,6,2,1,8)
