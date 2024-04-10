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