# Klasse, die einen regulären Schachzug kapselt
class Move:
    def __init__(self, from_pos : tuple, to_pos : tuple):
        self.fr = from_pos
        self.to = to_pos
        self.captured = None
        self.first_move = False
    
    def __str__(self):
        return f"{chr(self.fr[0] + 65)}{self.fr[1] + 1} -> {chr(self.to[0] + 65)}{self.to[1] + 1}"

# Oberklasse für alle Figuren
class Piece:
    def __init__(self, color : int):
        if color != 0 and color != 1:
            raise ValueError("color must be 0 or 1")
            
        self.color = color
        self.moved = False
    
    # Aktualisiert dias first_move-Attribut in allen Zügen in der Liste
    def set_first_move_in_list(self, moves : list):
        for move in moves:
            move.first_move = not self.moved

    # gibt alle möglichen horizontalen oder vertikalen Züge zurück(mit unendlicher Distanz)
    def get_straight_moves(self, board : list, pos : tuple) -> list:
        moves = []

        # Horizontal
        for x in range(pos[0] + 1, 8):
            if board[x][pos[1]] != None:
                if board[x][pos[1]].color != self.color:
                    move = Move(pos, (x, pos[1]))
                    move.captured = board[x][pos[1]]
                    moves.append(move)
                break
            moves.append(Move(pos, (x, pos[1])))
        
        for x in range(pos[0] - 1, -1, -1):
            if board[x][pos[1]] != None:
                if board[x][pos[1]].color != self.color:
                    move = Move(pos, (x, pos[1]))
                    move.captured = board[x][pos[1]]
                    moves.append(move)
                break
            moves.append(Move(pos, (x, pos[1])))
        
        # Vertikal
        for y in range(pos[1] + 1, 8):
            if board[pos[0]][y] != None:
                if board[pos[0]][y].color != self.color:
                    move = Move(pos, (pos[0], y))
                    move.captured = board[pos[0]][y]
                    moves.append(move)
                break
            moves.append(Move(pos, (pos[0], y)))

        for y in range(pos[1] - 1, -1, -1):
            if board[pos[0]][y] != None:
                if board[pos[0]][y].color != self.color:
                    move = Move(pos, (pos[0], y))
                    move.captured = board[pos[0]][y]
                    moves.append(move)
                break
            moves.append(Move(pos, (pos[0], y)))

        self.set_first_move_in_list(moves)

        return moves
    
    # gibt alle möglichen diagonalen Züge zurück(mit unendlicher Distanz)
    def get_diagonal_moves(self, board : list, pos : tuple) -> list:
        moves = []

        for x in range(1, 8):
            if pos[0] + x > 7 or pos[1] + x > 7:
                break
            if board[pos[0] + x][pos[1] + x] != None:
                if board[pos[0] + x][pos[1] + x].color != self.color:
                    move = Move(pos, (pos[0] + x, pos[1] + x))
                    move.captured = board[pos[0] + x][pos[1] + x]
                    moves.append(move)
                break
            moves.append(Move(pos, (pos[0] + x, pos[1] + x)))
        
        for x in range(1, 8):
            if pos[0] - x < 0 or pos[1] - x < 0:
                break
            if board[pos[0] - x][pos[1] - x] != None:
                if board[pos[0] - x][pos[1] - x].color != self.color:
                    move = Move(pos, (pos[0] - x, pos[1] - x))
                    move.captured = board[pos[0] - x][pos[1] - x]
                    moves.append(move)
                break
            moves.append(Move(pos, (pos[0] - x, pos[1] - x)))
        
        for x in range(1, 8):
            if pos[0] + x > 7 or pos[1] - x < 0:
                break
            if board[pos[0] + x][pos[1] - x] != None:
                if board[pos[0] + x][pos[1] - x].color != self.color:
                    move = Move(pos, (pos[0] + x, pos[1] - x))
                    move.captured = board[pos[0] + x][pos[1] - x]
                    moves.append(move)
                break
            moves.append(Move(pos, (pos[0] + x, pos[1] - x)))
        
        for x in range(1, 8):
            if pos[0] - x < 0 or pos[1] + x > 7:
                break
            if board[pos[0] - x][pos[1] + x] != None:
                if board[pos[0] - x][pos[1] + x].color != self.color:
                    move = Move(pos, (pos[0] - x, pos[1] + x))
                    move.captured = board[pos[0] - x][pos[1] + x]
                    moves.append(move)
                break
            moves.append(Move(pos, (pos[0] - x, pos[1] + x)))

        self.set_first_move_in_list(moves)

        return moves

    def get_moves(self, board : list, pos : tuple) -> list:
        raise NotImplementedError("get_moves not implemented on " + str(type(self)))

    # überprüft, ob diese Figur auf von einem Feld auf ein anderes Feld ziehen kann und es somit "angreift"
    def attacks_square(self, square: tuple, board : list, pos : tuple) -> bool:
        for move in self.get_moves(board, pos):
            if move.to == square:
                return True
        
        return False

