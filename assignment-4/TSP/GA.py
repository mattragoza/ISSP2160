# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 12:48:15 2019

Genetic Algorithm for the TSP 

@authors: Milos Hauskrecht and Giacomo Nebbia
"""
import sys, os, argparse, random
import matplotlib.pyplot as plt

from TSP import TSP_Problem, Standard_Cities
from population import Population


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_population', default=500, type=int, help='population size')
    parser.add_argument('--n_generations', default=500, type=int, help='number of generations to run')
    parser.add_argument('--mutate_prob', default=0.05, type=float, help='probability of an individual being mutated')
    parser.add_argument('--cull_pct', default=0.05, type=float, help='percentage of the least fit individuals to be removed')
    parser.add_argument('--elite_pct', default=0.05, type=float, help='proportion of best individuals to carry over from one generation to the next')
    parser.add_argument('--out_dir', default='fig/', help='directory where to place the plots (it will be automatically created if not existent')
    parser.add_argument('--no_plot', default=False, action='store_true', help='output stats as a metrics file instead of a plot')
    parser.add_argument('--out_file', default=None, help='name of file to output metrics')
    parser.add_argument('--random_seed', default=None, type=int)
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)

    if args.random_seed is not None:
        random.seed(args.random_seed)

    # create output directory if not present
    if not args.no_plot and not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    # initialize the TSP problem
    problem = TSP_Problem(Standard_Cities)

    # store generation-specific stats information
    fitness_vals = []
    min_fitness_vals = []
    pop_size = []

    # generate initial population
    population = Population(problem, N_POP=args.n_population)

    # store average and min fitess values for the current population
    fitness_vals.append(population.mean_fitness())
    min_fitness_vals.append(population.min_fitness())
    pop_size.append(len(population))  
    
    # simulate for the MAX_ITERATION number of generations
    for curr_iter in range(args.n_generations):
        
        # create a new population
        population = population.build_a_new_generation(
            CULLING_PERC=args.cull_pct,
            ELITE_PERC=args.elite_pct,
            M_RATE=args.mutate_prob
        )

        # store stats for the current population
        fitness_vals.append(population.mean_fitness())
        best_fitness=population.min_fitness()
        min_fitness_vals.append(best_fitness)
        pop_size.append(len(population))
        
        # print stats for every 50th population
        if curr_iter % 50 == 0:
            print('Iteration [{}] of [{}] ({:.2f}%) -- Best solution: cost = [{:.2f}] -- Population size [{}]'.format(curr_iter, args.n_generations, curr_iter * 100 / args.n_generations, best_fitness, len(population)))   

    if args.out_file:

        with open(args.out_file, 'w') as f:
            f.write('generation mean_fitness min_fitness pop_size\n')
            for i, (mean_f, min_f, pop) in enumerate(zip(fitness_vals, min_fitness_vals, pop_size)):
                f.write(f'{i} {mean_f} {min_f} {pop}\n')

    if not args.no_plot:
        best_solution = population.get_best_individual()
        print("Best solution found has cost [{:.2f}]\n{}".format(best_solution.fitness, best_solution.tour))

        # plot results
        plt.plot(list(range(len(fitness_vals))), fitness_vals, label = 'Avg')
        plt.plot(list(range(len(fitness_vals))), min_fitness_vals, label = 'Min')
        plt.xlabel('Generations')
        plt.ylabel('Cost (opposite trend of fitness)')
        pars_as_str_title = 'N_pop = {}, p_mut = {:.2f}, p_cull={:.2f}, p_elite={:.2f}'.format(args.n_population, args.mutate_prob, args.cull_pct, args.elite_pct)
        plt.title('Evolution [{}]'.format(pars_as_str_title))
        plt.legend()
        pars_as_str_file = 'N_pop_{}_p_mut_{:02d}_p_cull_{:02d}_p_elite_{:02}'.format(args.n_population, int(args.mutate_prob * 100), int(args.cull_pct * 100), int(args.elite_pct * 100))
        plt.savefig(args.out_dir + 'evolution_{}.png'.format(pars_as_str_file))
        plt.show()


if __name__ == '__main__':
    main(sys.argv[1:])
