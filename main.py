"""
## main.py

This module is the entry point of the application. It allows the user to choose between two games: Tic Tac Toe and Reversi. 
The games are played 100 times, with different player strategies. The results (number of wins for each player and ties) are 
then printed out.

The module imports the necessary classes and functions from the gamestate, game, and players modules.

Functions:
- main(): The main function of the module. It handles the game choice, plays the games, and prints out the results.

This module is part of a first semester project in Artificial Intelligence at University of Peloponnese, 
Department of Informatics and Telecommunications.

Authors: 
- Giannopoulos Georgios
- Giannopoulos Ioannis
"""
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
