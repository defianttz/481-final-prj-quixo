from games import *


class Quixo(Game):

    def __init__(self, h=5, v=5, k=5):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        # Set board to blank spaces
        board = [[' ' for _ in range(self.v)] for _ in range(self.h)]

        self.initial = GameState(to_move='X', utility=0, board=board, moves=moves)

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        return state.moves

    def get_moves(self, board):
        """Return a list of moves for this board."""
        moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        player = state.to_move
        board = [row[:] for row in state.board]
        board[self.h - move[1] - 1][move[0]-1] = player
        moves = state.moves[:]
        moves.remove(move)
        return GameState(to_move=('O' if player == 'X' else 'X'),
                          utility=self.compute_utility(board, player),
                          board=board, moves=moves)

    def utility(self, state, player):
        """Return the value of this final state to player."""
        if player == 'X':
            return state.utility
        else:
            return -state.utility

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return state.utility != 0 or len(state.moves) == 0

    # Define a function to print the current board state
    def print_board(self, board):
        """Print the current board state."""
        for row in board:
            print('|' + '|'.join(row) + '|')

    def display(self, state):
        """Print or otherwise display the state."""
        print("Current state:")
        self.print_board(state.board)
        print("Next player:", state.to_move)

    def compute_utility(self, board, player):
        """If the game is over, return the utility for player."""
        for i in range(len(board)):
            if all(x == player for x in board[i]):
                return 1
        for j in range(len(board[0])):
            if all(board[i][j] == player for i in range(len(board))):
                return 1
        if all(board[i][i] == player for i in range(len(board))):
            return 1
        if all(board[i][len(board) - i - 1] == player for i in range(len(board))):
            return 1
        return 0
    def min_value(self, state):
        if self.terminal_test(state):
            return self.utility(state, 'O')
        v = float('inf')
        for action in self.actions(state):
            v = min(v, self.max_value(self.result(state, action)))
        return v
    def max_value(self, state):
        if self.terminal_test(state):
            return self.utility(state, 'X')
        v = float('-inf')
        for action in self.actions(state):
            v = max(v, self.min_value(self.result(state, action)))
        return v
    def minmax_decision(self, state, game):
        """Return the optimal action for the current player, using the Minimax algorithm."""
        player = state.to_move
        if player == 'X':
            return max(game.actions(state), key=lambda move: game.min_value(game.result(state, move)))
        else:
            return min(game.actions(state), key=lambda move: game.max_value(game.result(state, move)))

    def play_game(self):
        state = self.initial
        while True:
            player = state.to_move
            print("Player", player, "'s turn")
            self.display(state)
            if self.terminal_test(state):
                print("Game over!")
                return self.compute_utility(state.board, 'X')
            move = self.minmax_decision(state, self)
            state = self.result(state, move)
if __name__ == '__main__':
    print("Let's play Quixo!")
    q = Quixo()
    #t = TicTacToe()
    #print(t.play_game(minmax_player, random_player))
    q.play_game(minmax_player, random_player)
