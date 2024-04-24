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
    while(True):

        print("\t\t\tΕργασία Μαθήματος Τεχνητής Νοημοσύνης")
        print("Τα ερωτήματα εκτελούνται σειριακά εκτός του ερωτήματος 3.1 που")
        print("είναι το παιχνίδι του manual player VS minimax για το Reversi.")
        print("Πληκτρολογήστε\n1 για τα ερωτήματα της τρίλιζας\n2 για τα ερωτήματα του Reversi\n3 για το ερώτημα 3.1 και έπειτα cntr+c για την διακοπή του.\nΟτιδήποτε άλλο για έξοδο\n")
        print("Which game would you like to play?\n (1) Tic Tac Toe\n (2) Reversi\n (3) Question 3.1")
        game_choice = input("Enter the number of the game you would like to play: ")

        if (game_choice== '1' or game_choice == '2' or game_choice == '3'):
            x_wins = 0
            o_wins = 0
            ties = 0
            if game_choice == '1':
                game = TicTacToe()
                print("\t\t\tΕρώτημα 2.1\n")
                x_wins = 0
                o_wins = 0
                ties = 0
                start_time = time.time()
                # minmax player VS random player
                for i in range(100):
                    
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
                
                print("X wins: ", x_wins/100 * 100, "%")
                print("O wins: ", o_wins / 100 * 100, "%")
                print("Ties: ", ties / 100 * 100, "%")
                print(f"Time elapsed:  {total_time:.2f} seconds\n")

                next_quest = input("\nΠατήστε οτιδήποτε για να συνεχίσετε στην επόμενη ερώτηση >> ")


                print("=============================================================================================")
                print("\nΕρώτημα 2.2 α-β player VS Random player")
                x_wins = 0
                o_wins = 0
                ties = 0

                # alpha beta player VS random player
                start_time = time.time()
                for i in range(100):
                    
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
                    
                print("X wins: ", x_wins/100 * 100, "%")
                print("O wins: ", o_wins / 100 * 100, "%")
                print("Ties: ", ties / 100 * 100, "%")
                print(f"Time elapsed:  {total_time:.2f} seconds\n")


                next_quest = input("\nΠατήστε οτιδήποτε για να συνεχίσετε στην επόμενη ερώτηση >> ")

                print("=============================================================================================")
                print("\nΕρώτημα 2.3 Monte Carlo player VS Random player")
                x_wins = 0
                o_wins = 0
                ties = 0
                
                # Monte Carlo tree search  player VS random player
                start_time = time.time()
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
                end_time = time.time()
                total_time = (end_time - start_time)
                
                print("X wins: ", x_wins/100 * 100, "%")
                print("O wins: ", o_wins / 100 * 100, "%")
                print("Ties: ", ties / 100 * 100, "%")
                
                print(f"Time elapsed:  {total_time:.2f} seconds\n")

                # break
        
            elif game_choice == '2':

                game = Reversi()
                print("Ερώτημα 3.2 Τυχαίος παίκτης εναντίον Τυχαίου παίκτη\n")
                start_time = time.time()
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

                end_time = time.time()
                total_time = (end_time - start_time)
                print("X wins: ", x_wins / 100 * 100, "%")
                print("O wins: ", o_wins / 100 * 100, "%")
                print("Ties: ", ties / 100 * 100, "%")
                print(f"Time elapsed:  {total_time:.2f} seconds\n")
                next_quest = input("\nΠατήστε οτιδήποτε για να συνεχίσετε στην επόμενη ερώτηση >> ")

                print("=============================================================================================")
                print("\nΕρώτημα 3.4 Πριόνισμα α-β με περιορισμό βάθους VS Random player\nΠαίρνει αρκετά λεπτά για να ολοκληρωθεί, περίπου 20 λεπτά\n")
                x_wins = 0
                o_wins = 0
                ties = 0
                start_time = time.time()
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

                end_time = time.time()
                total_time = (end_time - start_time) / 60
                print("X wins: ", x_wins/100 * 100, "%")
                print("O wins: ", o_wins / 100 * 100, "%")
                print("Ties: ", ties / 100 * 100, "%")
                print(f"Time elapsed:  {total_time:.2f} minutes\n")
                

                # break
            elif(game_choice=='3'):
                print("Ερώτημα 3.1 Παιχνίδι Reversi μεταξύ χειροκίνητου και minimax παίκτη\n")
                game = Reversi()
                x_wins = 0
                o_wins = 0
                ties = 0
                utility = game.play_game(manual_player, minmax_player)
                if utility == 1:
                        print("'X' won!")
                        x_wins += 1
                elif utility == -1:
                    print("'O' won!")
                    o_wins += 1
                else:
                    print('Tie!')
                    ties += 1

        else:
            print("Έξοδος...\n")
            break
        
    # print("X wins: ", x_wins/100 * 100, "%")
    # print("O wins: ", o_wins / 100 * 100, "%")
    # print("Ties: ", ties / 100 * 100, "%")
    # print(f"Time elapsed:  {total_time:.2f} minutes\n")
    
if __name__ == "__main__":
    main()
