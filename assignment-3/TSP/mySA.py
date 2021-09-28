import math
import TSP, SA
from SA import linear_cooling


def cosine_cooling(i, k):
    '''
    Return a cosine-modulated linear
    cooling coefficient for simulation 
    step i out of k.
    '''
    return (k - i)/k * (1 + math.cos(math.pi*i)/2)


def power_cooling(i, k, b=0.01):
    '''
    Return an exponential cooling
    coefficient for simulation step
    i out of k.
    '''
    return b**(i/k)


def step_cooling(i, k, b=0.5, n=5):
    '''
    Return an step-wise cooling
    coefficient for simulation step
    i out of k.
    '''
    return b**math.floor(n*i/k)


if __name__ == '__main__':
    tsp_problem = TSP.TSP_Problem(TSP.Standard_Cities)

    n_trials = 10
    mean_dist = 0
    for i in range(n_trials):
        (
            init_tour,
            init_dist,
            best_tour,
            best_dist,
            n_tours_tried,
            n_tours_accepted
        ) = SA.sim_anneal(
            tsp_problem, 20000, 100, linear_cooling, verbose=False
        )
        mean_dist += best_dist/n_trials

    print(f'mean_dist = {mean_dist:.2f}')
