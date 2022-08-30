# Klasse, die einen regulären Schachzug kapselt
class Move:
    def __init__(self, from_pos : tuple, to_pos : tuple):
        self.fr = from_pos
        self.to = to_pos
        self.captured = None
        self.first_move = False
        self.undone_advanced_two_last_move = None
        self.hash_before = None
    
    def __str__(self):
        return f"{chr(self.fr[0] + 65)}{self.fr[1] + 1} -> {chr(self.to[0] + 65)}{self.to[1] + 1}"
    
    def __eq__(self, o):
        if not type(o) is Move:
            return False
        
        return self.fr == o.fr and self.to == o.to and self.first_move == o.first_move and self.captured == o.captured

# Oberklasse für alle Figuren
class Piece:
    def __init__(self, color : int, pos : tuple):
        if color != 0 and color != 1:
            raise ValueError("color must be 0 or 1")
            
        self.color = color
        self.pos = pos
        self.moved = False
    
    def __eq__(self, o):
        if not type(self) is type(o):
            return False
        
        return self.color == o.color and self.pos == o.pos and self.moved == o.moved
    
    # Aktualisiert dias first_move-Attribut in allen Zügen in der Liste
    def set_first_move_in_list(self, moves : list):
        for move in moves:
            move.first_move = not self.moved

    # gibt alle möglichen horizontalen oder vertikalen Züge zurück(mit unendlicher Distanz)
    def get_straight_moves(self, board : list) -> list:
        moves = []

        # Horizontal
        for x in range(self.pos[0] + 1, 8):
            if board[x][self.pos[1]] != None:
                if board[x][self.pos[1]].color != self.color:
                    move = Move(self.pos, (x, self.pos[1]))
                    move.captured = board[x][self.pos[1]]
                    moves.append(move)
                break
            moves.append(Move(self.pos, (x, self.pos[1])))
        
        for x in range(self.pos[0] - 1, -1, -1):
            if board[x][self.pos[1]] != None:
                if board[x][self.pos[1]].color != self.color:
                    move = Move(self.pos, (x, self.pos[1]))
                    move.captured = board[x][self.pos[1]]
                    moves.append(move)
                break
            moves.append(Move(self.pos, (x, self.pos[1])))
        
        # Vertikal
        for y in range(self.pos[1] + 1, 8):
            if board[self.pos[0]][y] != None:
                if board[self.pos[0]][y].color != self.color:
                    move = Move(self.pos, (self.pos[0], y))
                    move.captured = board[self.pos[0]][y]
                    moves.append(move)
                break
            moves.append(Move(self.pos, (self.pos[0], y)))

        for y in range(self.pos[1] - 1, -1, -1):
            if board[self.pos[0]][y] != None:
                if board[self.pos[0]][y].color != self.color:
                    move = Move(self.pos, (self.pos[0], y))
                    move.captured = board[self.pos[0]][y]
                    moves.append(move)
                break
            moves.append(Move(self.pos, (self.pos[0], y)))

        self.set_first_move_in_list(moves)

        return moves
    
    # gibt alle möglichen diagonalen Züge zurück(mit unendlicher Distanz)
    def get_diagonal_moves(self, board : list) -> list:
        moves = []

        for x in range(1, 8):
            if self.pos[0] + x > 7 or self.pos[1] + x > 7:
                break
            if board[self.pos[0] + x][self.pos[1] + x] != None:
                if board[self.pos[0] + x][self.pos[1] + x].color != self.color:
                    move = Move(self.pos, (self.pos[0] + x, self.pos[1] + x))
                    move.captured = board[self.pos[0] + x][self.pos[1] + x]
                    moves.append(move)
                break
            moves.append(Move(self.pos, (self.pos[0] + x, self.pos[1] + x)))
        
        for x in range(1, 8):
            if self.pos[0] - x < 0 or self.pos[1] - x < 0:
                break
            if board[self.pos[0] - x][self.pos[1] - x] != None:
                if board[self.pos[0] - x][self.pos[1] - x].color != self.color:
                    move = Move(self.pos, (self.pos[0] - x, self.pos[1] - x))
                    move.captured = board[self.pos[0] - x][self.pos[1] - x]
                    moves.append(move)
                break
            moves.append(Move(self.pos, (self.pos[0] - x, self.pos[1] - x)))
        
        for x in range(1, 8):
            if self.pos[0] + x > 7 or self.pos[1] - x < 0:
                break
            if board[self.pos[0] + x][self.pos[1] - x] != None:
                if board[self.pos[0] + x][self.pos[1] - x].color != self.color:
                    move = Move(self.pos, (self.pos[0] + x, self.pos[1] - x))
                    move.captured = board[self.pos[0] + x][self.pos[1] - x]
                    moves.append(move)
                break
            moves.append(Move(self.pos, (self.pos[0] + x, self.pos[1] - x)))
        
        for x in range(1, 8):
            if self.pos[0] - x < 0 or self.pos[1] + x > 7:
                break
            if board[self.pos[0] - x][self.pos[1] + x] != None:
                if board[self.pos[0] - x][self.pos[1] + x].color != self.color:
                    move = Move(self.pos, (self.pos[0] - x, self.pos[1] + x))
                    move.captured = board[self.pos[0] - x][self.pos[1] + x]
                    moves.append(move)
                break
            moves.append(Move(self.pos, (self.pos[0] - x, self.pos[1] + x)))

        self.set_first_move_in_list(moves)

        return moves

    def get_moves(self, board : list) -> list:
        raise NotImplementedError("get_moves not implemented on " + str(type(self)))

    # überprüft, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square(self, square : tuple, board : list) -> bool:
        for move in self.get_moves(board):
            if move.to == square:
                return True
        
        return False
    
    # überprüft auf einem leeren Schachfeld, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square_on_empty_board(self, square : tuple) -> bool:
        raise NotImplementedError("attacks_square_on_empty_board not implemented on " + str(type(self)))


