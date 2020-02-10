import copy

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
        print()
