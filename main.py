from gamestate.gamestate import GameState
from game.game import Game
from game.tic_tac_toe import TicTacToe
from game.reversi import Reversi
from players.players import manual_player, minmax_player, random_player, alpha_beta_player, mcts_player
# from monte_carlo.monte_carlo_tree_search import MCTS

def main():
    x_wins = 0
    o_wins = 0
    ties = 0

    print("Which game would you like to play?\n (1) Tic Tac Toe\n (2) Reversi")
    
    while(True):
        game_choice = input("Enter the number of the game you would like to play: ")

        if game_choice == '1':
            game = TicTacToe()
            
            for i in range(100):

                utility = game.play_game(mcts_player, random_player)

                if utility == 1:
                    print("'X' won!")
                    x_wins += 1
                elif utility == -1:
                    print("'O' won!")
                    o_wins += 1
                else:
                    print('Tie!')
                    ties += 1

            break
    
        elif game_choice == '2':

            game = Reversi()

            for i in range(100):

                utility = game.play_game(random_player, random_player)

                if utility == 1:
                    print("'X' won!")
                    x_wins += 1
                elif utility == -1:
                    print("'O' won!")
                    o_wins += 1
                else:
                    print('Tie!')
                    ties += 1

            break

        else:
            print("Invalid choice.\n")
        
    print("X wins: ", x_wins)
    print("O wins: ", o_wins)
    print("Ties: ", ties)
    
if __name__ == "__main__":
    main()
