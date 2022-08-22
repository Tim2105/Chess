from math import inf
from uuid import uuid4
from enum import Enum
from threading import Timer
from bisect import insort

# Klasse, die einen regulären Schachzug kapselt
class Move:
    def __init__(self, from_pos : tuple, to_pos : tuple):
        self.fr = from_pos
        self.to = to_pos
        self.captured = None
        self.first_move = False
        self.undone_advanced_two_last_move = None
    
    def __str__(self):
        return f"{chr(self.fr[0] + 65)}{self.fr[1] + 1} -> {chr(self.to[0] + 65)}{self.to[1] + 1}"
    
    def __eq__(self, o):
        if not type(o) is Move:
            return False
        
        return self.fr == o.fr and self.to == o.to and self.first_move == o.first_move and type(self.captured) == type(o.captured)

# Oberklasse für alle Figuren
class Piece:
    def __init__(self, color : int, pos : tuple):
        if color != 0 and color != 1:
            raise ValueError("color must be 0 or 1")
            
        self.color = color
        self.pos = pos
        self.moved = False
    
    def __hash__(self):
        val = 0
        val += self.color
        val += self.pos[0] << 1
        val += self.pos[1] << 4
        val += int(self.moved) << 7

        return val
    
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

# Klasse, die einen En Passant Zug kapselt
class En_Passant_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple, en_passant_pos : tuple):
        super().__init__(from_pos, to_pos)
        self.en_passant_pos = en_passant_pos
    
    def __eq__(self, o):
        if not type(o) is En_Passant_Move:
            return False
        
        return self.fr == o.fr and self.to == o.to and self.en_passant_pos == o.en_passant_pos

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
        
        return self.fr == o.fr and self.to == o.to and type(self.promotion_piece) == type(o.promotion_piece) and type(self.captured) == type(o.captured)

# Klasse, die einen Doppelzug eines Bauern kapselt
class Pawn_Double_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple):
        super().__init__(from_pos, to_pos)
    
    def __eq__(self, o):
        if not type(o) is Pawn_Double_Move:
            return False
        
        return self.fr == o.fr and self.to == o.to

# Bauer
class Pawn(Piece):
    def __init__(self, color : int, pos : tuple):
        super().__init__(color, pos)
        # relevant für En Passant
        self.advanced_two_last_move = False

    def get_moves(self, board : list) -> list:
        moves = []

        if self.color == 0:
            if self.pos[1] >= 7:
                return moves

            if board[self.pos[0]][self.pos[1] + 1] == None:
                moves.append(Move(self.pos, (self.pos[0], self.pos[1] + 1)))

                # Erster Zug vom Bauern
                if not self.moved:
                    if board[self.pos[0]][self.pos[1] + 2] == None:
                        moves.append(Pawn_Double_Move(self.pos, (self.pos[0], self.pos[1] + 2)))
                
            # Schlagen
            if self.pos[0] > 0 and board[self.pos[0] - 1][self.pos[1] + 1] != None and board[self.pos[0] - 1][self.pos[1] + 1].color != self.color:
                move = Move(self.pos, (self.pos[0] - 1, self.pos[1] + 1))
                move.captured = board[self.pos[0] - 1][self.pos[1] + 1]
                moves.append(move)
            
            if self.pos[0] < 7 and board[self.pos[0] + 1][self.pos[1] + 1] != None and board[self.pos[0] + 1][self.pos[1] + 1].color != self.color:
                move = Move(self.pos, (self.pos[0] + 1, self.pos[1] + 1))
                move.captured = board[self.pos[0] + 1][self.pos[1] + 1]
                moves.append(move)

            # En Passant
            if self.pos[1] == 4:
                if self.pos[0] > 0:
                    en_passant_pawn = board[self.pos[0] - 1][self.pos[1]]
                    if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                        move = En_Passant_Move(self.pos, (self.pos[0] - 1, self.pos[1] + 1), (self.pos[0] - 1, self.pos[1]))
                        move.captured = en_passant_pawn
                        moves.append(move)
                
                if self.pos[0] < 7:
                    en_passant_pawn = board[self.pos[0] + 1][self.pos[1]]
                    if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                        move = En_Passant_Move(self.pos, (self.pos[0] + 1, self.pos[1] + 1), (self.pos[0] + 1, self.pos[1]))
                        move.captured = en_passant_pawn
                        moves.append(move)

        else:
            if self.pos[1] <= 0:
                return moves

            if board[self.pos[0]][self.pos[1] - 1] == None:
                moves.append(Move(self.pos, (self.pos[0], self.pos[1] - 1)))

                # Erster Zug vom Bauern
                if not self.moved:
                    if board[self.pos[0]][self.pos[1] - 2] == None:
                        moves.append(Pawn_Double_Move(self.pos, (self.pos[0], self.pos[1] - 2)))
                
            # Schlagen
            if self.pos[0] > 0 and board[self.pos[0] - 1][self.pos[1] - 1] != None and board[self.pos[0] - 1][self.pos[1] - 1].color != self.color:
                move = Move(self.pos, (self.pos[0] - 1, self.pos[1] - 1))
                move.captured = board[self.pos[0] - 1][self.pos[1] - 1]
                moves.append(move)

            if self.pos[0] < 7 and board[self.pos[0] + 1][self.pos[1] - 1] != None and board[self.pos[0] + 1][self.pos[1] - 1].color != self.color:
                move = Move(self.pos, (self.pos[0] + 1, self.pos[1] - 1))
                move.captured = board[self.pos[0] + 1][self.pos[1] - 1]
                moves.append(move)
            
            # En Passant
            if self.pos[1] == 3:
                if self.pos[0] > 0:
                    en_passant_pawn = board[self.pos[0] - 1][self.pos[1]]
                    if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                        move = En_Passant_Move(self.pos, (self.pos[0] - 1, self.pos[1] - 1), (self.pos[0] - 1, self.pos[1]))
                        move.captured = en_passant_pawn
                        moves.append(move)
                
                if self.pos[0] < 7:
                    en_passant_pawn = board[self.pos[0] + 1][self.pos[1]]
                    if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                        move = En_Passant_Move(self.pos, (self.pos[0] + 1, self.pos[1] - 1), (self.pos[0] + 1, self.pos[1]))
                        move.captured = en_passant_pawn
                        moves.append(move)

        # Mache aus allen Umwandlungen Promotion_Moves
        # iteriere über eine Kopie aller Züge, damit wir die Originalliste verändern können
        for move in list(moves):
            if move.to[1] == 0 or move.to[1] == 7:
                # Bauern können in Damen, Türmen, Läufern und Springer umwandeln
                queen_move = Promotion_Move(move.fr, move.to, Queen(self.color, move.to), self)
                queen_move.captured = move.captured
                moves.append(queen_move)
                rook_move = Promotion_Move(move.fr, move.to, Rook(self.color, move.to), self)
                rook_move.captured = move.captured
                moves.append(rook_move)
                bishop_move = Promotion_Move(move.fr, move.to, Bishop(self.color, move.to), self)
                bishop_move.captured = move.captured
                moves.append(bishop_move)
                knight_move = Promotion_Move(move.fr, move.to, Knight(self.color, move.to), self)
                knight_move.captured = move.captured
                moves.append(knight_move)

                # entferne den alten Zug
                moves.remove(move)
                

        self.set_first_move_in_list(moves)

        return moves
    
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
    
    def attacks_square_on_empty_board(self, square : tuple):
        return self.attacks_square(square, None)