# Klasse, die einen Rochadenzug kapselt
class Castling_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple, castling_rook_fr : tuple, castling_rook_to : tuple):
        super().__init__(from_pos, to_pos)
        self.castling_rook_fr = castling_rook_fr
        self.castling_rook_to = castling_rook_to
    
    def __eq__(self, o):
        if not type(o) is Castling_Move:
            return False
        
        return self.fr == o.fr and self.to == o.to and self.castling_rook_fr == o.castling_rook_fr and self.castling_rook_to == o.castling_rook_to and self.first_move == o.first_move
    
    def __str__(self):
        return super().__str__()

# Klasse, die einen En Passant Zug kapselt
class En_Passant_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple, en_passant_pos : tuple):
        super().__init__(from_pos, to_pos)
        self.en_passant_pos = en_passant_pos
    
    def __eq__(self, o):
        if not type(o) is En_Passant_Move:
            return False
        
        return self.fr == o.fr and self.to == o.to and self.en_passant_pos == o.en_passant_pos and self.captured == o.captured
    
    def __str__(self):
        return super().__str__()

# Klasse, die eine Bauernaufwertung kapselt
class Promotion_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple, promotion_piece : Piece, promoted_piece : Piece):
        super().__init__(from_pos, to_pos)
        self.promotion_piece = promotion_piece
        self.promoted_piece = promoted_piece
    
    def __str__(self):
        return f"{super().__str__()} -> {type(self.promotion_piece).__name__}"
    
    def __eq__(self, o):
        if not type(o) is Promotion_Move:
            return False
        
        return self.fr == o.fr and self.to == o.to and type(self.promotion_piece) == type(o.promotion_piece) and self.captured == o.captured

# Klasse, die einen Doppelzug eines Bauern kapselt
class Pawn_Double_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple):
        super().__init__(from_pos, to_pos)
    
    def __eq__(self, o):
        if not type(o) is Pawn_Double_Move:
            return False
        
        return self.fr == o.fr and self.to == o.to
    
    def __str__(self):
        return super().__str__()

