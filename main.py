from gamestate.gamestate import GameState
from game.game import Game
from game.tic_tac_toe import TicTacToe
from players.players import manual_player, minmax_player, random_player

def main():
    game = TicTacToe()
    utility = game.play_game(minmax_player, random_player)
    if utility == 1:
        print("'X' won!")
    elif utility == -1:
        print("'O' won!")
    else:
        print('Tie!')


if __name__ == "__main__":
    main()
