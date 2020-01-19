class Board:

    def __init__(self, grid):
        self.grid = grid

    def touch(self, move):
        # move must be in the form A1,...,D4,etc
        y_coord = ord(move[0]) - 65
        x_coord = int(move[1]) - 1

        for y, x in [(y_coord - 1, x_coord), (y_coord + 1, x_coord), (y_coord, x_coord), (y_coord, x_coord - 1), (y_coord, x_coord + 1)]:
            try:
                if x < 0 or y < 0 or x > n or y > n:
                    raise IndexError
                self.grid[y][x] ^= 1
            except IndexError:
                continue

    def goal_test(self):
        list_grid = [e for row in self.grid for e in row]
        if all(e == 0 for e in list_grid):
            return True
        else:
            return False

    def print_grid(self):
        for row in self.grid:
            print(row)


if __name__ == '__main__':
    grid = [[1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 0, 0], [1, 0, 1, 0]]
    n = len(grid)
    board = Board(grid)
    board.print_grid()

    while not board.goal_test():
        move = input("Please enter move: ")
        if len(move) == 2:
            y_coord = (ord(move[0]) - 65)
            x_coord = int(move[1]) - 1
            y_cond = False
            x_cond = False

            # Check if moves are in bounds
            if y_coord < n and y_coord >= 0:
                y_cond = True

            if x_coord < n and x_coord >= 0:
                x_cond = True

            if y_cond and x_cond:
                board.touch(move)

            else:
                print('Not a valid move')
                continue
        else:
            print('Not a valid move')
            continue

        board.print_grid()
        if board.goal_test():
            print('Board solved')
