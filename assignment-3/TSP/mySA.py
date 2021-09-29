import sys, argparse, math
import TSP, SA
from SA import linear_cooling


def cosine_cooling(i, k, f=10, **kwargs):
    '''
    Return a cosine-modulated linear
    cooling coefficient for simulation 
    step i out of k.
    '''
    return (k - i)/k * (1 + math.cos(math.pi*i*f/k)/2)


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
    return b**(math.floor(n*i/k)/n)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_trials', type=int, default=10)
    parser.add_argument('--n_steps', type=int, default=20000)
    parser.add_argument('--init_temp', type=int, default=1)
    parser.add_argument('--cooling_fn', type=str, default='power')
    parser.add_argument('--cooling_base', type=float, default=0.1)
    parser.add_argument('--no_agg', default=False, action='store_true')
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    tsp_problem = TSP.TSP_Problem(TSP.Standard_Cities)

    if not args.no_agg:
        print(f'n_trials = {args.n_trials}')
        print(f'n_steps = {args.n_steps}')
        print(f'init_temp = {args.init_temp}')
        print(f'cooling_fn = {args.cooling_fn}')
        print(f'cooling_base = {args.cooling_base}')

    cooling_fn_map = {
        'linear': linear_cooling,
        'cosine': cosine_cooling,
        'power': power_cooling,
        'step': step_cooling,
    }

    best_tours_and_stats = []
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
        best_tours_and_stats.append(
            (best_dist, best_tour, init_dist, n_tours_tried, n_tours_accepted)
        )
        if not args.no_agg:
            print('.', end='', flush=True)

    if not args.no_agg:
        print()

    if args.no_agg:
        print('trial_idx init_dist n_tours_tried n_tours_accepted best_dist best_tour')
        for i, (bd, bt, id_, nt, na) in enumerate(best_tours_and_stats):
            print(f'{i} {id_:.2f} {nt:.2f} {na:.2f} {bd:.2f} {",".join(map(str, best_tour))}')
    else:
        mean_best_dist = sum(t[0] for t in best_tours_and_stats) / args.n_trials
        mean_init_dist = sum(t[2] for t in best_tours_and_stats) / args.n_trials
        mean_n_tried = sum(t[3] for t in best_tours_and_stats) / args.n_trials
        mean_n_accept = sum(t[4] for t in best_tours_and_stats) / args.n_trials
        print(f'mean_best_dist = {mean_best_dist:.2f}')
        print(f'mean_n_tried = {mean_n_tried:.2f}')
        print(f'mean_n_accept = {mean_n_accept:.2f}')
        print(f'mean_init_dist = {mean_init_dist:.2f}')

        best_tour_and_stats = sorted(best_tours_and_stats)[0]
        best_best_dist = best_tour_and_stats[0]
        best_best_tour = best_tour_and_stats[1]
        best_init_dist = best_tour_and_stats[2]
        best_n_tried = best_tour_and_stats[3]
        best_n_accept = best_tour_and_stats[4]
        print(f'best_best_dist = {best_best_dist:.2f}')
        print(f'best_n_tried = {best_n_tried:.2f}')
        print(f'best_n_accept = {best_n_accept:.2f}')
        print(f'best_init_dist = {best_init_dist:.2f}')
        print(f'best_best_tour = {best_best_tour}')
if __name__ == '__main__':
    main(sys.argv[1:])