# Klasse, die einen Rochadenzug kapselt
class Castling_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple, castling_rook_fr : tuple, castling_rook_to : tuple):
        super().__init__(from_pos, to_pos)
        self.castling_rook_fr = castling_rook_fr
        self.castling_rook_to = castling_rook_to

# Klasse, die einen En Passant Zug kapselt
class En_Passant_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple, en_passant_pos : tuple):
        super().__init__(from_pos, to_pos)
        self.en_passant_pos = en_passant_pos

# Klasse, die eine Bauernaufwertung kapselt
class Promotion_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple, promotion_piece : Piece):
        super().__init__(from_pos, to_pos)
        self.promotion_piece = promotion_piece
    
    def __str__(self):
        return f"{super().__str__()} -> {type(self.promotion_piece).__name__}"

# Klasse, die einen Doppelzug eines Bauern kapselt
class Pawn_Double_Move(Move):
    def __init__(self, from_pos : tuple, to_pos : tuple):
        super().__init__(from_pos, to_pos)

# Bauer
class Pawn(Piece):
    def __init__(self, color : int):
        super().__init__(color)
        # relevant für En Passant
        self.advanced_two_last_move = False

    def get_moves(self, board : list, pos : tuple) -> list:
        moves = []

        if self.color == 0:
            if pos[1] >= 7:
                return moves

            if board[pos[0]][pos[1] + 1] == None:
                moves.append(Move(pos, (pos[0], pos[1] + 1)))

                # Erster Zug vom Bauern
                if not self.moved:
                    if board[pos[0]][pos[1] + 2] == None:
                        moves.append(Pawn_Double_Move(pos, (pos[0], pos[1] + 2)))
                
            # Schlagen
            if pos[0] > 0 and board[pos[0] - 1][pos[1] + 1] != None and board[pos[0] - 1][pos[1] + 1].color != self.color:
                move = Move(pos, (pos[0] - 1, pos[1] + 1))
                move.captured = board[pos[0] - 1][pos[1] + 1]
                moves.append(move)
            
            if pos[0] < 7 and board[pos[0] + 1][pos[1] + 1] != None and board[pos[0] + 1][pos[1] + 1].color != self.color:
                move = Move(pos, (pos[0] + 1, pos[1] + 1))
                move.captured = board[pos[0] + 1][pos[1] + 1]
                moves.append(move)

            # En Passant
            if pos[1] == 4:
                if pos[0] > 0:
                    en_passant_pawn = board[pos[0] - 1][pos[1]]
                    if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                        move = En_Passant_Move(pos, (pos[0] - 1, pos[1] + 1), (pos[0] - 1, pos[1]))
                        move.captured = en_passant_pawn
                        moves.append(move)
                
                if pos[0] < 7:
                    en_passant_pawn = board[pos[0] + 1][pos[1]]
                    if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                        move = En_Passant_Move(pos, (pos[0] + 1, pos[1] + 1), (pos[0] + 1, pos[1]))
                        move.captured = en_passant_pawn
                        moves.append(move)

        else:
            if pos[1] <= 0:
                return moves

            if board[pos[0]][pos[1] - 1] == None:
                moves.append(Move(pos, (pos[0], pos[1] - 1)))

                # Erster Zug vom Bauern
                if not self.moved:
                    if board[pos[0]][pos[1] - 2] == None:
                        moves.append(Pawn_Double_Move(pos, (pos[0], pos[1] - 2)))
                
            # Schlagen
            if pos[0] > 0 and board[pos[0] - 1][pos[1] - 1] != None and board[pos[0] - 1][pos[1] - 1].color != self.color:
                move = Move(pos, (pos[0] - 1, pos[1] - 1))
                move.captured = board[pos[0] - 1][pos[1] - 1]
                moves.append(move)

            if pos[0] < 7 and board[pos[0] + 1][pos[1] - 1] != None and board[pos[0] + 1][pos[1] - 1].color != self.color:
                move = Move(pos, (pos[0] + 1, pos[1] - 1))
                move.captured = board[pos[0] + 1][pos[1] - 1]
                moves.append(move)
            
            # En Passant
            if pos[1] == 3:
                if pos[0] > 0:
                    en_passant_pawn = board[pos[0] - 1][pos[1]]
                    if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                        move = En_Passant_Move(pos, (pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1]))
                        move.captured = en_passant_pawn
                        moves.append(move)
                
                if pos[0] < 7:
                    en_passant_pawn = board[pos[0] + 1][pos[1]]
                    if en_passant_pawn != None and en_passant_pawn.color != self.color and isinstance(en_passant_pawn, Pawn) and en_passant_pawn.advanced_two_last_move:
                        move = En_Passant_Move(pos, (pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1]))
                        move.captured = en_passant_pawn
                        moves.append(move)

        # Mache aus allen Umwandlungen Promotion_Moves
        # iteriere über eine Kopie aller Züge, damit wir die Originalliste verändern können
        for move in list(moves):
            if move.to[1] == 0 or move.to[1] == 7:
                # Bauern können in Damen, Türmen, Läufern und Springer umwandeln
                moves.append(Promotion_Move(move.fr, move.to, Queen(self.color)))
                moves.append(Promotion_Move(move.fr, move.to, Rook(self.color)))
                moves.append(Promotion_Move(move.fr, move.to, Bishop(self.color)))
                moves.append(Promotion_Move(move.fr, move.to, Knight(self.color)))

                # entferne den alten Zug
                moves.remove(move)
                

        self.set_first_move_in_list(moves)

        return moves
    
    def attacks_square(self, square : tuple, board : list, pos : tuple):
        if self.color == 0:
            if square[0] == pos[0] - 1 and square[1] == pos[1] + 1:
                return True
            if square[0] == pos[0] + 1 and square[1] == pos[1] + 1:
                return True
        else:
            if square[0] == pos[0] - 1 and square[1] == pos[1] - 1:
                return True
            if square[0] == pos[0] + 1 and square[1] == pos[1] - 1:
                return True
        
        return False