# Bauer
class Pawn(Piece):
    def __init__(self, color : int, pos : tuple):
        super().__init__(color, pos)
        # relevant für En Passant
        self.advanced_two_last_move = False

    def __eq__(self, o):
        if not type(self) is type(o):
            return False
        
        return self.color == o.color and self.pos == o.pos and self.moved == o.moved and self.advanced_two_last_move == o.advanced_two_last_move

    def get_moves(self, board : list) -> list:
        moves = []

        forward = 1 if self.color == 0 else -1

        pos_y = self.pos[1] + forward
        pos_2y = self.pos[1] + 2 * forward

        if board[self.pos[0]][pos_y] == None:
            moves.append(Move(self.pos, (self.pos[0], pos_y)))

            # Erster Zug vom Bauern
            if not self.moved:
                if board[self.pos[0]][pos_2y] == None:
                    moves.append(Pawn_Double_Move(self.pos, (self.pos[0], pos_2y)))
            
        # Schlagen
        if self.pos[0] > 0 and board[self.pos[0] - 1][pos_y] != None and board[self.pos[0] - 1][pos_y].color != self.color:
            move = Move(self.pos, (self.pos[0] - 1, pos_y))
            move.captured = board[self.pos[0] - 1][pos_y]
            moves.append(move)
        
        if self.pos[0] < 7 and board[self.pos[0] + 1][pos_y] != None and board[self.pos[0] + 1][pos_y].color != self.color:
            move = Move(self.pos, (self.pos[0] + 1, pos_y))
            move.captured = board[self.pos[0] + 1][pos_y]
            moves.append(move)

        en_passant_y = 4 if self.color == 0 else 3

        # En Passant
        if self.pos[1] == en_passant_y:
            if self.pos[0] > 0:
                en_passant_pawn = board[self.pos[0] - 1][self.pos[1]]
                if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                    move = En_Passant_Move(self.pos, (self.pos[0] - 1, pos_y), (self.pos[0] - 1, self.pos[1]))
                    move.captured = en_passant_pawn
                    moves.append(move)
            
            if self.pos[0] < 7:
                en_passant_pawn = board[self.pos[0] + 1][self.pos[1]]
                if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                    move = En_Passant_Move(self.pos, (self.pos[0] + 1, pos_y), (self.pos[0] + 1, self.pos[1]))
                    move.captured = en_passant_pawn
                    moves.append(move)

        # Mache aus allen Umwandlungen Promotion_Moves
        # iteriere über eine Kopie aller Züge, damit wir die Originalliste verändern können
        for move in moves.copy():
            if move.to[1] == 0 or move.to[1] == 7:
                # Bauern können in Damen, Türmen, Läufern und Springer umwandeln
                queen_move = Promotion_Move(move.fr, move.to, Queen(self.color, move.to), self)
                queen_move.captured = move.captured
                queen_move.promotion_piece.moved = True
                moves.append(queen_move)
                rook_move = Promotion_Move(move.fr, move.to, Rook(self.color, move.to), self)
                rook_move.captured = move.captured
                rook_move.promotion_piece.moved = True
                moves.append(rook_move)
                bishop_move = Promotion_Move(move.fr, move.to, Bishop(self.color, move.to), self)
                bishop_move.captured = move.captured
                bishop_move.promotion_piece.moved = True
                moves.append(bishop_move)
                knight_move = Promotion_Move(move.fr, move.to, Knight(self.color, move.to), self)
                knight_move.captured = move.captured
                knight_move.promotion_piece.moved = True
                moves.append(knight_move)

                # entferne den alten Zug
                moves.remove(move)
                
        self.set_first_move_in_list(moves)

        return moves
    
    # überprüft, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square(self, square : tuple, board : list):
        if self.color == 0:
            if square[0] == self.pos[0] - 1 and square[1] == self.pos[1] + 1:
                return True
            if square[0] == self.pos[0] + 1 and square[1] == self.pos[1] + 1:
                return True
        else:
            if square[0] == self.pos[0] - 1 and square[1] == self.pos[1] - 1:
                return True
            if square[0] == self.pos[0] + 1 and square[1] == self.pos[1] - 1:
                return True
        
        return False
    
    # überprüft auf einem leeren Schachfeld, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square_on_empty_board(self, square : tuple):
        return self.attacks_square(square, None)

