import os
import shutil
import time

from board import Board
from input_parser import parse, testfile, collapse_list
from node import Node

def recursive_dls(n, max_d, max_l, current_puzzle, puzzle_number):
    """Recursive implementation of depth limited search.

    Arguments:
        n {int} -- size of grid (i.e. 2x2 = 2, 3x3 = 3)
        max_d {int} -- max depth
        max_l {int} -- N/A
        current_puzzle {Board} -- Board object that represents the starting puzzle grid
        puzzle_number {int} -- index variable for output filenames
    """
    # Solution reached. Return path and solved grid.
    if current_puzzle.state.goal_test():

        # Create path to solution
        intermediate_puzzle = current_puzzle
        final_path = []

        # Populate dict of moves and states to solution.
        while True:
            final_path.append(
                {intermediate_puzzle.move: intermediate_puzzle.state.grid})  # Store the move that led us to solution
            intermediate_puzzle = intermediate_puzzle.parent  # Move up the tree and repeat until we hit root.

            # When we hit root, i.e. None parent, add "0" to final path.
            if not intermediate_puzzle.parent:
                final_path.append({"0": intermediate_puzzle.state.grid})
                break

        # Output path and grid.
        with open(f"out_dfs/{puzzle_number}_dfs_solution.txt", 'w') as f:

            for pair in final_path[::-1]:
                for move, grid in pair.items():
                    f.write("{} {}\n".format(move, collapse_list(grid)))
            f.close()

        return final_path

    # Hit max depth and didn't reach solution.
    elif max_d == 1:
        return "1"

    # Continue recursive calls of dfs limited depth.
    else:
        # Get all child states and run dls on them.
        child_states = current_puzzle.generate_states()
        hit_max_depth = False

        # Launch recursive calls of dls on children nodes.
        for child_node in child_states:

            # Print node that is being visited at the moment (write if file doesnt exist, append if it does.)
            fname = f"out_dfs/{puzzle_number}_dfs_search.txt"
            with open(fname, "a+") as f:
                f.write("{} {} {} {}\n".format("0", "0", "0", collapse_list(child_node.state.grid)))
                f.close()

            # Decrement max_d on each recursive call.
            result = recursive_dls(n, max_d - 1, max_l, child_node, puzzle_number)

            # Check if we have hit no sol (failure) or max depth with no sol (cutoff)
            if max_depth_hit(result):
                hit_max_depth = True
            else:
                return result

        # Check if hit max or failed search for each child in the generated child states.
        if hit_max_depth:
            return "1"  # Backtrack
        else:
            return []  # Continue


def max_depth_hit(result):
    """Check if the search yielded no solution due to having hit the max depth.

    Arguments:
        result {str, list} -- Result of search.

    Returns:
        bool -- Has max depth been hit.
    """
    return (len(result) == 1) and (result[0] == "1")


def write_starting_state(start_node, puzzle_version):
    """Write out starting state in search text file.

    Arguments:
        start_node {Node} -- start node of the problem.
        puzzle_version {int} -- iterator for filenaming (same as the one used for the search).
    """
    fname = f"out_dfs/{puzzle_version}_dfs_search.txt"
    with open(fname, "w+") as f:
        f.write("{} {} {} {}\n".format("0", "0", "0", collapse_list(start_node.state.grid)))
        f.close()
    return


def write_no_solution(result, puzzle_version):
    """Write to solution file "no solution" in the case that dfs never yields a solution.

    Arguments:
        result {dict or str} -- If result == "1", we know we didn't reach a solution and this method will run.
        puzzle_version {int} -- iterator for filenaming (same as the one used for the search).
    """
    if result == "1":
        with open(f"out_dfs/{puzzle_version}_dfs_solution.txt", 'w+') as f:
            f.write("no solution")
            f.close()
    return


if __name__ == '__main__':

    # If folder exists, delete it and create a new version (clear old output)
    desired_folder_path = os.path.join(os.getcwd(), "out_dfs/")
    if os.path.isdir(desired_folder_path):
        shutil.rmtree(desired_folder_path, ignore_errors=True)
    os.mkdir(desired_folder_path)

    # Run search and output to text files.
    for version, case_args in enumerate(parse(testfile)):

        # Write initial setup to search file.
        initial_node = Node("0", Board(case_args[3]))
        write_starting_state(initial_node, version)

        # Run dfs timed.
        s = time.time()
        res = recursive_dls(*case_args[:3], initial_node, version)
        print(
            f"Time elapsed for puzzle {version} with size = {case_args[0]} and max_d = {case_args[1]}: {str(round(time.time() - s, 4))}s.")

        # Write out "no solution" in the case where we return a failed search.
        write_no_solution(res, version)
