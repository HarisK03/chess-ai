# Chess AI #

## About The Project ##

This application is an implementation of Chess AI in Python. Two AI methods are used independently.

![alt text](https://github.com/HarisK03/chess-ai/blob/readme/chess.png)

## Implementing The Game ##
The [python-chess](https://github.com/niklasf/python-chess) library is used to implement the basics of move calculation and game state monitoring. The game engine [Komodo](https://github.com/michaeldv/donna_opening_books/blob/master/komodo.bin) is used to provide an opening book for the first few moves that are played.

## Minimax Algorithm ##
The Minimax algorithm is a decision-making algorithm commonly used in game theory and artificial intelligence for two-player zero-sum games. There are various factors used in evaluating a position:
1. The piece position
2. The depth of the evaluation
3. Doubled/blocked/isolated pawns
4. Material in play versus material captured 

## Monte Carlo Tree Search (MCTS) Algorithm ##
Monte Carlo Tree Search (MCTS) is a heuristic search algorithm used in decision-making and is particularly effective in game-playing AI. The four steps of the MCTS are as follows:
1. **Selection**: Choose the most promising node by balancing exploration and exploitation based on historical statistics.
2. **Expansion**: Expand the selected node by generating potential child nodes representing possible actions or future states.
3. **Simulation** (Rollout): Simulate games or actions from the expanded nodes to assess potential outcomes until reaching a terminal state.
4. **Backpropagation**: Update statistics (such as wins and visits) for the nodes traversed during selection and simulation to refine future decision-making.

## Contact ##

Haris Kamal - HarisKamal03@gmail.com

Project Link - https://github.com/HarisK03/chess-ai