# Turm
class Rook(Piece):
    def get_moves(self, board : list) -> list:
        return self.get_straight_moves(board)
    
    # überprüft, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square(self, square : tuple, board : list):
        # überprüfe, ob das zu überprüfende Feld in derselben Zeile liegt
        if square[0] == self.pos[0]:
            if square[1] < self.pos[1]:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(square[1] + 1, self.pos[1]):
                    if board[self.pos[0]][i] != None:
                        return False
                return True
            else:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(self.pos[1] + 1, square[1]):
                    if board[self.pos[0]][i] != None:
                        return False
                return True
        elif square[1] == self.pos[1]:
            if square[0] < self.pos[0]:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(square[0] + 1, self.pos[0]):
                    if board[i][self.pos[1]] != None:
                        return False
                return True
            else:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(self.pos[0] + 1, square[0]):
                    if board[i][self.pos[1]] != None:
                        return False
                return True
        
        return False
    
    # überprüft auf einem leeren Schachfeld, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square_on_empty_board(self, square : tuple):
        col_diff = abs(square[0] - self.pos[0])
        row_diff = abs(square[1] - self.pos[1])
        return (col_diff == 0 or row_diff == 0) and col_diff != row_diff
            

# Springer
class Knight(Piece):
    directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def get_moves(self, board : list) -> list:
        moves = []

        for direction in Knight.directions:
            if self.pos[0] + direction[0] > 7 or self.pos[0] + direction[0] < 0:
                continue
            if self.pos[1] + direction[1] > 7 or self.pos[1] + direction[1] < 0:
                continue
            if board[self.pos[0] + direction[0]][self.pos[1] + direction[1]] != None:
                if board[self.pos[0] + direction[0]][self.pos[1] + direction[1]].color != self.color:
                    move = Move(self.pos, (self.pos[0] + direction[0], self.pos[1] + direction[1]))
                    move.captured = board[self.pos[0] + direction[0]][self.pos[1] + direction[1]]
                    moves.append(move)
                continue
            else:
                moves.append(Move(self.pos, (self.pos[0] + direction[0], self.pos[1] + direction[1])))
        
        self.set_first_move_in_list(moves)

        return moves
    
    # überprüft, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square(self, square : tuple, board : list):
        col_diff = abs(square[0] - self.pos[0])
        row_diff = abs(square[1] - self.pos[1])

        return row_diff == 2 and col_diff == 1 or row_diff == 1 and col_diff == 2
    
    # überprüft auf einem leeren Schachfeld, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square_on_empty_board(self, square : tuple):
        return self.attacks_square(square, None)

