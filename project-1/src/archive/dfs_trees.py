from input_parser import parse, testfile
import copy
import time


class Board:
    
    def __init__(self, grid):
        self.grid = grid

    def touch(self, move):
        # move must be in the form A1,...,D4,etc
        y_coord = ord(move[0]) - 65
        x_coord = int(move[1]) - 1
        n = len(self.grid)
        
        # Don't modify inplace
        temp_grid = copy.deepcopy(self.grid)

        for y, x in [(y_coord - 1, x_coord), (y_coord + 1, x_coord), 
                     (y_coord, x_coord), (y_coord, x_coord - 1), (y_coord, x_coord + 1)]:
            try:
                if x < 0 or y < 0 or x >= n or y >= n:
                    raise IndexError
                temp_grid[y][x] ^= 1 # Flip from black to white or vice versa.
            except IndexError:
                continue
                
        return temp_grid

    def goal_test(self):
        list_grid = [e for row in self.grid for e in row]
        if all(e == 0 for e in list_grid):
            return True
        else:
            return False

    def print_grid(self):
        for row in self.grid:
            print(row)
        print("_")

class Node:
    
    def __init__(self, move, state):
        self.move = move
        self.state = state
        self.children = []
        self.parent = None
    
    def assign_parent(self):
        for child in self.children:
            child.parent = self
        
    def add_child(self, new_node):
        self.children.append(new_node)
        
    def get_depth(self, root):
        # DFS implementation of max depth call
        if not root: 
            return 0
        
        # Recursive calls of get_depth()
        maximum_depth = 0  
        for c in root.children:
            maximum_depth = max(maximum_depth, self.get_depth(c))
            
        return maximum_depth + 1
    
    def __eq__(self, other_node):
        return (self.move == other_node.move) and (self.state.grid == other_node.state.grid)

    def __str__(self):
        print(f"Move: {self.move}")
        
        print("State:")
        self.state.print_grid()

        if self.children == []:
            return ""
        else:        
            print("Children:")
            for c in self.children:
                c.state.print_grid()
        return ""

def already_seen(g, group):
    for game in group:
        if g.state == game.state:
            return True
    return False

def dfs_tree(n, max_d, max_l, puzzle):
    """Implementation of slide 29 in 472-2-search-Winter2020.pdf
    
    Notes:
        - ignore max_l for dfs
    """
    # Start timer
    s = time.time()
    
    # Make use of n (processing using n is used in parse())
    assert n == len(puzzle)
    
    # Initialize
    alpha = list(map(chr, range(ord('A'), ord('Z')+1))) # alphabet
    n = len(puzzle)
    
    # 
    print("===== Initial State =====")
    root = Node("0", Board(puzzle))
    print(root, "\n=========================")
    
    # Initialize lists to be used
    open_l = [root] 
    closed_l = []
    final_path = []
    
    # Limited-depth depth first search algorithm
    while len(open_l) != 0:

        # Set current puzzle
        current_puzzle = open_l[0]
        d = current_puzzle.get_depth(root)

        if d > max_d:
            break

        # Goal found
        if current_puzzle.state.goal_test():
            print("Solved in {}s".format(str(round(time.time()-s, 6))))
            intermediate_puzzle = current_puzzle

            while True:
                final_path.append(intermediate_puzzle.move) # Store the move that led us to solution
                intermediate_puzzle = intermediate_puzzle.parent # Move up the tree and repeat until we hit root.
                if not intermediate_puzzle.parent:
                    final_path.append("0")
                    break
                
            # Outputs
            print(f"Path to solution: {final_path[::-1]}")
            return root, current_puzzle.state.print_grid()
        else:
            # Generate children
            for y in alpha[:n]:
                for x in range(1,27)[:n]:
                    
                    # Make move, create child Node (includes move and board) and append this new node to parent.
                    move = y + str(x)
                    new_state = current_puzzle.state.touch(move)
                    child = Node(move, Board(new_state))
                    
                    # Assign parent
                    current_puzzle.assign_parent()
                    
                    # Check if child has been visited or not
                    if not already_seen(child, open_l) or not already_seen(child, closed_l):
                        open_l.append(child)
                        current_puzzle.add_child(child)
            
            # Put leftmost_puzzle from open to closed
            closed_l.append(open_l.pop(0))
    
    # If all fails, print no solution.
    print(f"\nNo solution after depth {d-1}")
    return None, None


if __name__ == '__main__':

    # Testing
    grid = [[1, 1], [1, 0]]
    solved, _ = dfs_tree(2, 3, 0, grid)

    # Prod
    # for args in parse(testfile):
    #     solved_root, _ = dfs_tree(*args)