from gamestate.gamestate import GameState
from game.game import Game
from game.tic_tac_toe import TicTacToe
from game.reversi import Reversi
from players.players import manual_player, minmax_player, random_player, alpha_beta_player

def main():

    print("Which game would you like to play?\n (1) Tic Tac Toe\n (2) Reversi")
    
    while(True):
        game_choice = input("Enter the number of the game you would like to play: ")
        if game_choice == '1':
            game = TicTacToe()
            utility = game.play_game(alpha_beta_player, random_player)
            if utility == 1:
                print("'X' won!")
            elif utility == -1:
                print("'O' won!")
            else:
                print('Tie!')
            return
        elif game_choice == '2':
            game = Reversi()

            utility = game.play_game(manual_player, random_player)
            if utility == 1:
                print("'X' won!")
            elif utility == -1:
                print("'O' won!")
            else:
                print('Tie!')
            return
        else:
            print("Invalid choice.\n")
    
if __name__ == "__main__":
    main()