# Turm
class Rook(Piece):
    def get_moves(self, board : list, pos : tuple) -> list:
        return self.get_straight_moves(board, pos)
    
    def attacks_square(self, square : tuple, board : list, pos : tuple):
        # überprüfe, ob das zu überprüfende Feld in derselben Zeile liegt
        if square[0] == pos[0]:
            if square[1] < pos[1]:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(square[1] + 1, pos[1]):
                    if board[pos[0]][i] != None:
                        return False
                return True
            else:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(pos[1] + 1, square[1]):
                    if board[pos[0]][i] != None:
                        return False
                return True
        elif square[1] == pos[1]:
            if square[0] < pos[0]:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(square[0] + 1, pos[0]):
                    if board[i][pos[1]] != None:
                        return False
                return True
            else:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(pos[0] + 1, square[0]):
                    if board[i][pos[1]] != None:
                        return False
                return True
        
        return False
            

# Springer
class Knight(Piece):
    directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def get_moves(self, board : list, pos : tuple) -> list:
        moves = []

        for direction in Knight.directions:
            if pos[0] + direction[0] > 7 or pos[0] + direction[0] < 0:
                continue
            if pos[1] + direction[1] > 7 or pos[1] + direction[1] < 0:
                continue
            if board[pos[0] + direction[0]][pos[1] + direction[1]] != None:
                if board[pos[0] + direction[0]][pos[1] + direction[1]].color != self.color:
                    move = Move(pos, (pos[0] + direction[0], pos[1] + direction[1]))
                    move.captured = board[pos[0] + direction[0]][pos[1] + direction[1]]
                    moves.append(move)
                continue
            moves.append(Move(pos, (pos[0] + direction[0], pos[1] + direction[1])))
        
        self.set_first_move_in_list(moves)

        return moves
    
    def attacks_square(self, square : tuple, board : list, pos : tuple):
        row_diff = abs(square[0] - pos[0])
        col_diff = abs(square[1] - pos[1])

        return row_diff == 2 and col_diff == 1 or row_diff == 1 and col_diff == 2

