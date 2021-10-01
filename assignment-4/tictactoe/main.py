"""
Let's play the tic-tac-toe game!

@author: milos
"""
import sys, os, argparse, random

from tictactoe import TicTacToe
from player import Player
from heuristics import Heuristics
from naive_heuristics import NaiveHeuristics
import my_heuristics


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size', type=int, default=10, help='play games on an N x N board of this size')
    parser.add_argument('--A_heuristic', type=str, default='basic', help='heuristic function for player A (naive|basic)')
    parser.add_argument('--B_heuristic', type=str, default='naive', help='heuristic function for player B (naive|basic)')
    parser.add_argument('--A_k_ply', type=int, default=2, help='depth limit for player A\'s search algorithm')
    parser.add_argument('--B_k_ply', type=int, default=2, help='depth limit for player B\'s search algorithm')
    parser.add_argument('--n_A_starts', type=int, default=1, help='number of games to play where player A starts')
    parser.add_argument('--n_B_starts', type=int, default=1, help='number of games to play where player B starts')
    parser.add_argument('--print_steps', default=False, action='store_true')
    parser.add_argument('--out_file', type=str, default=None, help='output file to write win/loss/draw counts')
    parser.add_argument('--random_seed', type=int, default=None)
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)

    if args.random_seed is not None:
        random.seed(args.random_seed)

    heuristic_map = {
        'naive': NaiveHeuristics(),
        'basic': Heuristics(),
        'my': my_heuristics.MyHeuristics(),
    }

    # define players
    playerA = Player(args.A_k_ply, heuristic_map[args.A_heuristic], 'Player A')
    playerB = Player(args.B_k_ply, heuristic_map[args.B_heuristic], 'Player B')
    stats = {'Player A wins': 0, 'Player B wins': 0, 'Tied': 0}

    # set the board size of the game
    board_size = args.board_size

    # start the game with players A and B
    # use print_steps=False to remove printouts of moves
    game = TicTacToe(board_size, playerA, playerB, print_steps=args.print_steps)
    outcomes = []

    for i in range(args.n_A_starts):
        # Player A moves first
        game.reset()
        game.set_players(playerA, playerB)
        result, winner = game.start()
        print(result)
        if winner is None:
            stats['Tied'] += 1
        else:
            stats['{} wins'.format(winner.name)] += 1
        outcomes.append((i, repr('Player A'), repr(winner.name) if winner else 'Tie'))

    for i in range(args.n_B_starts):
        # Player B moves first
        game.reset()
        game.set_players(playerB, playerA)
        result, winner = game.start()
        print(result)
        if winner is None:
            stats['Tied'] += 1
        else:
            stats['{} wins'.format(winner.name)] += 1
        outcomes.append(
            (i+args.n_A_starts, repr('Player B'), repr(winner.name) if winner else 'Tie')
        )

    print(stats)

    if args.out_file is not None:
        with open(args.out_file, 'w') as f:
            f.write('game_idx start outcome\n')
            for game_idx, start, outcome in outcomes:
                f.write(f'{game_idx} {start} {outcome}\n')


if __name__ == '__main__':
    main(sys.argv[1:])
