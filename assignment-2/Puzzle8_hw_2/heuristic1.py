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
    Compute misplaced tile heuristic.
    '''
    assert len(state) == len(target_state)
    return sum(s != t for s,t in zip(state, target_state) if s)



if __name__ == '__main__':
    assert h_function([0,1,2], [0,1,2]) == 0
    assert h_function([1,0,2], [0,1,2]) == 1
    assert h_function([1,2,0], [0,1,2]) == 2
    assert h_function([2,1,0], [0,1,2]) == 1
    assert h_function([2,0,1], [0,1,2]) == 2
    assert h_function([0,2,1], [0,1,2]) == 2
    print('Done')
