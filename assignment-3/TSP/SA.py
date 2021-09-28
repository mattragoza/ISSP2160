import math, random
import TSP


def p_accept(delta, temp):
    '''
    Get the probability of accepting
    a worse state based on the energy
    delta and the simulation step and
    the current temperature.
    '''
    assert delta >= 0
    assert temp > 0
    return math.exp(-delta/temp)


def linear_cooling(i, k, **kwargs):
    '''
    Return a linear cooling coefficient
    for simulation step i out of k.
    '''
    return (k - i)/k


def sim_anneal(
    TSP_problem,
    no_of_steps,
    init_temperature,
    cooling_fn=linear_cooling,
    cooling_kws=dict(),
    verbose=False
):
    '''
    Solve the traveling salesman problem
    using simulated annealing.
    '''
    # random initial tour and distance
    init_tour = TSP_problem.generate_random_tour()
    init_dist = TSP_problem.evaluate_tour(init_tour)

    # collect statistics
    n_tours_tried = 0
    n_tours_accepted = 0

    # track the current and best tours
    best_tour = curr_tour = init_tour
    best_dist = curr_dist = init_dist

    for i in range(no_of_steps):

        # get next candidate tour
        next_tour = TSP_problem.permute_tour(curr_tour)
        next_dist = TSP_problem.evaluate_tour(next_tour)
        delta = next_dist - curr_dist
        n_tours_tried += 1

        # linear cooling schedule
        temp = init_temperature * cooling_fn(i, k=no_of_steps, **cooling_kws)

        if next_dist < curr_dist:
            if verbose:
                print(
                    f'[step={i} temp={temp} dist={curr_dist:.2f}] {delta}'
                )
            # always accept better tours
            curr_tour = next_tour
            curr_dist = next_dist
            n_tours_accepted += 1

            if curr_dist < best_dist:
                # found new best tour
                best_tour = curr_tour
                best_dist = curr_dist

        elif p_accept(delta, temp) >= random.random():
            if verbose:
                print(
                    f'[step={i} temp={temp} dist={curr_dist:.2f}] {delta}'
                )
            # accept the tour, even though it's worse
            curr_tour = next_tour
            curr_dist = next_dist
            n_tours_accepted += 1

    return (
        init_tour,
        init_dist,
        best_tour,
        best_dist,
        n_tours_tried,
        n_tours_accepted
    )


if __name__ == '__main__':
    tsp_problem = TSP.TSP_Problem(TSP.Standard_Cities)
    (
        init_tour,
        init_dist,
        best_tour,
        best_dist,
        n_tours_tried,
        n_tours_accepted
    ) = sim_anneal(tsp_problem, 100000, 100, verbose=False)

    print(f'init_dist = {init_dist:.2f}')
    print(f'best_dist = {best_dist:.2f}')
    print(f'n_tours_tried = {n_tours_tried}')
    print(f'n_tours_accepted = {n_tours_accepted}')
