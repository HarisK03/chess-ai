"""
Chess move search using the Monte Carlo Tree Search Algorithm.
"""

from __future__ import annotations
import chess
import math
import random


class Node:
    """
    A node.

    Public Attributes:
    ==========
    state: the board state of the node
    parent: the parent of the node
    move: the best move from this state
    visits: number of times the node has been visited
    wins: number of wins from this node
    children: the list of children Nodes
    """

    def __init__(self, state: chess.Board, parent: Node = None, move: chess.Move = None) -> None:
        """
        Intialize a node with the given parameters.
        """
        self.state = state
        self.parent = parent
        self.move = move
        self.visits = 0
        self.wins = 0
        self.children = []

    def select(self) -> Node:
        """
        Select a node.
        """
        node = self
        while node.children:
            unexplored_children = [
                child for child in node.children if child.visits == 0]
            if unexplored_children:
                return random.choice(unexplored_children)
            else:
                node = max(node.children, key=lambda child: child.wins / child.visits +
                           1.4 * math.sqrt(math.log(child.parent.visits + 1) / (child.visits + 1)))
        return node

    def expand(self) -> None:
        """
        Expand the node.
        """
        legal_moves = list(self.state.legal_moves)
        for move in legal_moves:
            state = self.state.copy()
            state.push(move)
            self.children.append(Node(state, self, move))

    def simulate(self) -> int:
        """
        Simulate/rollout a random game from the state.
        """
        state = self.state.copy()
        while not state.is_game_over():
            legal_moves = list(state.legal_moves)
            state.push(random.choice(legal_moves))
        result = state.result()
        if result == "1-0":
            return 1
        elif result == "0-1":
            return -1
        return 0

    def backpropagate(self, result) -> None:
        """
        Backpropogate the result to the other nodes.
        """
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)


class MCTS:
    """
    A MCTS class to perform search operations.
    """

    def __init__(self, state: chess.Board) -> None:
        """
        Intialize the MCTS with the root node.
        """
        self.root = Node(state)

    def run(self, iterations: int) -> None:
        """
        Peform iterations from the root node.
        """
        for _ in range(iterations):
            # defined order for MCTS
            node = self.root.select()
            node.expand()
            result = node.simulate()
            node.backpropagate(result)

    def best_move(self, color: chess.Color) -> chess.Move:
        """
        Return the best move found during the MCTS.
        """
        if color == chess.WHITE:
            return max(self.root.children, key=lambda child: child.visits).move
        return min(self.root.children, key=lambda child: child.visits).move


# Pick moves using the MCTS
# Play a game until a player loses
if __name__ == "__main__":
    state = chess.Board()

    while not state.is_game_over():
        mcts = MCTS(state)
        mcts.run(1000)  # search for 1000 iterations
        best_move = mcts.best_move(state.turn)
        state.push(best_move)

        print(state)  # visualize the board to stdout