# Turm
class Rook(Piece):
    def get_moves(self, board : list) -> list:
        return self.get_straight_moves(board)
    
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
    
    def attacks_square_on_empty_board(self, square : tuple):
        return self.pos[0] == square[0] or self.pos[1] == square[1]
            

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
            moves.append(Move(self.pos, (self.pos[0] + direction[0], self.pos[1] + direction[1])))
        
        self.set_first_move_in_list(moves)

        return moves
    
    def attacks_square(self, square : tuple, board : list):
        col_diff = abs(square[0] - self.pos[0])
        row_diff = abs(square[1] - self.pos[1])

        return row_diff == 2 and col_diff == 1 or row_diff == 1 and col_diff == 2
    
    def attacks_square_on_empty_board(self, square : tuple):
        return self.attacks_square(square, None)

# Läufer
class Bishop(Piece):
    def get_moves(self, board : list) -> list:
        return self.get_diagonal_moves(board)
    
    def attacks_square(self, square : tuple, board : list):
        col_diff = square[0] - self.pos[0]
        row_diff = square[1] - self.pos[1]

        # überprüfe, ob das zu überprüfende Feld in derselben Diagonale liegt
        if abs(row_diff) == abs(col_diff):
            for i in range(1, abs(row_diff)):
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                if board[self.pos[0] + i * col_diff // abs(col_diff)][self.pos[1] + i * row_diff // abs(row_diff)] != None:
                    return False
            return True

        return False
    
    def attacks_square_on_empty_board(self, square : tuple):
        return abs(square[0] - self.pos[0]) == abs(square[1] - self.pos[1])

# Dame
class Queen(Piece):
    def get_moves(self, board : list) -> list:
        return self.get_straight_moves(board) + self.get_diagonal_moves(board)

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
    
    def attacks_square_on_empty_board(self, square : tuple):
        col_diff = square[0] - self.pos[0]
        row_diff = square[1] - self.pos[1]

        return row_diff == 0 or col_diff == 0 or abs(row_diff) == abs(col_diff)

# König
class King(Piece):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

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
            enemy_pieces = {board[i][j] : (i, j) for i in range(8) for j in range(8) if board[i][j] != None and board[i][j].color != self.color}
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
    
    def attacks_square(self, square : tuple, board : list):
        col_diff = abs(square[0] - self.pos[0])
        row_diff = abs(square[1] - self.pos[1])

        return row_diff <= 1 and col_diff <= 1
    
    def attacks_square_on_empty_board(self, square : tuple):
        return self.attacks_square(square, None)

# Stellt ein Schachbrett dar
# kann Züge generieren auf das Schachbrett ausführen
class Board:
    def __init__(self, fen_string : str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"):
        self.turn = 0
        self.board = [[None for x in range(8)] for y in range(8)]

        # Initialisiere die Figuren
        self.read_fen_string(fen_string)
        
        self.pieces = []
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != None:
                    self.pieces.append(self.board[x][y])
        
        kings = [x for x in self.pieces if isinstance(x, King)]
        if len(kings) != 2 or kings[0].color == kings[1].color:
            raise ValueError("Invalid FEN string: Both colors must have exactly one King")
        
        self.move_history = []
        
        self.init_zobrist()
    
    def __eq__(self, o):
        if type(self) != type(o):
            return False
        
        if self.turn != o.turn or len(self.pieces) != len(o.pieces):
            return False
        
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != o.board[x][y]:
                    return False
        
        return True
            
        
    # initialisiere die Zobristtabelle
    def init_zobrist(self):
        self.zobrist_table = [[] for j in range(64)]

        for square in self.zobrist_table:
            for i in range(18):
                square.append(uuid4().int & 0xffffffff)
        
        self.black_to_move = uuid4().int & 0xffffffff
    
    def get_zobrist_piece_value(self, piece : Piece):
        if piece == None:
            raise ValueError("Piece is None")
        
        if isinstance(piece, Pawn):
            if piece.advanced_two_last_move:
                return piece.color * 9 + 8
            else:
                return piece.color * 9
        elif isinstance(piece, Rook):
            if piece.moved:
                return piece.color * 9 + 6
            else:
                return piece.color * 9 + 1
        elif isinstance(piece, Knight):
            return piece.color * 9 + 2
        elif isinstance(piece, Bishop):
            return piece.color * 9 + 3
        elif isinstance(piece, Queen):
            return piece.color * 9 + 4
        elif isinstance(piece, King):
            if piece.moved:
                return piece.color * 9 + 7
            else:
                return piece.color * 9 + 5
        else:
            raise ValueError("Invalid piece")
        

    # Zobrist Hash
    # Quelle: https://research.cs.wisc.edu/techreports/1970/TR88.pdf
    def __hash__(self):
        res : int = self.black_to_move * self.turn
    
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != None:
                    res ^= self.zobrist_table[x * 8 + y][self.get_zobrist_piece_value(self.board[x][y])]

        return res
    
    # generiert aus einer Liste von Zügen die dazugehörigen Hashes, wenn man den Zug ausführen würde
    # weitaus effizienter als den Zug ausszuführen, zu hashen und ihn dann wieder Rückgängig zu machen
    def get_hashes_after_moves(self, moves : list) -> dict:
        res = {}
        curr_hash = self.__hash__()

        for move in moves:
            new_hash = curr_hash ^ self.black_to_move
            new_hash ^= self.zobrist_table[move.fr[0] * 8 + move.fr[1]][self.get_zobrist_piece_value(self.board[move.fr[0]][move.fr[1]])]

            if move.captured != None:
                if isinstance(move, En_Passant_Move):
                    new_hash ^= self.zobrist_table[move.en_passant_pos[0] * 8 + move.en_passant_pos[1]][self.get_zobrist_piece_value(move.captured)]
                else:
                    new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(move.captured)]
                
                new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(self.board[move.fr[0]][move.fr[1]])]
            elif isinstance(move, Pawn_Double_Move):
                new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(self.board[move.fr[0]][move.fr[1]]) + 8]
            elif isinstance(move, Promotion_Move):
                new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(move.promotion_piece)]
            else:
                if isinstance(self.board[move.fr[0]][move.fr[1]], King) and move.first_move:
                    new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(self.board[move.fr[0]][move.fr[1]]) + 2]
                elif isinstance(self.board[move.fr[0]][move.fr[1]], Rook) and move.first_move:
                    new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(self.board[move.fr[0]][move.fr[1]]) + 5]
                else:
                    new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(self.board[move.fr[0]][move.fr[1]])]

            if isinstance(move, Castling_Move):
                new_hash ^= self.zobrist_table[move.rook_fr[0] * 8 + move.rook_fr[1]][self.get_zobrist_piece_value(self.board[move.rook_fr[0]][move.rook_fr[1]])]
                new_hash ^= self.zobrist_table[move.rook_to[0] * 8 + move.rook_to[1]][self.get_zobrist_piece_value(self.board[move.rook_fr[0]][move.rook_fr[1]])]

            res[move] = new_hash
        
        return res

        
    # liest einen FEN-String ein und initialisiert das Board
    # FEN-Strings sind der Standard um Schachfelder mit ASCII-Zeichen zu beschreiben
    def read_fen_string(self, fen_string : str):
        strings = fen_string.split()

        if len(strings) < 4:
            raise ValueError("Invalid FEN-String: Missing one or more fields")

        # Teil 1: Position der Figuren
        row = 7
        col = 0
        for char in strings[0]:
            if char == '/':
                row -= 1
                col = 0
                continue
            if char.isdigit():
                col += int(char)
                continue
            if char.isalpha():
                if char.isupper():
                    color = 0
                else:
                    color = 1

                char = char.lower()

                if char == 'k':
                    self.board[col][row] = King(color, (col, row))
                elif char == 'q':
                    self.board[col][row] = Queen(color, (col, row))
                elif char == 'r':
                    self.board[col][row] = Rook(color, (col, row))
                    if not (color == 0 and row == 0 and col in [0, 7] or color == 1 and row == 7 and col in [0, 7]):
                        self.board[col][row].moved = True
                elif char == 'b':
                    self.board[col][row] = Bishop(color, (col, row))
                elif char == 'n':
                    self.board[col][row] = Knight(color, (col, row))
                elif char == 'p':
                    self.board[col][row] = Pawn(color, (col, row))
                    if not (color == 0 and row == 1 or color == 1 and row == 6):
                        self.board[col][row].moved = True
                else:
                    raise ValueError("Invalid FEN-String: Invalid character during position parsing")
                
                col += 1
            else:
                raise ValueError("Invalid FEN-String: Invalid character during position parsing")
        
        # Teil 2: Welcher Spieler am Zug ist
        if strings[1] == "b":
            self.turn = 1
        elif strings[1] == "w":
            self.turn = 0
        else:
            raise ValueError("Invalid FEN-String: Invalid color (must be b or w)")
        
        # Teil 3: Welche Rochaden sind möglich
        if 'Q' not in strings[2]:
            possible_rook = self.board[0][0]
            if possible_rook != None and isinstance(possible_rook, Rook) and possible_rook.color == 0:
                possible_rook.moved = True
        if 'K' not in strings[2]:
            possible_rook = self.board[7][0]
            if possible_rook != None and isinstance(possible_rook, Rook) and possible_rook.color == 0:
                possible_rook.moved = True
        if 'q' not in strings[2]:
            possible_rook = self.board[0][7]
            if possible_rook != None and isinstance(possible_rook, Rook) and possible_rook.color == 1:
                possible_rook.moved = True
        if 'k' not in strings[2]:
            possible_rook = self.board[7][7]
            if possible_rook != None and isinstance(possible_rook, Rook) and possible_rook.color == 1:
                possible_rook.moved = True
        
        # Teil 4: Welcher Bauer kann per En Passant geschlagen werden(wenn vorhanden)
        if strings[3] != "-":
            en_passant_square = strings[3]
            if len(en_passant_square) != 2 or not en_passant_square[0] in "abcdefgh" or not en_passant_square[1] in "12345678":
                raise ValueError(f"Invalid FEN-String: Invalid en passant square {strings[3]} (must be a1, b2, c3, ..., h8)")

            possible_pawn = None
            if en_passant_square[1] == "3":
                possible_pawn = self.board[ord(en_passant_square[0]) - 97][3]
            elif en_passant_square[1] == "6":
                possible_pawn = self.board[ord(en_passant_square[0]) - 97][4]

            if possible_pawn != None and isinstance(possible_pawn, Pawn) and possible_pawn.color != self.turn:
                possible_pawn.advanced_two_last_move = True
            else:
                raise ValueError(f"Invalid FEN-String: Invalid En Passant Square {strings[3]} (must be a square where a pawn of the other color can be captured)")
        
        # Teil 5 und Teil 6(Halfmove- und Fullmove-Nummern) sind in diesem Projekt nicht relevant und werden hier ignoriert

    # gibt alle machbaren Züge einer Farbe zurück
    # enthält Züge, die den eigenen König im Schach lassen(illegal)!
    def get_moves(self, color : int) -> list:
        moves = []

        own_pieces = [x for x in self.pieces if x.color == color]

        for piece in own_pieces:
            moves += piece.get_moves(self.board)
        
        return moves

    def get_legitimate_moves_from_piece(self, piece : Piece) -> list:
        if not piece in self.pieces:
            raise ValueError("Piece not on board")
        
        moves = []

        king = [x for x in self.pieces if isinstance(x, King) and x.color == piece.color][0]

        for move in piece.get_moves(self.board):
            self.do_move(move)
            enemy_pieces = [x for x in self.pieces if x.color != piece.color]
            if not any(x.attacks_square(king.pos, self.board) for x in enemy_pieces):
                moves.append(move)

            self.undo_move(move)
        
        return moves

    def get_legitimate_moves_from_pos(self, pos : tuple) -> list:
        self.get_legitimate_moves_from_piece(self.board[pos[0]][pos[1]])

    # gibt alle legitimen Züge eines Spielers zurück
    # wenn die Liste leer ist, dann ist der Spieler Schachmatt
    def get_legitimate_moves(self, color : int) -> list:
        moves = []

        king = [x for x in self.pieces if isinstance(x, King) and x.color == self.turn][0]
        own_pieces = [x for x in self.pieces if x.color == color]
        enemy_pieces = [x for x in self.pieces if x.color != color]

        # Es reicht i.d.R., die gegnerischen Figuren zu betrachten, die den Köing auf einem sonst leeren Feld in Schach stellen
        potential_enemy_attackers = [x for x in self.pieces if x.color != color and x.attacks_square_on_empty_board(king.pos)]

        for piece in own_pieces:
            for move in piece.get_moves(self.board):
                self.do_move(move)

                # Wenn der König bewegt wurde, müssen alle gegnerischen Figuren betrachtet werden
                if isinstance(self.board[move.to[0]][move.to[1]], King):
                    if not any(x.attacks_square(king.pos, self.board) for x in enemy_pieces):
                        moves.append(move)
                else:
                    if not any(x.attacks_square(king.pos, self.board) for x in potential_enemy_attackers):
                        moves.append(move)

                self.undo_move(move)
            
        return moves
    
    # führt einen Zug aus
    def do_move(self, move : Move):
        if self.board[move.fr[0]][move.fr[1]] == None:
            raise ValueError("Piece does not exist")

        self.board[move.to[0]][move.to[1]] = self.board[move.fr[0]][move.fr[1]]
        self.board[move.to[0]][move.to[1]].moved = True
        self.board[move.fr[0]][move.fr[1]] = None
        self.board[move.to[0]][move.to[1]].pos = move.to
        self.turn = 1 - self.turn
        
        if move.captured != None:
            self.pieces.remove(move.captured)
        
        if isinstance(move, Pawn_Double_Move):
            self.board[move.to[0]][move.to[1]].advanced_two_last_move = True
        elif isinstance(move, Castling_Move):
            self.board[move.castling_rook_to[0]][move.castling_rook_to[1]] = self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]]
            self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]] = None
            self.board[move.castling_rook_to[0]][move.castling_rook_to[1]].pos = move.castling_rook_to
        elif isinstance(move, Promotion_Move):
            self.board[move.to[0]][move.to[1]] = move.promotion_piece
            move.promotion_piece.pos = move.to
            self.pieces.remove(move.promoted_piece)
            self.pieces.append(move.promotion_piece)
        elif isinstance(move, En_Passant_Move):
            self.board[move.en_passant_pos[0]][move.en_passant_pos[1]] = None
        
        for piece in self.pieces:
            if isinstance(piece, Pawn):
                if piece.advanced_two_last_move:
                    piece.advanced_two_last_move = False
                    move.undone_advanced_two_last_move = piece.pos
                    break
        
        self.move_history.append(move)
    
    # macht einen Zug rückgängig
    def undo_move(self, move : Move):
        if move != self.move_history[-1]:
            raise ValueError("Can only undo last move")

        if move.undone_advanced_two_last_move != None:
            pos = move.undone_advanced_two_last_move
            self.board[pos[0]][pos[1]].advanced_two_last_move = True

        self.board[move.fr[0]][move.fr[1]] = self.board[move.to[0]][move.to[1]]
        self.board[move.fr[0]][move.fr[1]].moved = not move.first_move
        self.board[move.to[0]][move.to[1]] = None
        self.board[move.fr[0]][move.fr[1]].pos = move.fr
        self.turn = 1 - self.turn

        if move.captured != None:
            self.board[move.to[0]][move.to[1]] = move.captured
            move.captured.pos = move.to
            self.pieces.append(move.captured)
        
        if isinstance(move, Pawn_Double_Move):
            self.board[move.fr[0]][move.fr[1]].advanced_two_last_move = False
        elif isinstance(move, Castling_Move):
            self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]] = self.board[move.castling_rook_to[0]][move.castling_rook_to[1]]
            self.board[move.castling_rook_to[0]][move.castling_rook_to[1]] = None
            self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]].pos = move.castling_rook_fr
        elif isinstance(move, Promotion_Move):
            self.board[move.fr[0]][move.fr[1]] = move.promoted_piece
            move.promoted_piece.pos = move.fr
            self.pieces.remove(move.promotion_piece)
            self.pieces.append(move.promoted_piece)
        elif isinstance(move, En_Passant_Move):
            self.board[move.en_passant_pos[0]][move.en_passant_pos[1]] = move.captured
            move.captured.pos = move.en_passant_pos
            move.captured.advanced_two_last_move = True
        
        self.move_history.pop()

