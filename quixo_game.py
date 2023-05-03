from games import *


class Quixo(Game):

    def __init__(self, h=5, v=5, k=5):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        # Set board to blank spaces
        board = [[' ' for _ in range(5)]
                        for _ in range(5)]

        self.initial = GameState(to_move='X', utility=0, board=board, moves=moves)

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        pass

    def get_moves(self, board):
        """Return a list of moves for this board."""
        pass

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        pass

    def utility(self, state, player):
        """Return the value of this final state to player."""
        pass

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        pass

    # Define a function to print the current board state
    def print_board(self, board):
        """Print the current board state."""
        for row in board:
            print('|' + '|'.join(row) + '|')

    def display(self, state):
        """Print or otherwise display the state."""
        pass

    def compute_utility(self, state):
        """If the game is over, return the utility for player."""
        pass

if __name__ == '__main__':
    print("Let's play Quixo!")
    q = Quixo()
    q.print_board(q.initial.board)

        # Quixo().play_game()
