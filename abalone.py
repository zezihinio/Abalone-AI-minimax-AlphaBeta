from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class AbaloneGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 'B'  # 'B' pour Blanc, 'N' pour Noir
        self.depth = 3  # Profondeur de l'IA

    
    def initialize_board(self):
        # Initialise le plateau de jeu d'Abalone
        board = [['.' for _ in range(9)] for _ in range(9)]
        # Position initiale des billes blanches et noires
        positions = {
            'B': [(0, 6), (0, 7), (0, 8), 
                  (1, 5), (1, 6), (1, 7), (1, 8),
                  (2, 4), (2, 5), (2, 6), (2, 7), 
                  (3, 4), (3, 5), (3, 6)],            
            'N': [(5, 2), (5, 3), (5, 4), 
                  (6, 1), (6, 2), (6, 3), (6, 4),
                  (7, 0), (7, 1), (7, 2), (7, 3), 
                  (8, 0), (8, 1), (8, 2)]
        }
        for player, pos_list in positions.items():
            for x, y in pos_list:
                board[x][y] = player
        return board
    
    
    def is_over(self):
        # Vérifie si le jeu est terminé et retourne le gagnant
        count_B = sum(row.count('B') for row in self.board)
        count_N = sum(row.count('N') for row in self.board)
        if count_B <= 8:
            return 'N'
        elif count_N <= 8:
            return 'B'
        return False
    

    def get_legal_moves(self, player):
        # Retourne une liste des mouvements légaux pour un joueur donné
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x in range(9):
            for y in range(9):
                if self.board[x][y] == player:
                    for dx, dy in directions:
                        if self.is_legal_move(x, y, dx, dy):
                            moves.append((x, y, dx, dy))
        
        return moves

    def is_legal_move(self, x, y, dx, dy):
        # Vérifie si un mouvement est légal, incluant Sumito
        new_x, new_y = x + dx, y + dy
        if not (0 <= new_x < 9 and 0 <= new_y < 9):
            return False

        # Vérifie si la case de destination est vide
        if self.board[new_x][new_y] == '.':
            return True

        # Variables pour compter les pions alliés et adverses
        count_ally = 0
        count_opponent = 0
        temp_x, temp_y = x, y

        # Compte les billes alliées
        while 0 <= temp_x < 9 and 0 <= temp_y < 9 and self.board[temp_x][temp_y] == self.current_player:
            count_ally += 1
            temp_x += dx
            temp_y += dy

        # Compte les billes adverses
        while 0 <= temp_x < 9 and 0 <= temp_y < 9 and self.board[temp_x][temp_y] != self.current_player and self.board[temp_x][temp_y] != '.':
            count_opponent += 1
            temp_x += dx
            temp_y += dy

        # Vérifie si la poussée d'un adversaire est valide (Sumito)
        if count_ally > count_opponent and count_ally <= 3 and count_opponent != 0:
            if temp_x < 0 or temp_x >= 9 or temp_y < 0 or temp_y >= 9 or self.board[temp_x][temp_y] == '.':
                return True

        # Vérifie si la case de destination contient des alliés et permet de les pousser
        if self.board[new_x][new_y] == self.current_player:
            count_ally = 0
            temp_x, temp_y = new_x, new_y

            # Compte les billes alliées
            while 0 <= temp_x < 9 and 0 <= temp_y < 9 and self.board[temp_x][temp_y] == self.current_player:
                count_ally += 1
                temp_x += dx
                temp_y += dy

            # Vérifie si le mouvement est valide pour pousser les alliés
            if count_ally <= 3 and (temp_x < 0 or temp_x >= 9 or temp_y < 0 or temp_y >= 9 or self.board[temp_x][temp_y] == '.'):
                # Vérifie si les pions alliés se trouvent au bord et seraient poussés hors du plateau
                for i in range(1, count_ally + 1):
                    new_ally_x = new_x + i * dx
                    new_ally_y = new_y + i * dy
                    if not (0 <= new_ally_x < 9 and 0 <= new_ally_y < 9):
                        return False
                return True

        return False


    def apply_move(self, board, move):
        new_board = [row[:] for row in board]
        x, y, dx, dy = move
        new_x, new_y = x + dx, y + dy

        if new_board[new_x][new_y] == '.':
            new_board[new_x][new_y] = new_board[x][y]
            new_board[x][y] = '.'
        else:
            to_push = []
            temp_x, temp_y = x, y
            while 0 <= temp_x < 9 and 0 <= temp_y < 9 and new_board[temp_x][temp_y] != '.':
                to_push.append((temp_x, temp_y))
                temp_x += dx
                temp_y += dy

            for (px, py) in reversed(to_push):
                new_px, new_py = px + dx, py + dy
                if 0 <= new_px < 9 and 0 <= new_py < 9:
                    new_board[new_px][new_py] = new_board[px][py]
                new_board[px][py] = '.'

        return new_board


    def evaluate_board(self, board):
        """
    Evaluate the given board state and return a score based on various strategic criteria.
    Args:
        board (list): The current state of the game board.
    Returns:
        int: The evaluated score of the board.

    The evaluation is based on:
    1. Pushing opponent pieces off the board.
    2. Breaking opponent lines with own pieces.
    3. Covering own pieces to block opponent pushes.
    4. Prioritizing moves with 3 or 2 allied pieces.
    5. Moving pieces towards the center.

    Sub-functions:
        get_neighbors(x, y): Returns neighbors of a position on the board.
        in_bounds(x, y): Checks if a position is within board limits.
        check_push(x, y, dx, dy, player): Checks how many opponent and allied pieces can be pushed.
        evaluate_move(x, y, dx, dy, player, counters): Evaluates a move based on priority rules.
    """
        def get_neighbors(x, y):
            neighbors = []
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                if 0 <= x + dx < 9 and 0 <= y + dy < 9:
                    neighbors.append((x + dx, y + dy))
            return neighbors

        def in_bounds(x, y):
            return 0 <= x < 9 and 0 <= y < 9

        def check_push(x, y, dx, dy, player):
            opponent = 'B' if player == 'N' else 'N'
            ally_count = 0
            opponent_count = 0

            nx, ny = x, y
            while in_bounds(nx, ny) and board[nx][ny] == player:
                ally_count += 1
                nx += dx
                ny += dy

            while in_bounds(nx, ny) and board[nx][ny] == opponent:
                opponent_count += 1
                nx += dx
                ny += dy

            if ally_count > opponent_count and opponent_count > 0:
                return ally_count, opponent_count
            return ally_count, 0

        def evaluate_move(x, y, dx, dy, player, counters):
            score = 0
            ally_count, opponent_count = check_push(x, y, dx, dy, player)

            # 1. Pousser 2 pions adverses vers la sortie avec 3 pions alliés
            if ally_count >= 3 and opponent_count == 2:
                if not in_bounds(x + 3 * dx, y + 3 * dy):
                    score += 375
                    counters['1. Pousser 2 pions adverses vers la sortie avec 3 pions alliés'] += 1

            # 2. Pousser 1 pion adverse vers la sortie avec 3 ou 2 pions alliés
            elif (ally_count >= 2 and opponent_count == 1):
                if not in_bounds(x + 2 * dx, y + 2 * dy):
                    score += 350
                    counters['2. Pousser 1 pion adverse vers la sortie avec 3 ou 2 pions alliés'] += 1

            # 3. Pousser 2 ou 1 pions adverses pour casser une ligne avec 3 pions alliés
            elif ally_count == 3 and opponent_count in [1, 2]:
                score += 225
                counters['3. Pousser 2 ou 1 pions adverses pour casser une ligne avec 3 pions alliés'] += 1

            # 4. Pousser 1 pion adverses pour casser une ligne avec 2 pions alliés
            elif ally_count == 2 and opponent_count == 1:
                score += 220
                counters['4. Pousser 1 pion adverses pour casser une ligne avec 2 pions alliés'] += 1

            # 5. Pousser 2 ou 1 pions adverses avec 3 pions alliés
            elif ally_count == 3 and opponent_count in [1, 2]:
                score += 200
                counters['5. Pousser 2 ou 1 pions adverses avec 3 pions alliés'] += 1

            # 6. Pousser 1 pion adverse avec 2 pions alliés
            elif ally_count == 2 and opponent_count == 1:
                score += 175
                counters['6. Pousser 1 pion adverse avec 2 pions alliés'] += 1
            
            # 7. Couvrir un pion allié pour annuler une poussée adverse
            opponent = 'B' if player == 'N' else 'N'
            for nx, ny in get_neighbors(x, y):
                if board[nx][ny] == opponent:
                    for nnx, nny in get_neighbors(nx, ny):
                        if board[nnx][nny] == player:
                            score += 150
                            counters['7. Couvrir un pion allié pour annuler une poussée adverse'] += 1

            # 8. Privilégier les déplacements de 3 ou 2 pions alliés
            if ally_count == 3:
                score += 125
                counters['8. Privilégier les déplacements de 3 alliés'] += 1
            elif ally_count == 2:
                score += 100
                counters['8. Privilégier les déplacements de 2 alliés'] += 1

            # 9. Déplacer un pion vers le centre
            if ally_count == 1:
                score += (5 - max(abs(x - 4), abs(y - 4))) * 10
                counters['9. Déplacer un pion vers le centre'] += 1

            return score

        # Initialiser les compteurs
        counters = {
            '1. Pousser 2 pions adverses vers la sortie avec 3 pions alliés': 0,
            '2. Pousser 1 pion adverse vers la sortie avec 3 ou 2 pions alliés': 0,
            '3. Pousser 2 ou 1 pions adverses pour casser une ligne avec 3 pions alliés': 0,
            '4. Pousser 1 pion adverses pour casser une ligne avec 2 pions alliés': 0,
            '5. Pousser 2 ou 1 pions adverses avec 3 pions alliés': 0,
            '6. Pousser 1 pion adverse avec 2 pions alliés': 0,
            '7. Couvrir un pion allié pour annuler une poussée adverse': 0,
            '8. Privilégier les déplacements de 3 alliés': 0,
            '8. Privilégier les déplacements de 2 alliés': 0,
            '9. Déplacer un pion vers le centre': 0,
        }

        # Évaluation du plateau pour chaque position
        total_score = 0
        for x in range(9):
            for y in range(9):
                if board[x][y] in ['B', 'N']:
                    player = board[x][y]
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for dx, dy in directions:
                        total_score += evaluate_move(x, y, dx, dy, player, counters)

        return total_score, counters

    
    def minimaxalphabeta(self, board, depth, alpha, beta, maximizing_player):
        """
    Perform the minimax algorithm with alpha-beta pruning to find the optimal move for the current player.

    Args:
        board (list): The current state of the game board.
        depth (int): The maximum depth to search in the game tree.
        alpha (float): The alpha value for alpha-beta pruning, the best score the maximizer can guarantee.
        beta (float): The beta value for alpha-beta pruning, the best score the minimizer can guarantee.
        maximizing_player (bool): True if the current turn is for the maximizing player, False otherwise.
    Returns:
        float: The evaluated score of the board state at the current depth.
    The function works as follows:
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
        """
                
        winner = self.is_over()
        if depth == 0 or winner:
            if winner:
                return float('-inf') if winner == 'N' else float('inf')
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_legal_moves('B'):
                new_board = self.apply_move(board, move)
                eval = self.minimaxalphabeta(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    #print("lets break apha beta puring while max, beta = ", beta, " <= alpha = ", alpha)
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_legal_moves('N'):
                new_board = self.apply_move(board, move)
                eval = self.minimaxalphabeta(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    #print("lets break apha beta puring while mini, beta = ", beta, " <= alpha = ", alpha)
                    break
            return min_eval
    
    def current_player_is_ai(self):
        return self.current_player == 'N'

    def direction_to_name(self, dx, dy):
        """Convertit les coordonnées de direction en nom de direction."""
        for direction in Direction:
            if direction.value == (dx, dy):
                return direction.name
        return None

    def ai_move(self):   
        best_move = None
        best_value = float('-inf')
        print("AI Move computation started.")
        
        for move in self.get_legal_moves('N'):
            print(f"Evaluating move: {move}")
            new_board = self.apply_move(self.board, move)
            move_value, counters = self.evaluate_board(new_board)
            direction_name = self.direction_to_name(move[2], move[3])
            print(f"Move: ({move[0]}, {move[1]}, {direction_name}) has value: {move_value}")
            
            # Afficher les compteurs pour le mouvement évalué
            print("Counters for this move:")
            for key, value in counters.items():
                print(f"{key}: {value}")
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
                direction_name2 = self.direction_to_name(best_move[2], best_move[3])
        
        print(f"Best move: ({best_move[0]}, {best_move[1]}, {direction_name2}) with value: {best_value}")
        self.board = self.apply_move(self.board, best_move)


    def play(self):
        while True:
            self.display_board()
            self.display_remaining_pieces()
            
            winner = self.is_over()
            if winner:
                print(f"Game over ! Le joueur {winner} a gagné.")
                break
            
            if self.current_player == 'B':
                print("C'est au tour du joueur Blanc.")
                move = self.get_player_move()
                self.board = self.apply_move(self.board, move)
                self.current_player = 'N'
            else:
                print("C'est au tour de l'IA.")
                self.ai_move()
                self.current_player = 'B'


    def get_player_move(self):
        while True:
            try:
                input_move = input("Entrez votre mouvement (format: x y direction ou 'q' pour quitter): ")
                if input_move.lower() == 'q':
                    print("Game over.")
                    exit()
                x, y, direction = input_move.split()
                x, y = int(x), int(y)
                direction = Direction[direction.upper()]
                dx, dy = direction.value
                if self.is_legal_move(x, y, dx, dy):
                    return (x, y, dx, dy)
                else:
                    print("Mouvement illégal, essayez de nouveau.")
            except (ValueError, KeyError):
                print("Format invalide, essayez de nouveau.")
                    
    def display_board(self):
        # Couleurs ANSI
        RED = "\033[91m"
        BLUE = "\033[94m"
        RESET = "\033[0m"
        
        # Afficher les indices des colonnes
        print("    " + " ".join(str(i) for i in range(9)))
        for i, row in enumerate(self.board):
            # Afficher les indices des lignes
            print(f"{i:2}  ", end="")
            for cell in row:
                if cell == 'B':
                    print(RED + 'B' + RESET, end=" ")
                elif cell == 'N':
                    print(BLUE + 'N' + RESET, end=" ")
                else:
                    print(cell, end=" ")
            print()
        print()


    def display_remaining_pieces(self):
        count_B = sum(row.count('B') for row in self.board)
        count_N = sum(row.count('N') for row in self.board)
        print(f"Pions restants - Blancs (B): {count_B}, Noirs (N): {count_N}")

if __name__ == "__main__":
    game = AbaloneGame()
    game.play()
