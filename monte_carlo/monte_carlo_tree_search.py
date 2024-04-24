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
    # Check if the node has children
    if node.children:

        child_nodes = node.children.keys()
        ucb_value = lambda child: ucb(child)
        # Select the child node with the highest UCB value
        best_child = max(child_nodes, key=ucb_value)

        return select(best_child)
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
    # Check if the node has no children and the game is not in a terminal state
    if not node.children and not game.terminal_test(node.state):
        # Initialize an empty dictionary for the children
        node.children = {}
        
        # Get all possible actions from the current state
        actions = game.actions(node.state)
        # For each action, create a new MCTNode with the resulting state and the current node as the parent
        # Then, add the new node to the children dictionary with the action as the key
        for action in actions:
            new_state = game.result(node.state, action)
            new_node = MCTNode(state=new_state, parent=node)
            node.children[new_node] = action


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

    # loop until the game reaches a terminal state
    while not game.terminal_test(state):
        # Choose a random action 
        action = random.choice(list(game.actions(state)))
        # Get the new state after taking the action
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
        # add the utility to the total utility of the node
        node.U += utility
    # increment the number of visits to the node
    node.N += 1
    # check if the node has a parent
    if node.parent:
        # backpropagate the utility to the parent node
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
        # select a leaf node
        leaf = select(root)
        # expand the leaf node
        child = expand(leaf, game)
        # simulate the game from the child node
        result = simulate(game, child.state)
        # Backpropagate the result of the simulation up the tree to update the total utility and visit count of each node
        backpropagate(child, result)

    # return the child node with the highest number of visits
    max_state = max(root.children, key=lambda p: p.N)
    return root.children.get(max_state)




