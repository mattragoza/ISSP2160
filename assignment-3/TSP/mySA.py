import sys, argparse, math
import TSP, SA
from SA import linear_cooling


def cosine_cooling(i, k, f=1, **kwargs):
    '''
    Return a cosine-modulated linear
    cooling coefficient for simulation 
    step i out of k.
    '''
    return (k - i)/k * (1 + math.cos(math.pi*i*f)/2)


def power_cooling(i, k, b=0.01, **kwargs):
    '''
    Return an exponential cooling
    coefficient for simulation step
    i out of k.
    '''
    return b**(i/k)


def step_cooling(i, k, b=0.01, n=5, **kwargs):
    '''
    Return an step-wise cooling
    coefficient for simulation step
    i out of k.
    '''
    return b**math.floor(n*i/k)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_trials', type=int, default=10)
    parser.add_argument('--n_steps', type=int, default=20000)
    parser.add_argument('--init_temp', type=int, default=50)
    parser.add_argument('--cooling_fn', type=str, default='step')
    parser.add_argument('--cooling_base', type=float, default=0.01)
    parser.add_argument('--no_agg', default=False, action='store_true')
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    tsp_problem = TSP.TSP_Problem(TSP.Standard_Cities)

    cooling_fn_map = {
        'linear': linear_cooling,
        'cosine': cosine_cooling,
        'power': power_cooling,
        'step': step_cooling,
    }

    best_dists_and_tours = []
    for i in range(args.n_trials):
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
        best_dists_and_tours.append((best_dist, best_tour))

    if args.no_agg:
        print('trial_idx best_dist best_tour')
        for i, (best_dist, best_tour) in enumerate(best_dists_and_tours):
            print(f'{i} {best_dist:.2f} {",".join(map(str, best_tour))}')
    else:
        mean_best_dist = sum(d for d,t in best_dists_and_tours) / args.n_trials
        min_best_dist, min_best_tour = sorted(best_dists_and_tours)[0]
        print(f'mean_best_dist = {mean_best_dist:.2f}')
        print(f'min_best_dist = {min_best_dist:.2f}')
        print(f'min_best_tour = {min_best_tour}')

if __name__ == '__main__':
    main(sys.argv[1:])
