"""
Tic Tac Toe Player
"""

from copy import deepcopy
import  math

X = "X"
O = "O"
EMPTY = None


# Helper functions

def get_diags(board):
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]


def get_columns(board):
    columns = []

    for i in range(3):
        columns.append([row[i] for row in board])

    return columns


def three_in_a_row(row):
    return True if row.count(row[0]) == 3 else False


def all_cells_filled(board):
    for row in board:
        if EMPTY in row:
            return False

    return True


def minimax_value(board, player, gameA, gameB):
    if terminal(board):
        return utility(board)

    if player == X:
        score = -math.inf

        for action in actions(board):
            score = max(score, minimax_value(result(board, action), O, gameA, gameB))

            gameA = max(gameA, score)

            if gameA >= gameB:
                break

        return score
    else:
        score = math.inf

        for action in actions(board):
            score = min(score, minimax_value(result(board, action), X, gameA, gameB))

            gameB = min(gameB, score)

            if gameA >= gameB:
                break

        return score


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counter_X = 0
    counter_O = 0

    for row in board:
        if X in row:
            counter_X += row.count(X)

        if O in row :
            counter_O += row.count(O)

    return X if counter_X <= counter_O else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    valid_actions = set()

    for i, row in enumerate(board):
        if EMPTY in row:
            for j, space in enumerate(row):
                if space is EMPTY:
                    valid_actions.add((i, j))

    return valid_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    
    copy_board = deepcopy(board)
    
    actioncurrent_player = player(copy_board)

    if copy_board[i][j] is not EMPTY:
        raise Exception("Action must be Invalid.")
    else:
        copy_board[i][j] = actioncurrent_player

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    rows = board + get_diags(board) + get_columns(board)

    for row in rows:
        actioncurrent_player = row[0]

        if actioncurrent_player is not None and three_in_a_row(row):
            return actioncurrent_player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return  True
    else:
        return all_cells_filled(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    best_move = None

    gameA = -math.inf
    gameB = math.inf

    if player(board) is X:
        score = -math.inf

        for action in actions(board):
            new_score = minimax_value(result(board, action),
                                  O, gameA, gameB)

            gameA = max(score, new_score)

            if new_score > score:
                score = new_score
                best_move = action

    else:
        score = math.inf

        for action in actions(board):
            new_score = minimax_value(result(board, action),
                                  X, gameA, gameB)

            gameB = min(score, new_score)

            if new_score < score:
                score = new_score
                best_move = action

    return best_move