# Läufer
class Bishop(Piece):
    def get_moves(self, board : list, pos : tuple) -> list:
        return self.get_diagonal_moves(board, pos)
    
    def attacks_square(self, square : tuple, board : list, pos : tuple):
        row_diff = square[0] - pos[0]
        col_diff = square[1] - pos[1]

        # überprüfe, ob das zu überprüfende Feld in derselben Diagonale liegt
        if abs(row_diff) == abs(col_diff):
            for i in range(1, abs(row_diff)):
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                if board[pos[0] + i * row_diff // abs(row_diff)][pos[1] + i * col_diff // abs(col_diff)] != None:
                    return False
            return True

        return False

# Dame
class Queen(Piece):
    def get_moves(self, board : list, pos : tuple) -> list:
        return self.get_straight_moves(board, pos) + self.get_diagonal_moves(board, pos)

    def attacks_square(self, square : tuple, board : list, pos : tuple):
        row_diff = square[0] - pos[0]
        col_diff = square[1] - pos[1]

        # überprüfe, ob das zu überprüfende Feld in derselben Zeile liegt
        if row_diff == 0:
            if square[1] < pos[1]:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(square[1] + 1, pos[1]):
                    if board[pos[0]][i] != None:
                        return False
                return True
            else:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(pos[1] + 1, square[1]):
                    if board[pos[0]][i] != None:
                        return False
                return True
        elif col_diff == 0:
            if square[0] < pos[0]:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(square[0] + 1, pos[0]):
                    if board[i][pos[1]] != None:
                        return False
                return True
            else:
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                for i in range(pos[0] + 1, square[0]):
                    if board[i][pos[1]] != None:
                        return False
                return True
        # überprüfe, ob das zu überprüfende Feld in derselben Diagonale liegt
        elif abs(row_diff) == abs(col_diff):
            for i in range(1, abs(row_diff)):
                # überprüfe, ob eine Figur zwischen beiden Feldern steht
                if board[pos[0] + i * row_diff // abs(row_diff)][pos[1] + i * col_diff // abs(col_diff)] != None:
                    return False
            return True
        
        return False

# König
class King(Piece):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def get_moves(self, board : list, pos : tuple) -> list:
        moves = []

        for direction in King.directions:
            if pos[0] + direction[0] > 7 or pos[0] + direction[0] < 0:
                continue
            if pos[1] + direction[1] > 7 or pos[1] + direction[1] < 0:
                continue
            if board[pos[0] + direction[0]][pos[1] + direction[1]] != None:
                if board[pos[0] + direction[0]][pos[1] + direction[1]].color != self.color:
                    move = Move(pos, (pos[0] + direction[0], pos[1] + direction[1]))
                    move.captured = board[pos[0] + direction[0]][pos[1] + direction[1]]
                    moves.append(move)
                continue
            moves.append(Move(pos, (pos[0] + direction[0], pos[1] + direction[1])))
        
        # Rochade
        # Bedingung für Rochade:
        # 1. König und Turm haben sich nicht bewegt
        # 2. Zwischen König und Turm ist keine andere Figur
        # 3. König und alle Felder zwischen Turm und König werden nicht angegriffen

        # Bedingung 1
        if not self.moved:
            enemy_pieces = {board[i][j] : (i, j) for i in range(8) for j in range(8) if board[i][j] != None and board[i][j].color != self.color}
            if self.color == 0:
                if pos == (4, 0):
                    left_corner_piece = board[0][0]
                    right_corner_piece = board[7][0]

                    # Bedingung 2 für Weiss auf Königseite
                    if board[5][0] == None and board[6][0] == None and isinstance(right_corner_piece, Rook) and right_corner_piece.color == self.color and not right_corner_piece.moved:
                        # Bedingung 3 für Weiss auf Königseite
                        path = [(4, 0), (5,0)]
                        if not any(piece.attacks_square(square, board, enemy_pieces[piece]) for piece in enemy_pieces.keys() for square in path):
                            new_move = Castling_Move(pos, (6, 0), (7, 0), (5, 0))
                            moves.append(new_move)
                    
                    # Bedingung 2 für Weiss auf Damenseite
                    if board[1][0] == None and board[2][0] == None and board[3][0] == None and isinstance(left_corner_piece, Rook) and left_corner_piece.color == self.color and not left_corner_piece.moved:
                        # Bedingung 3 für Weiss auf Damenseite
                        path = [(4, 0), (3, 0)]
                        if not any(piece.attacks_square(square, board, enemy_pieces[piece]) for piece in enemy_pieces.keys() for square in path):
                            new_move = Castling_Move(pos, (2, 0), (0, 0), (3, 0))
                            moves.append(new_move)
            else:
                if pos == (4, 7):
                    left_corner_piece = board[0][7]
                    right_corner_piece = board[7][7]

                    # Bedingung 2 für Schwarz auf Königseite
                    if board[5][7] == None and board[6][7] == None and isinstance(right_corner_piece, Rook) and right_corner_piece.color == self.color and not right_corner_piece.moved:
                        # Bedingung 3 für Schwarz auf Königseite
                        path = [(4, 7), (5,7)]
                        if not any(piece.attacks_square(square, board, enemy_pieces[piece]) for piece in enemy_pieces.keys() for square in path):
                            new_move = Castling_Move(pos, (6, 7), (7, 7), (5, 7))
                            moves.append(new_move)
                    
                    # Bedingung 2 für Schwarz auf Damenseite
                    if board[1][7] == None and board[2][7] == None and board[3][7] == None and isinstance(left_corner_piece, Rook) and left_corner_piece.color == self.color and not left_corner_piece.moved:
                        # Bedingung 3 für Schwarz auf Damenseite
                        path = [(4, 7), (3, 7)]
                        if not any(piece.attacks_square(square, board, enemy_pieces[piece]) for piece in enemy_pieces.keys() for square in path):
                            new_move = Castling_Move(pos, (2, 7), (0, 7), (3, 7))
                            moves.append(new_move)

        self.set_first_move_in_list(moves)

        return moves
    
    def attacks_square(self, square : tuple, board : list, pos : tuple):
        row_diff = abs(square[0] - pos[0])
        col_diff = abs(square[1] - pos[1])

        return row_diff <= 1 and col_diff <= 1

# Stellt ein Schachbrett dar
# kann Züge generieren auf das Schachbrett ausführen
class Board:
    def __init__(self, fen_string : str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"):
        self.turn = 0
        self.board = [[None for x in range(8)] for y in range(8)]

        # Initialisiere die Figuren
        self.read_fen_string(fen_string)
        
        self.pieces = {}
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != None:
                    self.pieces[self.board[x][y]] = (x, y)
        
        kings = [x for x in self.pieces.keys() if isinstance(x, King)]
        if len(kings) != 2 or kings[0].color == kings[1].color:
            raise ValueError("Invalid FEN string: Both colors must have exactly one King")
        
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
                    self.board[col][row] = King(color)
                elif char == 'q':
                    self.board[col][row] = Queen(color)
                elif char == 'r':
                    self.board[col][row] = Rook(color)
                elif char == 'b':
                    self.board[col][row] = Bishop(color)
                elif char == 'n':
                    self.board[col][row] = Knight(color)
                elif char == 'p':
                    self.board[col][row] = Pawn(color)
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

    def get_legitimate_moves_from_piece(self, piece : Piece) -> list:
        if not piece in self.pieces:
            raise ValueError("Piece not on board")
        
        moves = []

        king = [x for x in self.pieces.keys() if isinstance(x, King) and x.color == piece.color][0]

        for move in piece.get_moves(self.board, self.pieces[piece]):
            self.do_move(move)
            enemy_pieces = [x for x in self.pieces.keys() if x.color != piece.color]
            if not any(x.attacks_square(self.pieces[king], self.board, self.pieces[x]) for x in enemy_pieces):
                moves.append(move)

            self.undo_move(move)
        
        return moves

    def get_legitimate_moves_from_pos(self, pos : tuple) -> list:
        self.get_legitimate_moves_from_piece(self.board[pos[0]][pos[1]])

    # gibt alle legitimen Züge eines Spielers zurück
    # wenn die Liste leer ist, dann ist der Spieler Schachmatt
    def get_legitimate_moves(self, color : int) -> list:
        moves = []

        own_pieces = [x for x in self.pieces.keys() if x.color == color]

        for piece in own_pieces:
            moves += self.get_legitimate_moves_from_piece(piece)
            
        return moves
    
    # führt einen Zug aus
    def do_move(self, move : Move):
        self.board[move.to[0]][move.to[1]] = self.board[move.fr[0]][move.fr[1]]
        self.board[move.to[0]][move.to[1]].moved = True
        self.board[move.fr[0]][move.fr[1]] = None
        self.pieces[self.board[move.to[0]][move.to[1]]] = move.to
        
        if move.captured != None:
            self.pieces.pop(move.captured)

        for piece in self.pieces.keys():
            if isinstance(piece, Pawn):
                piece.advanced_two_last_move = False
        
        if isinstance(move, Pawn_Double_Move):
            self.board[move.to[0]][move.to[1]].advanced_two_last_move = True
        elif isinstance(move, Castling_Move):
            self.board[move.castling_rook_to[0]][move.castling_rook_to[1]] = self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]]
            self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]] = None
            self.pieces[self.board[move.castling_rook_to[0]][move.castling_rook_to[1]]] = move.castling_rook_to
        elif isinstance(move, Promotion_Move):
            self.pieces.pop(self.board[move.to[0]][move.to[1]])
            self.board[move.to[0]][move.to[1]] = move.promotion_piece
            self.pieces[move.promotion_piece] = move.to
        elif isinstance(move, En_Passant_Move):
            self.board[move.en_passant_pos[0]][move.en_passant_pos[1]] = None
    
    # macht einen Zug rückgängig
    def undo_move(self, move : Move):
        self.board[move.fr[0]][move.fr[1]] = self.board[move.to[0]][move.to[1]]
        self.board[move.fr[0]][move.fr[1]].moved = not move.first_move
        self.board[move.to[0]][move.to[1]] = None
        self.pieces[self.board[move.fr[0]][move.fr[1]]] = move.fr

        if move.captured != None:
            self.board[move.to[0]][move.to[1]] = move.captured
            self.pieces[move.captured] = move.to
        
        if isinstance(move, Pawn_Double_Move):
            self.board[move.fr[0]][move.fr[1]].advanced_two_last_move = False
        elif isinstance(move, Castling_Move):
            self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]] = self.board[move.castling_rook_to[0]][move.castling_rook_to[1]]
            self.board[move.castling_rook_to[0]][move.castling_rook_to[1]] = None
            self.pieces[self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]]] = move.castling_rook_fr
        elif isinstance(move, Promotion_Move):
            new_pawn = Pawn(move.promotion_piece.color)
            new_pawn.moved = True
            self.board[move.fr[0]][move.fr[1]] = new_pawn
            self.board[move.to[0]][move.to[1]] = None
            self.pieces[new_pawn] = move.fr
            self.pieces.pop(move.promotion_piece)
        elif isinstance(move, En_Passant_Move):
            new_pawn = Pawn(move.captured.color)
            new_pawn.moved = True
            new_pawn.advanced_two_last_move = True
            self.board[move.en_passant_pos[0]][move.en_passant_pos[1]] = new_pawn
            self.pieces[new_pawn] = move.en_passant_pos

b = Board()

import time

WHITE = 0
BLACK = 1

starting_board = Board()
midgame_board = Board("r5k1/5ppp/1p6/p1p5/7b/1PPrqPP1/1PQ4P/R4R1K b - - 0 1")
endgame_board = Board("8/8/8/8/5R2/2pk4/5K2/8 b - - 0 1")

start = int(round(time.time() * 1000000))
moves = b.get_legitimate_moves(0)
end = int(round(time.time() * 1000000))

print(f"{len(moves)} legitime Züge in {end - start}µs generiert")

for move in moves:
    print(move)