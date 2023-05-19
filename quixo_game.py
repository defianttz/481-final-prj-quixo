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

    def terminal_test2(self, state):
        board = state.board

        # Check if the board is completely filled
        if all(cell != ' ' for row in board for cell in row):
            return True

        # Check if there is a winner in any row
        for row in board:
            if len(set(row)) == 1 and row[0] != ' ':
                return True

        # Check if there is a winner in any column
        for col in range(len(board[0])):
            column = [board[row][col] for row in range(len(board))]
            if len(set(column)) == 1 and column[0] != ' ':
                return True

        # Check if there is a winner in the main diagonal
        diagonal = [board[i][i] for i in range(len(board))]
        if len(set(diagonal)) == 1 and diagonal[0] != ' ':
            return True

        # Check if there is a winner in the anti-diagonal
        anti_diagonal = [board[i][len(board) - i - 1] for i in range(len(board))]
        if len(set(anti_diagonal)) == 1 and anti_diagonal[0] != ' ':
            return True

        return False


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

    def compute_utility2(self, board, player):
        """If the game is over, return the utility for player."""

        if (self.check_rows(board, player) or
            self.check_columns(board, player) or
            self.check_diagonal_lr(board, player) or
            self.check_diagonal_rl(board, player)):
            return 10 if player == 'X' else -10
        else:
            return 0
    def min_value(self, state):
        if (self.terminal_test(state)):
            score = self.utility(state,  state.to_move)
            return score
        #depth -= 1
        global boards
        boards += 1
        v = np.inf
        for action in self.actions(state):

            v = min(v, self.max_value(self.result(state, action)))

        return v

    def max_value(self, state):
        if (self.terminal_test(state)):
            return self.utility(state, state.to_move)
        global boards
        boards += 1
        v = -np.inf
        for action in self.actions(state):
            #print(f"     move={action} board={state.board} depth={depth} player={state.to_move}\n")
            #print(f"     move1={action} board={state.board} player={state.to_move}\n utility={self.utility(state, state.to_move)}\n")

            v = max(v, self.min_value(self.result(state, action)))
            #print(f"     move2={action} board={state.board} player={state.to_move}\n utility={self.utility(state, state.to_move)}\n")

        return v
    def minmax_depth(self, state, game):
        """Return the optimal action for the current player, using the Minimax algorithm."""
        player = state.to_move
        max_depth = 4
        global boards
        boards = 0
        def min_value(state, alpha, beta, depth):
            #winner_found = self.terminal_test(state)

            if self.terminal_test(state):
                return self.utility(state, player, depth)

            global boards

            boards += 1
            # depth -= 1
            v = np.inf
            for a in self.actions(state):
                # print(f"     move1={action} board={state.board} player={state.to_move}\n utility={self.utility(state, state.to_move)}\n")
                v = min(v, max_value(self.result(state, a), alpha, beta, depth-1))

                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        def max_value(state, alpha, beta, depth):
            if self.terminal_test(state):
                return self.utility(state, player, depth)

            global boards
            boards+=1
            v = -np.inf
            for a in self.actions(state):

                v = max(v, min_value(self.result(state, a), alpha, beta, depth-1))

                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        bestScore = -np.inf
        beta = np.inf
        bestMove = None
        for a in game.actions(state):
            score = min_value(self.result(state, a), bestScore, beta,0)
            #print(f"key={a} score={score}", end="")

            if score > bestScore:
                bestScore = score
                bestMove = a
            #print(f"  bestScore={bestScore} bestMove={bestMove} board={state.board}")

        print(f"AI explored boards={boards}")
        return bestMove

    def minmax_decision(self, state, game):
        """Return the optimal action for the current player, using the Minimax algorithm."""
        player = state.to_move
        depth = 5
        global boards
        boards = 0
        #move = max(game.actions(state), key=lambda a: self.min_value(game.result(state, a), depth))
        move = max(game.actions(state), key=lambda a: self.min_value(game.result(state, a)))
        return move
    def minmax_decision2(self, state, game):
        """Return the optimal action for the current player, using the Minimax algorithm."""
        player = state.to_move
        depth = 0
        bestScore = -np.inf
        bestMove = None
        #move = max(game.actions(state), key=lambda a: self.min_value(game.result(state, a), depth))
        for move in game.actions(state):
            #self.log_info(f"key={move} board={state.board} depth={0}\n")
            score = self.min_value(game.result(state, move), depth)

            if score < bestScore:
                bestScore = score
                bestMove = move

        return bestMove
        """if player == 'X':
            return max(game.actions(state), key=lambda move: game.min_value(game.result(state, move)))
        else:
            return min(game.actions(state), key=lambda move: game.max_value(game.result(state, move)))
        """

    def play_game(self):
        state = self.initial
        while True:
            player = state.to_move
            print("Player", player, "'s turn")

            if player == 'X':
                move = query_player(self, state)
                #move = random_player(self, state)
            else:
                #move = self.minmax_decision(state, self)
                #move = alpha_beta_player(self, state)
                move = self.minmax_depth(state, self)
            state = self.result(state, move)
            print(f"{player} picked {move} utility={state.utility}\n")

            self.display(state)
            if self.terminal_test(state):
                print("Game over!")
                return self.utility(state, state.to_move)




    def play_game2(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                print(f'\nplayer: {state.to_move} move:', move)
                #print('\nplayer:', self.to_move(state))

                state = self.result(state, move)
                #print("resulting state: \nboard:  ", state.board)
                print("available moves:  ", state.moves)
                if self.terminal_test(state):
                    print("------------------")
                    self.display(state)

                    return self.compute_utility(state.board, self.to_move(self.initial))


if __name__ == '__main__':
    print("Let's play Quixo!")
    """board = [['X', 'X', 'X', 'O', ' '],
             ['O', 'X', 'O', ' ', ' '],
             ['O', ' ', 'X', ' ', ' '],
             ['O', ' ', ' ', ' ', ' '],
             ['O', ' ', ' ', ' ', 'X']]"""
    """board = [['X', 'X', 'X', ' '],
             ['O', 'X', 'O', ' '],
             ['O', ' ', 'X', ' '],
             ['O', ' ', 'O', ' ']]"""
    q = Quixo()
    #print(f"utility{q.compute_utility(board, 'X')}")
    #print(f"utility{q.compute_utility(board, 'O')}")
    #print(q.result(q.initial, (4,4)).utility)
    #print(q.initial)

    #utility = q.play_game(query_player, minmax_player) # computer moves first
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
    #utility = q.play_game(query_player, minmax_player) # computer moves first
