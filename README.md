# Tic Tac Toe Game
This is a simple implementation of the classic game Tic Tac Toe in Python. The game is played on a 3x3 grid by two players, one using 'X' and the other using 'O'. The player who first gets 3 of their marks in a row (up, down, across, or diagonally) is the winner.
--- 
## Project Structure
The project is structured as follows:
```
.gitignore
game/
    game.py
    tic_tac_toe.py
gamestate/
    gamestate.py
main.py
players/
    players.py
```
## Key files
- `main.py`: This is the entry point of the game. It creates a new game and starts it with two players: `minmax_player` and `manual_player`.
- `game/tic_tac_toe.py`: This file contains the `TicTacToe` class which extends the `Game` class. It defines the rules of the game, how to display the game state, and how to calculate the utility of a game state.
- `gamestate/gamestate.py`: This file defines the `GameState` class which represents the state of a game at a certain point in time.
- `players/players.py`: This file defines the `manual_player` and `minmax_player` classes which represent two types of players that can play the game.
