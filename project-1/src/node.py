from board import Board
import math


class Node:
    def __init__(self, move, state, g=0, parent=None):
        """
        Node class to be used for grid space searching.

        Attributes:
            state (Board) - has attribute grid (actual nested list of 1, 0.)
            parent (Node)
            action (str)
        """
        self.move = move
        self.parent = parent
        self.state = state
        self.g = g
        self.h = self.calculate_h2()
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.state.grid == other.state.grid

    def __len__(self):
        return len(self.state.grid)

    def __str__(self):
        print(f"Move: {self.move}")
        self.state.print_grid()

        return ""

    def get_parent(self):
        return self.parent

    def generate_states(self, use_g=True):
        children = []
        n = len(self)
        alpha = list(map(chr, range(ord('A'), ord('Z') + 1)))  # alphabet

        # Generate children
        for y in alpha[:n]:
            for x in range(1, 27)[:n]:

                # Make move, create child Node (includes move and board) and append this new node to parent.
                move = y + str(x)
                new_state = self.state.touch(move)
                if use_g:
                    child = Node(move=move, state=Board(new_state), parent=self, g=self.g + 1)
                else:
                    child = Node(move=move, state=Board(new_state), parent=self)

                children.append(child)

        return children

    def calculate_h(self):
        # Heuristic function, tests number of moves necessary assuming every move flips 5 arbitrary squares
        list_grid = [e for row in self.state.grid for e in row]
        return math.ceil(sum(list_grid) / 5)

    def calculate_h2(self):
        list_grid = [e for row in self.state.grid for e in row]
        return sum(list_grid)
