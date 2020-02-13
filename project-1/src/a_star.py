import os
import time
import shutil

from board import Board
from input_parser import parse, testfile, collapse_list
from node import Node


def recursive_a_star(n, max_d, max_l, current_puzzle, f_limit, file, puzzle_number):

    write_visit(file, current_puzzle)

    if current_puzzle.state.goal_test():
        return '2', current_puzzle

    elif max_l == 1:
        return '1', current_puzzle

    else:
        successors = []
        child_states = current_puzzle.generate_states()
        for child in child_states:
            child.f = max(child.f, current_puzzle.f)
            successors.append(child)

        while True:
            best = find_best(successors, sort_nodes, 0)
            if best.f > f_limit:
                return '0', best
            alternative = find_best(successors, sort_nodes, 1)
            result, best_recursive_node = recursive_a_star(n, max_d, max_l - 1, best, min(f_limit, alternative.f), file, puzzle_number)
            best.f = best_recursive_node.f
            if result != '0':
                return result, best_recursive_node


def sort_nodes(node):
    val = str(node.f)  # Start with f value (first sort)
    val += collapse_list(node.state.grid)  # Append string representation of grid (second sort in case of ties)
    return int(val)


def find_best(nodes, key, i):
    return sorted(nodes, key=key)[i]


def write_solution(f, final_node):
    intermediate_node = final_node
    final_path = []

    while intermediate_node.move != '0':
        final_path.append((intermediate_node.move, intermediate_node.state.grid))
        intermediate_node = intermediate_node.parent
    else:
        f.write(f'{intermediate_node.move} {collapse_list(intermediate_node.state.grid)}\n')

    for move, grid in final_path[::-1]:
        f.write(f'{move} {collapse_list(grid)}\n')


def write_visit(f, node):
    f.write(f'{node.f} {node.g} {node.h} {collapse_list(node.state.grid)}\n')


if __name__ == '__main__':
    desired_folder_path = os.path.join(os.getcwd(), "out_a_star/")
    if os.path.isdir(desired_folder_path):
        shutil.rmtree(desired_folder_path, ignore_errors=True)
    os.mkdir(desired_folder_path)

    for version, case_args in enumerate(parse(testfile)):

        with open(f'out_a_star/{version}_a_star_search.txt', 'w+') as search_file:

            initial_node = Node('0', Board(case_args[3]), 0)

            s = time.time()
            result, final_node = recursive_a_star(*case_args[:3], initial_node, 100000000, search_file, version)
            print(f"Time elapsed for puzzle {version} with size = {case_args[0]} and max_d = {case_args[1]}: {str(round(time.time() - s, 4))}s.")
            search_file.close()

        with open(f'out_a_star/{version}_a_star_solution.txt', 'w+') as solution_file:
            if result == '2':
                write_solution(solution_file, final_node)
            else:
                solutions_file.write('no solution')
            solution_file.close()
