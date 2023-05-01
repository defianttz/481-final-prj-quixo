from games import *

class Quixo(Game):

    def __init__(self, h=5, v=5, k=3):
        self.h = h
        self.v = v
        self.k = k
        self.initial = GameState(to_move='X', utility=0, board={})

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
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

    def display(self, state):
        """Print or otherwise display the state."""
        pass

    def compute_utility(self, state):
        """If the game is over, return the utility for player."""
        pass

    if __name__ == '__main__':
        print("To play a game of Quixo, type 'Quixo().play_game()'")
        #Quixo().play_game()