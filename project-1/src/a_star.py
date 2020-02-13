import os
import time

from board import Board
from input_parser import parse, testfile, collapse_list
from node import Node


def recursive_a_star(max_l, current_puzzle, f):

    current_puzzle.h = h(current_puzzle.state)

    if current_puzzle.state.goal_test():
        write_visit(f, current_puzzle)
        return current_puzzle

    elif max_l == 1:
        return '1'

    else:
        successors = []
        child_states = current_puzzle.generate_states()
        for child in child_states:
            child.f = max(child.g + child.h, current_puzzle.f)
            successors.append(child)


def write_solution(f, final_node):
    intermediate_node = final_node
    final_path = []

    while intermediate_node.move != '0':
        final_path.append({intermediate_node.move: intermediate_node.state.grid})
        intermediate_node = intermediate_node.parent

    for move, grid in list(final_path.items())[::-1]:
        f.write(f'{move} {collapse_list(grid)}\n')


def write_visit(f, node):
    f.write(f'{node.f} {node.g} {node.h} {collapse_list(node.state.grid)}\n')
