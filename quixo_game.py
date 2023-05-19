from games import *
import time
start_time = time.time()
class Quixo(Game):

    def __init__(self, board=None):
        self.h = 5
        self.v = 5
        self.k = 5
        if board is None:
            moves = [(x, y) for x in range(1, self.h + 1)
                     for y in range(1, self.v + 1)]

            # Set board to blank spaces
            board = [[' ' for _ in range(self.v)] for _ in range(self.h)]
        else:
            moves = self.get_moves(board)


        self.initial = GameState(to_move='X', utility=0, board=board, moves=moves)

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        return state.moves
    def log_info(self, text):
        with open("debug_log.txt", "a") as myfile:
            myfile.write(text)
    def get_moves(self, board):
        """Return a list of moves for this board."""
        moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == ' ':
                    moves.append((i+1, j+1))
        return moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        #"""Return the state that results from making a move from a state."""
        player = state.to_move
        board = [row[:] for row in state.board]
        board[move[0]-1][move[1]-1] = player
        moves = state.moves[:]
        moves.remove(move)

        return GameState(to_move=('O' if player == 'X' else 'X'),
                          utility=self.compute_utility(board, player),
                          board=board, moves=moves)

    def utility(self, state, player, depth=0):
        """Return the value of this final state to player."""
        if player == 'X':
            return state.utility + depth
        else:
            return -state.utility - depth

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
        #print("Current state:")
        self.print_board(state.board)
        #print("Next player:", state.to_move)

    def compute_utility(self, board, player):
        """If the game is over, return the utility for player."""
        # check if the row has a winner
        for i in range(len(board)):
            if all(x == player for x in board[i]):
                return 10
        # check if the column has a winner
        for j in range(len(board[0])):
            if all(board[i][j] == player for i in range(len(board))):
                return 10
        # check if the diagonal has a winner (left to right)
        if all(board[i][i] == player for i in range(len(board))):
            return 10
        # check if the diagonal has a winner (right to left)
        if all(board[i][len(board) - i - 1] == player for i in range(len(board))):
            return 10
        # if there is no winner, return 0
        return 0
    def check_rows(self, board, player):
        """If the game is over, return the utility for player."""
        for i in range(len(board)):
            if all(x == player for x in board[i]):
                return 10
        return 0

    def check_columns(self, board, player):
        for j in range(len(board[0])):
            if all(board[i][j] == player for i in range(len(board))):
                return 1
        return 0

    def check_diagonal_lr(self, board, player):
        if all(board[i][i] == player for i in range(len(board))):
            return 1
        return 0

    def check_diagonal_rl(self, board, player):
        if all(board[i][len(board) - i - 1] == player for i in range(len(board))):
            return 1
        return 0

    def play_game(self):
        state = self.initial
        while True:
            player = state.to_move
            print("Player", player, "'s turn")

            if player == 'X':
                move = query_player(self, state)
                #move = random_player(self, state)
            else:
                move = alpha_beta_cutoff_search(state, self)

            state = self.result(state, move)
            print(f"{player} picked {move} utility={state.utility}\n")

            self.display(state)
            if self.terminal_test(state):
                print("Game over!")
                return self.utility(state, state.to_move)

if __name__ == '__main__':
    print("Let's play Quixo!")
    """board = [['X', 'X', 'X', 'O', ' '],
             ['O', 'X', 'O', ' ', ' '],
             ['O', ' ', ' ', ' ', ' '],
             ['O', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', 'X']]"""
    """board = [['X', 'X', 'X', ' '],
             ['O', 'X', 'O', ' '],
             ['O', ' ', 'X', ' '],
             ['O', ' ', 'O', ' ']]"""
    q = Quixo()

    utility = q.play_game() # computer moves first
    end_time = time.time()
    print("\nGame over!")
    if utility >0:
        print("\nPlayer X wins!")
    elif utility < 0:
        print("\nPlayer O wins!")
    else:
        print("\nGame ended in a draw!")
    runtime = end_time - start_time
    print("Runtime:", runtime, "seconds")

