from board import Board

class Node:
    def __init__(self, move, state, parent=None):
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

    def generate_states(self):
        children = []
        n = len(self)
        alpha = list(map(chr, range(ord('A'), ord('Z')+1))) # alphabet

        # Generate children
        for y in alpha[:n]:
            for x in range(1,27)[:n]:

                # Make move, create child Node (includes move and board) and append this new node to parent.
                move = y + str(x)
                new_state = self.state.touch(move)
                child = Node(move = move, state = Board(new_state), parent = self)

                children.append(child)

        return children
