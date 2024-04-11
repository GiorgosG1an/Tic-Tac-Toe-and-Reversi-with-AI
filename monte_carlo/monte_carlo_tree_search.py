"""
## monte_carlo_tree_search.py

This module contains the implementation of the Monte Carlo Tree Search (MCTS) algorithm. MCTS is a 
heuristic search algorithm used in decision processes, most notably in Artificial Intelligence (AI) 
applications such as games.

Classes:
- MCTNode: Represents a node in the Monte Carlo Tree Search algorithm.

Functions:
- ucb(n, C=1.4): Calculates the Upper Confidence Bound (UCB) for a node.
- select(node): Selects the child node with the highest UCB value recursively until a leaf node is reached.
- expand(node, game): Expands the given node by creating child nodes for all possible actions in the game.
- simulate(game, state): Simulates a game from the given state until a terminal state is reached.
- backpropagate(node, utility): Backpropagates the utility value from a leaf node up to the root node.
- monte_carlo_tree_search(state, game, iterations=1000): Performs the MCTS algorithm to find the best move in a game.

Authors: 
- Giannopoulos Georgios
- Giannopoulos Ioannis
"""
import random
import numpy as np

class MCTNode:
    """
    Represents a node in the Monte Carlo Tree Search algorithm.

    Attributes:
        - parent (MCTNode): The parent node of this node.
        - state: The state associated with this node.
        - U (int): The U value of this node.
        - N (int): The N value of this node.
        - children (dict): A dictionary of child nodes.
        - actions: The actions associated with this node.
    """

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.parent = parent
        self.state = state
        self.U = U
        self.N = N
        self.children = {}
        self.actions = None


def ucb(n, C=1.4):
    """
    Upper Confidence Bound (UCB) formula for Monte Carlo Tree Search.

    Parameters:
    - n: Node object representing the current node in the search tree.
    - C: Exploration constant. Default value is 1.4.

    Returns:
    - The UCB value for the given node.

    Formula:
    `UCB = U / N + C * sqrt(log(parent.N) / N)`

    where:
    - U: Total reward of the node.
    - N: Number of times the node has been visited.
    - parent.N: Number of times the parent node has been visited.
    - C: Exploration constant.
    """
    if n.N == 0:
        return np.inf
    else:
        ucb_calc = n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)

    return ucb_calc

def select(node):
    """
    Selects the child node with the highest UCB value recursively until a leaf node is reached.

    Args:
        - node (Node): The current node in the tree.

    Returns:
        - Node: The selected leaf node.
    """
    if node.children:
        return select(max(node.children.keys(), key=lambda child: ucb(child)))
    else:
        return node

def expand(node, game):
    """
    Expands the given node by creating child nodes for all possible actions in the game.

    Args:
        - node (MCTNode): The node to expand.
        - game: The game object representing the current state of the game.

    Returns:
        - The selected child node.
    """
    if not node.children and not game.terminal_test(node.state):
        node.children = {MCTNode(state=game.result(node.state, action), parent=node): action
                         for action in game.actions(node.state)}
    return select(node)

def simulate(game, state):
    """
    Simulates a game from the given state until a terminal state is reached.
    Returns the utility value of the terminal state for the player.

    Parameters:
    - game: The game object representing the rules of the game.
    - state: The current state of the game.

    Returns:
    - The utility value of the terminal state for the player.
    """

    player = game.to_move(state)
    while not game.terminal_test(state):
        action = random.choice(list(game.actions(state)))
        state = game.result(state, action)
    return -game.utility(state, player)

def backpropagate(node, utility):
    """
    Backpropagates the utility value from a leaf node up to the root node.

    Args:
        - node (Node): The current node being backpropagated.
        - utility (float): The utility value to be backpropagated.
    """
    if utility > 0:
        node.U += utility
    node.N += 1
    if node.parent:
        backpropagate(node.parent, -utility)

def monte_carlo_tree_search(state, game, iterations=1000):
    """
    Performs Monte Carlo Tree Search algorithm to find the best move in a game.

    Args:
        - state: The current state of the game.
        - game: The game object that provides the necessary methods for game simulation.
        - iterations: The number of iterations to perform during the search (default=1000).

    Returns:
        The best move found by the Monte Carlo Tree Search algorithm.
    """

    root = MCTNode(state=state)

    for _ in range(iterations):
        leaf = select(root)
        child = expand(leaf, game)
        result = simulate(game, child.state)
        backpropagate(child, result)

    max_state = max(root.children, key=lambda p: p.N)
    return root.children.get(max_state)




