# Abalone Game with Minimax Algorithm and Alpha-Beta Pruning

This project implements the classic two-player board game Abalone using Python and Visual Studio Code. The game features an AI opponent powered by the Minimax algorithm with alpha-beta pruning optimization.

## Table of Contents
- [Installation](#installation)
- [Gameplay](#gameplay)
- [Features](#features)
- [How to Play](#how-to-play)
- [Algorithm Details](#algorithm-details)
- [License](#license)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/abalone-game.git
    cd abalone-game
    ```

2. **Set up a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Gameplay

Abalone is a two-player strategy game where the objective is to push the opponent's marbles off the board. This implementation includes an AI opponent using the Minimax algorithm with alpha-beta pruning.

## Features

- Classic Abalone board setup.
- AI opponent using Minimax algorithm with alpha-beta pruning.
- Evaluation function for strategic moves.
- Interactive console-based gameplay.

## How to Play

1. **Run the game:**
    ```sh
    python abalone.py
    ```

2. **Game Instructions:**
   - The board is displayed with coordinates.
   - Players take turns to move. The human player plays as 'B' (Blanc), and the AI plays as 'N' (Noir).
   - To make a move, input the coordinates of the marble to move and the direction (`UP`, `DOWN`, `LEFT`, `RIGHT`). For example: `2 4 RIGHT`.
   - The game ends when one player has fewer than 9 marbles remaining.

## Algorithm Details

### Minimax Algorithm with Alpha-Beta Pruning

The AI uses the Minimax algorithm enhanced with alpha-beta pruning to optimize decision-making. 
The `minimaxalphabeta`function Performs the minimax algorithm with alpha-beta pruning to find the optimal move for the current player. It return the evaluated score of the board state at the current depth.

#### The `minimaxalphabeta` function works as follows:
    1. If the game is over or the maximum depth is reached, return the evaluation of the board.
    2. If it's the maximizing player's turn:
        - Initialize the best evaluation to negative infinity.
        - For each legal move, apply the move, recursively call `minimaxalphabeta` with updated parameters, and update the best evaluation and alpha.
        - Perform alpha-beta pruning if alpha >= beta.
        - Return the best evaluation.
    3. If it's the minimizing player's turn:
        - Initialize the best evaluation to positive infinity.
        - For each legal move, apply the move, recursively call `minimaxalphabeta` with updated parameters, and update the best evaluation and beta.
        - Perform alpha-beta pruning if alpha >= beta.
        - Return the best evaluation.

The algorithm evaluates possible moves and selects the one with the highest score based on the following criteria:
1. Pushing opponent pieces off the board.
2. Breaking opponent lines with own pieces.
3. Covering own pieces to block opponent pushes.
4. Prioritizing moves with 3 or 2 allied pieces.
5. Moving pieces towards the center.

### Evaluation Function

The evaluation function assigns scores to board states based on strategic considerations:
- Higher scores for pushing opponent marbles off the board.
- Scores for breaking opponent lines or blocking pushes.
- Encouraging moves towards the center of the board.