class Transposition_Table_Entry_Type(Enum):
    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2

class Transposition_Table_Entry:
    def __init__(self, value : int, depth: int, entry_type : Transposition_Table_Entry_Type):
        self.value = value
        self.depth = depth
        self.entry_type = entry_type
        self.principal_variation = None
        self.killer_moves = []

class Computer_Player:
    # Quelle: https://www.chessprogramming.org/Simplified_Evaluation_Function
    piece_value = {
        King :      20000,
        Pawn :      100,
        Knight :    320,
        Bishop :    330,
        Rook :      500,
        Queen :     900
    }

    # Piece-Square Tables
    # Quelle: https://www.chessprogramming.org/Simplified_Evaluation_Function
    pst_midgame = {
        Pawn : [
            [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [ 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0],
            [ 10.0, 10.0, 20.0, 30.0, 30.0, 20.0, 10.0, 10.0],
            [  5.0,  5.0, 10.0, 25.0, 25.0, 10.0,  5.0,  5.0],
            [  0.0,  0.0,  0.0, 20.0, 20.0,  0.0,  0.0,  0.0],
            [  5.0, -5.0,-10.0,  0.0,  0.0,-10.0, -5.0,  5.0],
            [  5.0, 10.0, 10.0,-20.0,-20.0, 10.0, 10.0,  5.0],
            [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ],
        Knight : [
            [-50.0,-40.0,-30.0,-30.0,-30.0,-30.0,-40.0,-50.0],
            [-40.0,-20.0,  0.0,  0.0,  0.0,  0.0,-20.0,-40.0],
            [-30.0,  0.0, 10.0, 15.0, 15.0, 10.0,  0.0,-30.0],
            [-30.0,  5.0, 15.0, 20.0, 20.0, 15.0,  5.0,-30.0],
            [-30.0,  0.0, 15.0, 20.0, 20.0, 15.0,  0.0,-30.0],
            [-30.0,  5.0, 10.0, 15.0, 15.0, 10.0,  5.0,-30.0],
            [-40.0,-20.0,  0.0,  5.0,  5.0,  0.0,-20.0,-40.0],
            [-50.0,-40.0,-30.0,-30.0,-30.0,-30.0,-40.0,-50.0]
        ],
        Bishop : [
            [-20.0,-10.0,-10.0,-10.0,-10.0,-10.0,-10.0,-20.0],
            [-10.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,-10.0],
            [-10.0,  0.0,  5.0, 10.0, 10.0,  5.0,  0.0,-10.0],
            [-10.0,  5.0,  5.0, 10.0, 10.0,  5.0,  5.0,-10.0],
            [-10.0,  0.0, 10.0, 10.0, 10.0, 10.0,  0.0,-10.0],
            [-10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,-10.0],
            [-10.0,  5.0,  0.0,  0.0,  0.0,  0.0,  5.0,-10.0],
            [-20.0,-10.0,-10.0,-10.0,-10.0,-10.0,-10.0,-20.0]
        ],
        Rook : [
            [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [  5.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,  5.0],
            [ -5.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -5.0],
            [ -5.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -5.0],
            [ -5.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -5.0],
            [ -5.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -5.0],
            [ -5.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -5.0],
            [  0.0,  0.0,  0.0,  5.0,  5.0,  0.0,  0.0,  0.0]
        ],
        Queen : [
            [-20.0,-10.0,-10.0, -5.0, -5.0,-10.0,-10.0,-20.0],
            [-10.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,-10.0],
            [-10.0,  0.0,  5.0,  5.0,  5.0,  5.0,  0.0,-10.0],
            [ -5.0,  0.0,  5.0,  5.0,  5.0,  5.0,  0.0, -5.0],
            [  0.0,  0.0,  5.0,  5.0,  5.0,  5.0,  0.0, -5.0],
            [-10.0,  5.0,  5.0,  5.0,  5.0,  5.0,  0.0,-10.0],
            [-10.0,  0.0,  5.0,  0.0,  0.0,  0.0,  0.0,-10.0],
            [-20.0,-10.0,-10.0, -5.0, -5.0,-10.0,-10.0,-20.0]
        ],
        King : [
            [-30.0,-40.0,-40.0,-50.0,-50.0,-40.0,-40.0,-30.0],
            [-30.0,-40.0,-40.0,-50.0,-50.0,-40.0,-40.0,-30.0],
            [-30.0,-40.0,-40.0,-50.0,-50.0,-40.0,-40.0,-30.0],
            [-30.0,-40.0,-40.0,-50.0,-50.0,-40.0,-40.0,-30.0],
            [-20.0,-30.0,-30.0,-40.0,-40.0,-30.0,-30.0,-20.0],
            [-10.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-10.0],
            [ 20.0, 20.0,  0.0,  0.0,  0.0,  0.0, 20.0, 20.0],
            [ 20.0, 30.0, 10.0,  0.0,  0.0, 10.0, 30.0, 20.0]
        ]
    }

    pst_endgame = {
        Pawn : pst_midgame[Pawn],
        Knight : pst_midgame[Knight],
        Bishop : pst_midgame[Bishop],
        Rook : pst_midgame[Rook],
        Queen : pst_midgame[Queen],
        King : [
            [-50.0,-40.0,-30.0,-20.0,-20.0,-30.0,-40.0,-50.0],
            [-30.0,-20.0,-10.0,  0.0,  0.0,-10.0,-20.0,-30.0],
            [-30.0,-10.0, 20.0, 30.0, 30.0, 20.0,-10.0,-30.0],
            [-30.0,-10.0, 30.0, 40.0, 40.0, 30.0,-10.0,-30.0],
            [-30.0,-10.0, 30.0, 40.0, 40.0, 30.0,-10.0,-30.0],
            [-30.0,-10.0, 20.0, 30.0, 30.0, 20.0,-10.0,-30.0],
            [-30.0,-30.0,  0.0,  0.0,  0.0,  0.0,-30.0,-30.0],
            [-50.0,-30.0,-30.0,-30.0,-30.0,-30.0,-30.0,-50.0]
        ]
    }

    def __init__(self):
        self.searching = False
        self.curr_depth = 0
        self.transposition_table = {}
        self.best_move = None
        self.last_search_principal_variation = []
        self.last_search_interrupted = False
        self.nodes_visited = 0

    def get_pst_value(self, piece : Piece, use_endgame_values = False) -> float:
        if piece == None:
            return 0

        if use_endgame_values:
            if piece.color == 0:
                return self.pst_endgame[type(piece)][7 - piece.pos[1]][piece.pos[0]]
            else:
                return self.pst_endgame[type(piece)][piece.pos[1]][7 - piece.pos[0]]
        else:
            if piece.color == 0:
                return self.pst_midgame[type(piece)][7 - piece.pos[1]][piece.pos[0]]
            else:
                return self.pst_midgame[type(piece)][piece.pos[1]][7 - piece.pos[0]]
    
    # SEE - Static Exchange Evaluation
    # Überprüft eine Abfolge von Schlägen auf demselben Feld(immer mit der niedrigstmöglichen Figur)
    # und gibt die Veränderung im Material zurück(- -> verloren, + -> gewonnen)
    # Quelle : https://www.researchgate.net/publication/298853351_STATIC_EXCHANGE_EVALUATION_WITH_alpha_beta-APPROACH
    def see(self, board : Board, pos : tuple) -> float:
        # SEE funktioniert nur auf Feldern wo eine Figur des Spielers steht,
        # der momentan nicht ziehen kann
        if board.board[pos[0]][pos[1]] == None or board.board[pos[0]][pos[1]].color == board.turn:
            return 0

        value = 0

        own_pieces = [piece for piece in board.pieces if piece.color == board.turn]
        smallest_piece = None
        for piece in own_pieces:
            if piece.attacks_square(pos, board.board):
                if smallest_piece == None or self.piece_value[type(piece)] < self.piece_value[type(smallest_piece)]:
                    smallest_piece = piece
                    # Wenn die gefundene Figur ein Bauer ist, kann man keine kleinere Figur mehr finden
                    if type(piece) is Pawn:
                        break
        
        if smallest_piece != None:
            capture_move = None
            for move in smallest_piece.get_moves(board.board):
                if move.to == pos:
                    capture_move = move
                    break
            
            if capture_move != None:
                board.do_move(capture_move)
                value = max(0, self.piece_value[type(capture_move.captured)] - self.see(board, pos))
                board.undo_move(capture_move)
        
        return value
    
    # führt eine statische Evaluation des Spielfeldes durch
    def evaluate(self, board : Board, color : int, last_move : Move = None) -> float:
        value = 0

        own_queens = 0
        other_queens = 0
        own_minor_pieces = 0
        other_minor_pieces = 0


        for piece in board.pieces:
            if piece.color == color:
                value += self.piece_value[type(piece)]
                if isinstance(piece, Queen):
                    own_queens += 1
                
                if isinstance(piece, (Knight, Bishop)):
                    own_minor_pieces += 1
            else:
                value -= self.piece_value[type(piece)]
                if isinstance(piece, Queen):
                    other_queens += 1

                if isinstance(piece, (Knight, Bishop)):
                    other_minor_pieces += 1
        
        endgame = (own_queens == 0 and other_queens == 0) or (own_minor_pieces <= 1 and other_minor_pieces <= 1)

        own_pieces = [piece for piece in board.pieces if piece.color == color]
        other_pieces = [piece for piece in board.pieces if piece.color != color]

        for piece in own_pieces:
            value += self.get_pst_value(piece, endgame)
        
        for piece in other_pieces:
            value -= self.get_pst_value(piece, endgame)
        
        if last_move != None:
            last_moved_piece = board.board[last_move.to[0]][last_move.to[1]]
            captured_piece = last_move.captured

            captured_piece_val = 0
            if captured_piece != None:
                captured_piece_val = self.piece_value[type(captured_piece)] + self.get_pst_value(captured_piece, endgame)
            
            value += self.see(board, last_move.to) - captured_piece_val

        return value

    # sortiert die Züge nach dem SEE-Algorithmus
    def order_moves(self, moves : list, board : Board, depth : int) -> list:
        moves_copy = moves.copy()
        pv_moves = []

        # der beste gefundene Zug der letzten Iteration(wenn vorhanden und möglich)
        # kommt an den Anfang der Liste
        for move in self.last_depth_principal_variation:
            if move in moves_copy: 
                moves_copy.remove(move)
                pv_moves.append(move)
        
        winning_captures = []
        losing_captures = []
        killer_moves = []

        for move in moves_copy:
            if move.captured != None:
                board.do_move(move)
                if self.piece_value[type(move.captured)] - self.see(board, move.to) >= 0:
                    winning_captures.append(move)
                    moves_copy.remove(move)
                else:
                    losing_captures.append(move)
                    moves_copy.remove(move)
                board.undo_move(move)
            elif move in self.killer_moves[depth - 1]:
                killer_moves.append(move)
                moves_copy.remove(move)
        
        return pv_moves + winning_captures + killer_moves + moves_copy + losing_captures


    def alpha_beta(self, board : Board, depth : int, alpha : float, beta : float, principal_variation : list) -> float:
        # überprüfe, ob die Spielposition in der Transpositionstabelle enthalten ist
        if board.__hash__() in self.transposition_table:
            tt_entry = self.transposition_table[board.__hash__()]
            # der Eintrag in der Transpositionstabelle kann nur verwendet werden,
            # wenn die Suchtiefe nach dem Eintrag größer oder gleich der Suchtiefe ist,
            # mit der dieser Knoten noch bewertet werden soll
            if tt_entry.depth >= depth:
                # Wenn der Eintrag in der Transpositionstabelle ein exakter Eintrag ist,
                # dann wurden alle Kinder bewertet und wir wissen, dass das die tatsächliche Bewertung ist
                if tt_entry.entry_type == Transposition_Table_Entry_Type.EXACT:
                    principal_variation.clear()
                    principal_variation.extend(tt_entry.principal_variation)
                    return tt_entry.value
                # Dieser Knoten wurde letztes mal durch die Beta-Bedingung abgeschnitten
                elif tt_entry.entry_type == Transposition_Table_Entry_Type.LOWER_BOUND:
                    if tt_entry.value >= beta:
                        beta = tt_entry.value
                # Dieser Knoten wurde letztes mal vollständig bewertet, jedoch konnte alpha nicht verbessert werden
                elif tt_entry.entry_type == Transposition_Table_Entry_Type.UPPER_BOUND:
                    if tt_entry.value <= alpha:
                        alpha = tt_entry.value
                
                # Wenn sich Alpha und Beta überschneiden, dann ist die Bewertung des aktuellen Knotens nicht mehr relevant
                if alpha >= beta:
                    return tt_entry.value
        
        self.nodes_visited += 1

        if depth == 0:
            if len(board.move_history) == 0:
                return self.evaluate(board, board.turn)
            else:
                return self.evaluate(board, board.turn, board.move_history[-1])

        tt_type = Transposition_Table_Entry_Type.UPPER_BOUND

        # simuliere alle möglichen Züge
        for move in self.order_moves(board.get_legitimate_moves(board.turn), board, depth):
            board.do_move(move)
            child_pv = []
            val = -self.alpha_beta(board, depth - 1, -beta, -alpha, child_pv)
            board.undo_move(move)

            # Beta-Schnitt
            if val >= beta:
                self.transposition_table[board.__hash__()] = Transposition_Table_Entry(beta, depth, Transposition_Table_Entry_Type.LOWER_BOUND)
                self.killer_moves[depth - 1][0] = self.killer_moves[depth - 1][1]
                self.killer_moves[depth - 1][1] = move
                return beta

            # Wir konnten mit diesem Zug das Alpha verbessern
            if val > alpha:
                tt_type = Transposition_Table_Entry_Type.EXACT
                alpha = val

                principal_variation.clear()
                principal_variation.append(move)
                principal_variation.extend(child_pv)
            
            if not self.searching:
                self.last_search_interrupted = True
                return alpha
            
        # Eintrag in die Transpositionstabelle hinzufügen
        tt_entry = Transposition_Table_Entry(alpha, depth, tt_type)
        self.transposition_table[board.__hash__()] = tt_entry
        if tt_type == Transposition_Table_Entry_Type.EXACT:
            tt_entry.principal_variation = principal_variation.copy()

        return alpha
    
    def stop_search(self):
        self.searching = False
    
    def get_move(self, board : Board, search_time : float = 4, depth_incr : int = 1) -> Move:
        self.curr_depth = 0
        self.nodes_visited = 0
        self.searching = True
        self.last_search_interrupted = False
        self.last_depth_principal_variation = []
        self.killer_moves = []

        Timer(search_time, self.stop_search).start()

        while self.searching:
            self.curr_depth += depth_incr
            
            self.last_depth_principal_variation += [None] * (self.curr_depth - len(self.last_depth_principal_variation))
            self.killer_moves = [[None, None]] * (self.curr_depth - len(self.killer_moves)) + self.killer_moves

            pv = []

            self.alpha_beta(board, self.curr_depth, -inf, inf, pv)

            if not self.last_search_interrupted:
                print("Depth: " + str(self.curr_depth) + " | Nodes visited: " + str(self.nodes_visited))
                self.last_depth_principal_variation = pv
            
            self.best_move = self.last_depth_principal_variation[0] if len(self.last_depth_principal_variation) > 0 else None
        
        self.last_depth_principal_variation = [x for x in self.last_depth_principal_variation if x != None]
        
        print(f"PV of last full search(depth {self.curr_depth - 1}:)")

        for move in self.last_depth_principal_variation:
            print(move)

        return self.best_move


b = Board()

import time

WHITE = 0
BLACK = 1

starting_board = Board()
midgame_board = Board("r5k1/5ppp/1p6/p1p5/7b/1PPrqPP1/1PQ4P/R4R1K b - - 0 1")
endgame_board = Board("8/8/8/8/5R2/2pk4/5K2/8 b - - 0 1")

cp = Computer_Player()

start = int(round(time.time() * 1000000))
move = cp.get_move(endgame_board)
end = int(round(time.time() * 1000000))

print(f"Zug generiert nach {end - start}µs")