import numpy as np

from gamestate.gamestate import GameState
from game.game import Game
from game.tic_tac_toe import TicTacToe

def manual_player(game, state):
    """A manual player."""
    game.display(state)
    actions = game.actions(state)
    while True:
        action = input("Enter your move (e.g., 2,3): ")
        try:
            action = action.split(',')
            action = [int(v) for v in action]
            action = tuple(action)
            if action not in actions:
                print('invalid action!!')
            else:
                return action
        except:
            print('invalid action!!')

def minmax_player(game, state):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))

def random_player(game, state):
    """
    Randomly selects a move from the list of legal moves in the given game state.

    Args:
        game: The game object representing the game being played.
        state: The current state of the game.

    Returns:
        The randomly selected move.
    """
    legal_moves = game.actions(state)
    # count the number of legal moves
    num_legal_moves = len(legal_moves)
    # choose a random move
    random_move = np.random.randint(num_legal_moves)
    return game.actions(state)[random_move]

def alpha_beta_player(game, state):
    """
    Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states using alpha-beta pruning.

    Args:
        game: The game object representing the game being played.
        state: The current state of the game.
    
    Returns:
        The best move for the given state.
    """

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    alpha = -np.inf
    beta = np.inf
    best_score = -np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), alpha, beta)
        alpha = max(alpha, v)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action
 
