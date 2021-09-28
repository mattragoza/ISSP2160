import sys, argparse, math
import TSP, SA
from SA import linear_cooling


def cosine_cooling(i, k, f=1):
    '''
    Return a cosine-modulated linear
    cooling coefficient for simulation 
    step i out of k.
    '''
    return (k - i)/k * (1 + math.cos(math.pi*i*f)/2)


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


cooling_fn_map = {
    'linear': linear_cooling,
    'cosine': cosine_cooling,
    'power': power_cooling,
    'step': step_cooling,
}


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_trials', type=int, default=10)
    parser.add_argument('--n_steps', type=int, default=20000)
    parser.add_argument('--init_temp', type=int, default=100)
    parser.add_argument('--cooling_fn', default='linear')
    parser.add_argument('--cooling_base', type=float, default=0.01)
    parser.add_argument('--no_agg', default=False, action='store_true')
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    tsp_problem = TSP.TSP_Problem(TSP.Standard_Cities)

    n_trials = args.n_trials
    best_dists = []
    for i in range(n_trials):
        (
            init_tour,
            init_dist,
            best_tour,
            best_dist,
            n_tours_tried,
            n_tours_accepted
        ) = SA.sim_anneal(
            tsp_problem,
            no_of_steps=args.n_steps,
            init_temperature=args.init_temp,
            cooling_fn=cooling_fn_map[args.cooling_fn],
            cooling_kws=dict(b=args.cooling_base),
            verbose=False
        )
        best_dists.append(best_dist)

    if args.no_agg:
        print('best_dist')
        for d in best_dists:
            print(f'{d:.2f}')
    else:
        mean_best_dist = sum(best_dists) / args.n_trials
        print(f'best_dist = {mean_best_dist:.2f}')

if __name__ == '__main__':
    main(sys.argv[1:])
