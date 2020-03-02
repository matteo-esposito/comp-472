import os
import time
import shutil

from board import Board
from input_parser import parse, testfile, collapse_list
from node import Node


def iterative_bfs(n, max_d, max_l, current_puzzle, file, puzzle_number, path_length):
    """Iterative implementation of Best First search.

        Arguments:
            n {int} -- size of grid (i.e. 2x2 = 2, 3x3 = 3)
            max_d {int} -- N/A
            max_l {int} -- Max Searh Path Length
            current_puzzle {Board} -- Board object that represents the starting puzzle grid
            file -- Output File for Test Cases
            puzzle_number {int} -- index variable for output filenames
            path_length -- parameter to keep track of searched nodes
        """
    successors = [child for child in current_puzzle.generate_states()]

    priority_queue = find_sorted_list(successors, sort_nodes)

    closed_list = []

    path_length = 1

    write_visit(file, current_puzzle)

    while path_length < max_l:
        best = priority_queue.pop(0)
        while best in closed_list:
            best = priority_queue.pop(0)
        closed_list.append(best)

        write_visit(file, best)

        # Testing Goal
        if best.state.goal_test():
            return '2', best

        # Adding Unvisited children nodes to Priority Queue
        for child in best.generate_states():
            status = 'Unvisited'
            for visited in closed_list:
                if child == visited:
                    status = 'Visited'
                    break
            if status == 'Unvisited':
                priority_queue.append(child)

        # Resorting Priority Queue
        priority_queue = find_sorted_list(priority_queue, sort_nodes)

        path_length += 1

    return '1', best


def sort_nodes(node):
    val = str(node.f)  # Start with f-value (first sort)
    val += collapse_list(node.state.grid)  # Append string representation of grid (second sort in case of ties)
    return int(val)


def find_best(nodes, key, i):
    return sorted(nodes, key=key)[i]


def find_sorted_list(nodes, key):
    return sorted(nodes, key=key)


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
    desired_folder_path = os.path.join(os.getcwd(), "out_bfs_h1_iterative_test/")
    if os.path.isdir(desired_folder_path):
        shutil.rmtree(desired_folder_path, ignore_errors=True)
    os.mkdir(desired_folder_path)

    for version, case_args in enumerate(parse(testfile)):

        # counter = Counter()
        path_length = 0

        with open(os.path.join(desired_folder_path, f'{version}_bfs_search.txt'), 'w+') as search_file:

            initial_node = Node('0', Board(case_args[3]), 0)

            s = time.time()
            result, final_node = iterative_bfs(*case_args[:3], initial_node, search_file, version, path_length)
            print(f"Time elapsed for puzzle {version} with size = {case_args[0]} and max_d = {case_args[1]}: {str(round(time.time() - s, 4))}s.")
            search_file.close()

        with open(os.path.join(desired_folder_path, f'{version}_bfs_solution.txt'), 'w+') as solution_file:
            if result == '2':
                write_solution(solution_file, final_node)
            else:
                solution_file.write('no solution')
            solution_file.close()


