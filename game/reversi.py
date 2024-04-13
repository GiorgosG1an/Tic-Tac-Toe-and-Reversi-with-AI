"""
## reversi.py

This module contains the Reversi game implementation. Reversi is a strategy board game for two players, 
played on an 8×8 uncheckered board. Players take turns placing disks on the board with their assigned color 
facing up. During a play, any disks of the opponent's color that are in a straight line and bounded by the 
disk just placed and another disk of the current player's color are turned over to the current player's color.

The object of the game is to have the majority of disks turned to display your color when the last playable 
empty square is filled.

Classes:
- Reversi: This class represents a Reversi game. It inherits from the Game class and overrides its methods 
  to implement the Reversi game rules.

Authors: 
- Giannopoulos Georgios
- Giannopoulos Ioannis
"""
import numpy as np
from game.game import Game
from gamestate.gamestate import GameState
class Reversi(Game):
    """Play Reversi on an 8 x 8 board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'. Code
    adapted from http://inventwithpython.com/chapter15.html """

    def __init__(self):
        # Creates a brand new, blank board data structure.
        board = {}

        # Starting pieces:
        board[(3,3)] = 'X'
        board[(3,4)] = 'O'
        board[(4,3)] = 'O'
        board[(4,4)] = 'X'
        print(board)
        moves = self.getValidMoves(board, 'X')
        print(moves)
        self.initial = GameState(to_move='X', utility=0, board=board, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = self.getBoardCopy(state.board)
        tilesToFlip = self.isValidMove(board, state.to_move, move[0], move[1])
        board[(move[0],move[1])] = state.to_move
        for x, y in tilesToFlip:
            board[(x,y)] = state.to_move

        if state.to_move == 'X':
            moves = self.getValidMoves(board, 'O')
        else:
            moves = self.getValidMoves(board, 'X')
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return self.getValidMoves(state.board, state.to_move) == []

    def display(self, state):
        board = state.board
        valid_moves = set(state.moves)
        print(valid_moves)
        HLINE = '  +---+---+---+---+---+---+---+---+'
        VLINE = '  |   |   |   |   |   |   |   |   |'

        print('    1   2   3   4   5   6   7   8')
        print(HLINE)
        for y in range(8):
            print(VLINE)
            print(y+1, end=' ')
            for x in range(8):
                if (x,y) in board:
                    print('| %s' % (board[(x,y)]), end=' ')
                elif (x,y) in valid_moves:
                    print('| %s' % ('.'), end=' ')
                else:
                    print('| %s' % (' '), end=' ')
            print('|')
            print(VLINE)
            print(HLINE)

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if self.getValidMoves(board, player) == []:
            scores = self.getScoreOfBoard(board)
            if scores['X'] > scores['O']:
                return 1
            elif scores['X'] == scores['O']:
                return 0
            else:
                return -1
        else:
            return 0

    def getValidMoves(self, board, tile):
        # Returns a list of [x,y] lists of valid moves for the given player on the given board.
        validMoves = []

        for x in range(8):
            for y in range(8):
                if self.isValidMove(board, tile, x, y) != False:
                    validMoves.append((x, y))
        return validMoves

    def isValidMove(self, board, tile, xstart, ystart):
        # Returns False if the player's move on space xstart, ystart is invalid.
        # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
        if (xstart, ystart) in board or not self.isOnBoard(xstart, ystart):
            return False

        board[(xstart,ystart)] = tile # temporarily set the tile on the board.

        if tile == 'X':
            otherTile = 'O'
        else:
            otherTile = 'X'

        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection # first step in the direction
            y += ydirection # first step in the direction
            if self.isOnBoard(x, y) and (x,y) in board and board[(x,y)] == otherTile:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                while (x,y) in board and board[(x,y)] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self.isOnBoard(x, y):
                    continue
                if (x,y) in board and board[(x,y)] == tile:
                    # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        del board[(xstart,ystart)] # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    def isOnBoard(self, x, y):
        # Returns True if the coordinates are located on the board.
        return x >= 0 and x <= 7 and y >= 0 and y <=7

    def getBoardCopy(self, board):
        # Make a duplicate of the board list and return the duplicate.
        return {k: board[k] for k in board}

    def getScoreOfBoard(self, board):
        # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
        xscore = 0
        oscore = 0
        for k in board:
            if board[k] == 'X':
                xscore += 1
            if board[k] == 'O':
                oscore += 1
        return {'X':xscore, 'O':oscore}
    
    # ----------------- Start of heuristic functions -----------------

    def countTiles(self, board):
        """
        Counts the number of 'X' and 'O' tiles on the board and returns a percentage
        representing the dominance of one player over the other.

        Args:
            board (dict): A dictionary representing the game board, where the keys are
                          the positions and the values are the tiles ('X', 'O', or empty).

        Returns:
            float: The dominance percentage of the player with more tiles. If the number
                   of 'X' and 'O' tiles is equal, returns 0.

        """
        tiles_x = sum(1 for tile in board.values() if tile == 'X')
        tiles_o = sum(1 for tile in board.values() if tile == 'O')

        total_tiles = tiles_x + tiles_o

        if tiles_x > tiles_o:
            return 100 * tiles_x / total_tiles
        elif tiles_x < tiles_o:
            return 100 * tiles_o / total_tiles
        else:
            return 0
    
    def countCorners(self, board):
        """
        Counts the number of corners occupied by 'X' and 'O' on the board.

        Args:
            board (dict): The game board represented as a dictionary.

        Returns:
                The difference between the number of corners occupied by 'X' and 'O',
                multiplied by 25.

                ```python
                25 * (corners_x - corners_o)
                ```
        """
        corners_x = sum(1 for corner in [(0, 0), (0, 7), (7, 0), (7, 7)] if board.get(corner) == 'X')
        corners_o = sum(1 for corner in [(0, 0), (0, 7), (7, 0), (7, 7)] if board.get(corner) == 'O')

        return 25 * (corners_x - corners_o)
    
    def proximityCorners(self, board):
        """
        Calculates the proximity score based on the number of X and O tiles near the corners.

        Args:
            board (dict): A dictionary representing the game board.

        Returns:
            The proximity score calculated based on the difference between the number of X and O tiles near the corners.

            ```python
            -12.5 * (proximity_angle_x - proximity_angle_o)
            ```
        """
        proximity_angle_x = 0
        proximity_angle_o = 0

        # Define the squares enclosing each corner
        corners_enclosing_squares = {
            (0, 0): [(0, 1), (1, 0), (1, 1)],
            (0, 7): [(0, 6), (1, 7), (1, 6)],
            (7, 0): [(6, 0), (7, 1), (6, 1)],
            (7, 7): [(6, 7), (7, 6), (6, 6)]
        }

        for corner, enclosing_squares in corners_enclosing_squares.items():
            corner_tile = board.get(corner)
            if not corner_tile:  # If the corner is empty
                for square in enclosing_squares:
                    tile = board.get(square)
                    if tile == 'X':
                        proximity_angle_x += 1
                    elif tile == 'O':
                        proximity_angle_o += 1

        return -12.5 * (proximity_angle_x - proximity_angle_o)
    
    def calcMobility(self, state):
        """
        Calculates the mobility score for a given game state.

        Parameters:
        - state: The game state for which to calculate the mobility score.

        Returns:
        - The mobility score as a percentage.

        The mobility score is calculated by counting the number of valid moves for each player ('X' and 'O'), with the `getValidMoves()` method.
        The total number of moves is then used to calculate the percentage of moves available to the player with more moves.
        If both players have the same number of moves, the mobility score is 0.

        """
        moves_x = len(self.getValidMoves(state.board, 'X'))
        moves_o = len(self.getValidMoves(state.board, 'O'))

        total_moves = moves_x + moves_o

        if moves_x > moves_o:
            return 100 * moves_x / total_moves
        elif moves_x < moves_o:
            return 100 * moves_o / total_moves
        else:
            return 0
        
    

    def calcDiscs(self, board):
        """
        Calculates the total weight of discs on the board based on a predefined weight matrix.

        Args:
            board (dict): A dictionary representing the game board, where the keys are (row, col) tuples and the values are the disc types ('X' or 'O').

        Returns:
            int: The difference between the total weight of 'X' discs and 'O' discs on the board.
        """
        WEIGHT_MATRIX = [
            [20, -3, 11,  8,  8, 11, -3, 20],
            [-3, -7, -4,  1,  1, -4, -7, -3],
            [11, -4,  2,  2,  2,  2, -4, 11],
            [ 8,  1,  2, -3, -3,  2,  1,  8],
            [ 8,  1,  2, -3, -3,  2,  1,  8],
            [11, -4,  2,  2,  2,  2, -4, 11],
            [-3, -7, -4,  1,  1, -4, -7, -3],
            [20, -3, 11,  8,  8, 11, -3, 20]
        ]
        total_weight_x = 0
        total_weight_o = 0

        for row in range(8):
            for col in range(8):
                tile = board.get((row, col))
                if tile == 'X':
                    total_weight_x += WEIGHT_MATRIX[row][col]
                elif tile == 'O':
                    total_weight_o += WEIGHT_MATRIX[row][col]

        return total_weight_x - total_weight_o
    
    def heuristic_score(self, state):
        """
        Calculates the heuristic score for a given game state.

        The heuristic score is calculated by combining different terms with weights.
        The terms include the number of tiles, the number of corners, the proximity to corners,
        the mobility, and the number of discs on the board.

        Args:
            state (GameState): The game state for which to calculate the heuristic score.

        Returns:
            float: The heuristic score for the given game state, positive for the `X player` and negative for 
             the `O player`.
        """

        tiles_term = self.countTiles(state.board)
        corners_term = self.countCorners(state.board)
        proximity_corners_term = self.proximityCorners(state.board)
        mobility_term = self.calcMobility(state)
        discs_term = self.calcDiscs(state.board)

        # Linear combination of terms with weights
        score = (10 * tiles_term +
                 801.724 * corners_term +
                 382.026 * proximity_corners_term +
                 78.922 * mobility_term +
                 10 * discs_term)

        # Adjust the score based on the player's turn
        if state.to_move == 'X':
            return score
        else:
            return -score
        
    def alpha_beta_cutoff_search(self, state, depth=3):
        """
        Performs an alpha-beta cutoff search to find the best action for the given state.

        Args:
            state: The current state of the game.
            depth (optional): The maximum depth to search in the game tree. Defaults to 3.

        Returns:
            The best action to take based on the alpha-beta cutoff search.

        """
        player = self.to_move(state)

        def max_value(state, alpha, beta, depth):
            if self.terminal_test(state) or depth == 0:
                return self.heuristic_score(state)
            v = -np.inf
            for a in self.actions(state):
                v = max(v, min_value(self.result(state, a), alpha, beta, depth - 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth):
            if self.terminal_test(state) or depth == 0:
                return self.heuristic_score(state)
            v = np.inf
            for a in self.actions(state):
                v = min(v, max_value(self.result(state, a), alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        alpha = -np.inf
        beta = np.inf
        best_score = -np.inf
        best_action = None
        for a in self.actions(state):
            v = min_value(self.result(state, a), alpha, beta, depth)
            alpha = max(alpha, v)
            if v > best_score:
                best_score = v
                best_action = a

        return best_action