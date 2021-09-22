#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 18:32:46 2019

@author: milos
"""
import numpy as np

# a heuristic function for the 'current' state and the target state
def h_function(state, target_state):
    '''
    Compute Manhattan distance heuristic.
    '''
    assert len(state) == len(target_state) == 9
    return sum(
        manhattan_dist(i, j) for i,j in zip(
            np.argsort(state), np.argsort(target_state)
        ) if state[i] # ignore empty tile
    )


def manhattan_dist(i, j):
    '''
    Manhattan distance between two
    flat indices in a 3 x 3 array.
    '''
    assert (0 <= i < 9) and (0 <= j < 9)
    return abs(i//3 - j//3) + abs(i%3 - j%3)


if __name__ == '__main__':
    assert manhattan_dist(0, 0) == 0
    assert manhattan_dist(0, 1) == 1
    assert manhattan_dist(0, 2) == 2
    assert manhattan_dist(0, 3) == 1
    assert manhattan_dist(0, 4) == 2
    assert manhattan_dist(0, 5) == 3
    assert manhattan_dist(0, 6) == 2
    assert manhattan_dist(0, 7) == 3
    assert manhattan_dist(0, 8) == 4
    print('Done')
