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
from players.players import manual_player, minmax_player, random_player, alpha_beta_player, mcts_player, alpha_beta_cutoff_player
import time

def main():
    x_wins = 0
    o_wins = 0
    ties = 0

    print("Which game would you like to play?\n (1) Tic Tac Toe\n (2) Reversi")
    
    while(True):
        game_choice = input("Enter the number of the game you would like to play: ")

        if game_choice == '1':
            game = TicTacToe()

            start_time = time.time()
            # minmax player VS random player
            for i in range(10):
                

                utility = game.play_game(minmax_player, random_player)

                if utility == 1:
                    print("'X' won!")
                    x_wins += 1
                elif utility == -1:
                    print("'O' won!")
                    o_wins += 1
                else:
                    print('Tie!')
                    ties += 1
            end_time = time.time()
            total_time = (end_time - start_time)
            
            print("X wins: ", x_wins/10 * 100, "%")
            print("O wins: ", o_wins / 10 * 100, "%")
            print("Ties: ", ties / 10 * 100, "%")
            print(f"Time elapsed:  {total_time:.2f} seconds\n")

            x_wins = 0
            o_wins = 0
            ties = 0

            # alpha beta player VS random player
            for i in range(10):
                start_time = time.time()
                utility = game.play_game(alpha_beta_player, random_player)
    
                if utility == 1:
                    print("'X' won!")
                    x_wins += 1
                elif utility == -1:
                    print("'O' won!")
                    o_wins += 1
                else:
                    print('Tie!')
                    ties += 1
            end_time = time.time()
            total_time = (end_time - start_time)
                
            print("X wins: ", x_wins/10 * 100, "%")
            print("O wins: ", o_wins / 10 * 100, "%")
            print("Ties: ", ties / 10 * 100, "%")
            print(f"Time elapsed:  {total_time:.2f} seconds\n")

            x_wins = 0
            o_wins = 0
            ties = 0
            
            # Monte Carlo tree search  player VS random player
            start_time = time.time()
            for i in range(10):
                
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
            end_time = time.time()
            total_time = (end_time - start_time)
               
            print("X wins: ", x_wins/10 * 100, "%")
            print("O wins: ", o_wins / 10 * 100, "%")
            print("Ties: ", ties / 100 * 10, "%")
            
            print(f"Time elapsed:  {total_time:.2f} seconds\n")

            break
    
        elif game_choice == '2':

            game = Reversi()

            for i in range(100):

                utility = game.play_game(alpha_beta_cutoff_player, random_player)

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
        
    print("X wins: ", x_wins/100 * 100, "%")
    print("O wins: ", o_wins / 100 * 100, "%")
    print("Ties: ", ties / 100 * 100, "%")
    
if __name__ == "__main__":
    main()
