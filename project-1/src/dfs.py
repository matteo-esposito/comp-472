# For pycharm
# from src.input_parser import parse, testfile
# from src.board import Board
from input_parser import parse, testfile
from board import Board
import copy
import time

def already_seen(g, group):
    for game in group:
        if g.grid == game.grid:
            return True
    return False

def dfs(n, max_d, max_l, puzzle):
    """Implementation of slide 29 in 472-2-search-Winter2020.pdf
    
    Notes:
        - ignore max_l for dfs
    """
    # Start timer
    s = time.time()
    
    # Initialize
    problem_grid = puzzle.copy()
    open_l = [Board(problem_grid)] # List of board objects
    closed_l = []
    alpha = list(map(chr, range(ord('A'), ord('Z')+1))) # alphabet
    n = len(puzzle)
    moves = [] # TBU   
    
    print("Start:")
    open_l[0].print_grid()
    
    # Limited-depth depth first search algorithm
    while len(open_l) != 0:
        current_puzzle = open_l[0]

        # Goal found
        if current_puzzle.goal_test():
            print(f"Done @ {time.time()-s}")
            return current_puzzle.print_grid()
        else:
            # Generate kids
            for y in alpha[:n]:
                for x in range(1,27)[:n]:
                    # Reset puzzle
                    parent_puzzle = Board(copy.deepcopy(open_l[0].grid)) 
                    parent_puzzle.touch(y + str(x))
                    child = parent_puzzle
                    if not already_seen(child, open_l) or not already_seen(child, closed_l):
                        open_l.append(child)
            
            # Put leftmost_puzzle from open to closed
            closed_l.append(open_l.pop(0))
        
    return 1

if __name__ == "__main__":
    for args in parse(testfile):
        dfs(*args)
