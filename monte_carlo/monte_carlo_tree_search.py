import random
from collections import defaultdict
import numpy as np

class MCT_Node:
    """
    Represents a node in the Monte Carlo Tree Search algorithm.

    Attributes:
        - parent (MCT_Node): The parent node of this node.
        - state: The state associated with this node.
        - U (int): The U value of this node.
        - N (int): The N value of this node.
        - children (dict): A dictionary of child nodes.
        - actions: The actions associated with this node.
    """

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
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

def monte_carlo_tree_search(state, game, N=1000):
    """
    Perform Monte Carlo Tree Search to find the best move in a game.

    Args:
        - state: The current state of the game.
        - game: The game object that defines the game rules and actions.
        - N: The number of iterations to perform in the search (default: 1000).

    Returns:
        - The best move to play based on the Monte Carlo Tree Search.

    """
    def select(n):
        """
        Selects the child node with the highest UCB value recursively until a leaf node is reached.

        Parameters:
        - n: The current node to select from.

        Returns:
        - The selected node.

        """
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        """
        Expands the given node by creating child nodes for all possible actions.

        Args:
            - n (MCT_Node): The node to expand.

        Returns:
            - MCT_Node: The selected child node.
        """
        if not n.children and not game.terminal_test(n.state):
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                          for action in game.actions(n.state)}
        return select(n)

    def simulate(game, state):
        """
        Simulates a game from the given state until a terminal state is reached.
        Returns the utility value of the terminal state for the player.

        Parameters:
        - game: The game object representing the game being played.
        - state: The current state of the game.

        Returns:
        - The utility value of the terminal state for the player.
        """
        player = game.to_move(state)
        while not game.terminal_test(state):
            action = random.choice(list(game.actions(state)))
            state = game.result(state, action)
        v = game.utility(state, player)
        return -v

    def backpropagate(n, utility):
        """
        Backpropagates the utility value from a leaf node up to the root node.

        Args:
            - n (Node): The current node being backpropagated.
            - utility (float): The utility value to be backpropagated.
        """
        if utility > 0:
            n.U += utility
        n.N += 1

        if n.parent:
            backpropagate(n.parent, -utility)


    root = MCT_Node(state=state)

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backpropagate(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    return root.children.get(max_state)