# Läufer
class Bishop(Piece):
    def get_moves(self, board : list) -> list:
        return self.get_diagonal_moves(board)
    
    # überprüft, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square(self, square : tuple, board : list):
        col_diff = square[0] - self.pos[0]
        row_diff = square[1] - self.pos[1]

        # überprüfe, ob das zu überprüfende Feld in derselben Diagonale liegt
        if abs(row_diff) == abs(col_diff) and col_diff != 0:
            for i in range(1, abs(row_diff)):
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                if board[self.pos[0] + i * col_diff // abs(col_diff)][self.pos[1] + i * row_diff // abs(row_diff)] != None:
                    return False
            return True

        return False
    
    # überprüft auf einem leeren Schachfeld, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square_on_empty_board(self, square : tuple):
        col_diff = abs(square[0] - self.pos[0])
        row_diff = abs(square[1] - self.pos[1])

        return abs(col_diff) == abs(row_diff) and col_diff != 0

# Dame
class Queen(Piece):
    def get_moves(self, board : list) -> list:
        return self.get_straight_moves(board) + self.get_diagonal_moves(board)

    # überprüft, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square(self, square : tuple, board : list):
        row_diff = square[0] - self.pos[0]
        col_diff = square[1] - self.pos[1]

        # überprüfe, ob das zu überprüfende Feld in derselben Zeile liegt
        if row_diff == 0:
            if square[1] < self.pos[1]:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(square[1] + 1, self.pos[1]):
                    if board[self.pos[0]][i] != None:
                        return False
                return True
            else:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(self.pos[1] + 1, square[1]):
                    if board[self.pos[0]][i] != None:
                        return False
                return True
        elif col_diff == 0:
            if square[0] < self.pos[0]:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(square[0] + 1, self.pos[0]):
                    if board[i][self.pos[1]] != None:
                        return False
                return True
            else:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(self.pos[0] + 1, square[0]):
                    if board[i][self.pos[1]] != None:
                        return False
                return True
        # überprüfe, ob das zu überprüfende Feld in derselben Diagonale liegt
        elif abs(row_diff) == abs(col_diff):
            for i in range(1, abs(row_diff)):
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                if board[self.pos[0] + i * row_diff // abs(row_diff)][self.pos[1] + i * col_diff // abs(col_diff)] != None:
                    return False
            return True
        
        return False
    
    # überprüft auf einem leeren Schachfeld, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square_on_empty_board(self, square : tuple):
        col_diff = square[0] - self.pos[0]
        row_diff = square[1] - self.pos[1]

        return ((row_diff == 0 or col_diff == 0) and row_diff != col_diff) or abs(row_diff) == abs(col_diff)

# König
class King(Piece):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    knight_directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def get_moves(self, board : list) -> list:
        moves = []

        for direction in King.directions:
            if self.pos[0] + direction[0] > 7 or self.pos[0] + direction[0] < 0:
                continue
            if self.pos[1] + direction[1] > 7 or self.pos[1] + direction[1] < 0:
                continue
            if board[self.pos[0] + direction[0]][self.pos[1] + direction[1]] != None:
                if board[self.pos[0] + direction[0]][self.pos[1] + direction[1]].color != self.color:
                    move = Move(self.pos, (self.pos[0] + direction[0], self.pos[1] + direction[1]))
                    move.captured = board[self.pos[0] + direction[0]][self.pos[1] + direction[1]]
                    moves.append(move)
                continue
            moves.append(Move(self.pos, (self.pos[0] + direction[0], self.pos[1] + direction[1])))
        
        # Rochade
        # Bedingung für Rochade:
        # 1. König und Turm haben sich nicht bewegt
        # 2. Zwischen König und Turm ist keine andere Figur
        # 3. König und alle Felder zwischen Turm und König werden nicht angegriffen

        # Bedingung 1
        if not self.moved:
            enemy_pieces = [board[i][j] for i in range(8) for j in range(8) if board[i][j] != None and board[i][j].color != self.color]
            if self.color == 0:
                if self.pos == (4, 0):
                    left_corner_piece = board[0][0]
                    right_corner_piece = board[7][0]

                    # Bedingung 2 für Weiss auf Königseite
                    if board[5][0] == None and board[6][0] == None and isinstance(right_corner_piece, Rook) and right_corner_piece.color == self.color and not right_corner_piece.moved:
                        # Bedingung 3 für Weiss auf Königseite
                        path = [(4, 0), (5,0)]
                        if not any(piece.attacks_square(square, board) for piece in enemy_pieces for square in path):
                            new_move = Castling_Move(self.pos, (6, 0), (7, 0), (5, 0))
                            moves.append(new_move)
                    
                    # Bedingung 2 für Weiss auf Damenseite
                    if board[1][0] == None and board[2][0] == None and board[3][0] == None and isinstance(left_corner_piece, Rook) and left_corner_piece.color == self.color and not left_corner_piece.moved:
                        # Bedingung 3 für Weiss auf Damenseite
                        path = [(4, 0), (3, 0)]
                        if not any(piece.attacks_square(square, board) for piece in enemy_pieces for square in path):
                            new_move = Castling_Move(self.pos, (2, 0), (0, 0), (3, 0))
                            moves.append(new_move)
            else:
                if self.pos == (4, 7):
                    left_corner_piece = board[0][7]
                    right_corner_piece = board[7][7]

                    # Bedingung 2 für Schwarz auf Königseite
                    if board[5][7] == None and board[6][7] == None and isinstance(right_corner_piece, Rook) and right_corner_piece.color == self.color and not right_corner_piece.moved:
                        # Bedingung 3 für Schwarz auf Königseite
                        path = [(4, 7), (5,7)]
                        if not any(piece.attacks_square(square, board) for piece in enemy_pieces for square in path):
                            new_move = Castling_Move(self.pos, (6, 7), (7, 7), (5, 7))
                            moves.append(new_move)
                    
                    # Bedingung 2 für Schwarz auf Damenseite
                    if board[1][7] == None and board[2][7] == None and board[3][7] == None and isinstance(left_corner_piece, Rook) and left_corner_piece.color == self.color and not left_corner_piece.moved:
                        # Bedingung 3 für Schwarz auf Damenseite
                        path = [(4, 7), (3, 7)]
                        if not any(piece.attacks_square(square, board) for piece in enemy_pieces for square in path):
                            new_move = Castling_Move(self.pos, (2, 7), (0, 7), (3, 7))
                            moves.append(new_move)

        self.set_first_move_in_list(moves)

        return moves
    
    def get_knight_moves(self, board : list) -> list:
        moves = []

        for direction in King.knight_directions:
            if self.pos[0] + direction[0] > 7 or self.pos[0] + direction[0] < 0:
                continue
            if self.pos[1] + direction[1] > 7 or self.pos[1] + direction[1] < 0:
                continue
            if board[self.pos[0] + direction[0]][self.pos[1] + direction[1]] != None:
                if board[self.pos[0] + direction[0]][self.pos[1] + direction[1]].color != self.color:
                    move = Move(self.pos, (self.pos[0] + direction[0], self.pos[1] + direction[1]))
                    move.captured = board[self.pos[0] + direction[0]][self.pos[1] + direction[1]]
                    moves.append(move)
                continue
            else:
                moves.append(Move(self.pos, (self.pos[0] + direction[0], self.pos[1] + direction[1])))

        return moves
    
    def get_pawn_moves(self, board : list) -> list:
        moves = []

        if self.color == 0:
            if self.pos[1] >= 6:
                return moves
        else:
            if self.pos[1] <= 1:
                return moves


        forward = 1 if self.color == 0 else -1
        pos_y = self.pos[1] + forward

        # Uns interessieren nur Schlagzüge
        if self.pos[0] > 0:
            piece = board[self.pos[0] - 1][pos_y]
            if piece != None and piece.color != self.color:
                move = Move(self.pos, (self.pos[0] - 1, pos_y))
                move.captured = piece
                moves.append(move)
        
        if self.pos[0] < 7:
            piece = board[self.pos[0] + 1][pos_y]
            if piece != None and piece.color != self.color:
                move = Move(self.pos, (self.pos[0] + 1, pos_y))
                move.captured = piece
                moves.append(move)

        return moves

    # überprüft, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square(self, square : tuple, board : list):
        col_diff = abs(square[0] - self.pos[0])
        row_diff = abs(square[1] - self.pos[1])

        return (row_diff <= 1 and col_diff <= 1) and (row_diff == 1 or col_diff == 1)
    
    # überprüft auf einem leeren Schachfeld, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square_on_empty_board(self, square : tuple):
        return self.attacks_square(square, None)