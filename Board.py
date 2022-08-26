from ChessUtils import *

from collections import defaultdict
from uuid import uuid4

# Stellt ein Schachbrett dar
# kann Züge generieren auf das Schachbrett ausführen
class Board:
    def __init__(self, fen_string : str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.turn = 0
        self.board = [[None for x in range(8)] for y in range(8)]

        # Initialisiere die Figuren
        self.read_fen_string(fen_string)
        
        self.pieces = []
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != None:
                    self.pieces.append(self.board[x][y])
        
        # überprüfe, ob beide Farben genau einen König haben
        kings = [x for x in self.pieces if isinstance(x, King)]
        if len(kings) != 2 or kings[0].color == kings[1].color:
            raise ValueError("Invalid FEN string: Both colors must have exactly one King")
        
        self.kings = kings
        self.kings.sort(key=lambda x: x.color)

        self.en_passantable_pawn = None
        
        # Initialisiere die Wiederholungstabelle
        # Die Tabelle speichert, wie häufig eine Position aufgetreten ist
        self.repetition_table = defaultdict(lambda : 0)
        
        self.move_history = []
        
        self.init_zobrist()

        self.hash = self.__hash__()
        self.repetition_table[self.hash] = 1
    
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
        
    # initialisiere die Zobrist-Tabelle
    def init_zobrist(self):
        self.zobrist_table = [[] for j in range(64)]

        for square in self.zobrist_table:
            for i in range(18):
                # Nur die ersten 64 Bits werden benutzt
                square.append(uuid4().int & 0xffffffff)
        
        self.black_to_move = uuid4().int & 0xffffffff
    
    # gibt zu einer Figur den Index zurück,
    # mit dem man auf den richtigen Wert in der Zobrist-Tabelle zugreifen kann
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
    
        for piece in self.pieces:
            res ^= self.zobrist_table[piece.pos[0] * 8 + piece.pos[1]][self.get_zobrist_piece_value(piece)]

        return res

    # berechnet aus dem vorherigen Hash und dem letzten ausgeführten Zug den neuen Zobrist-Hash
    def get_hash_after_move(self, move : Move) -> int:
        # Spielfarbe wechseln
        new_hash = self.hash ^ self.black_to_move

        if isinstance(move, Promotion_Move):
            moving_piece = move.promoted_piece
            # Neue aufgewertete Figur ein-XORen
            new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(move.promotion_piece)]
            # Und alten Bauern raus-XORen
            new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(moving_piece)]
        else:
            moving_piece = self.board[move.to[0]][move.to[1]]
        # Bewegte Figur von alter Position raus-XORen
        # Wenn die Figur zum ersten mal bewegt wurde, muss man die unbewegte Variante raus XORen
        if move.first_move:
            if isinstance(move, Pawn_Double_Move):
                new_hash ^= self.zobrist_table[move.fr[0] * 8 + move.fr[1]][self.get_zobrist_piece_value(moving_piece) - 8]
            elif isinstance(moving_piece, Rook):
                new_hash ^= self.zobrist_table[move.fr[0] * 8 + move.fr[1]][self.get_zobrist_piece_value(moving_piece) - 5]
            elif isinstance(moving_piece, King):
                new_hash ^= self.zobrist_table[move.fr[0] * 8 + move.fr[1]][self.get_zobrist_piece_value(moving_piece) - 2]
            else:
                new_hash ^= self.zobrist_table[move.fr[0] * 8 + move.fr[1]][self.get_zobrist_piece_value(moving_piece)]
        else:
            new_hash ^= self.zobrist_table[move.fr[0] * 8 + move.fr[1]][self.get_zobrist_piece_value(moving_piece)]

        # Geschlagene Figur "raus-XORen"
        if move.captured != None:
            if isinstance(move, En_Passant_Move):
                new_hash ^= self.zobrist_table[move.en_passant_pos[0] * 8 + move.en_passant_pos[1]][self.get_zobrist_piece_value(move.captured)]
            else:
                new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(move.captured)]
            
        new_hash ^= self.zobrist_table[move.to[0] * 8 + move.to[1]][self.get_zobrist_piece_value(moving_piece)]

        # Rochade "ein-XORen"
        if isinstance(move, Castling_Move):
            new_hash ^= self.zobrist_table[move.castling_rook_fr[0] * 8 + move.castling_rook_fr[1]][self.get_zobrist_piece_value(self.board[move.castling_rook_to[0]][move.castling_rook_to[1]])]
            new_hash ^= self.zobrist_table[move.castling_rook_to[0] * 8 + move.castling_rook_to[1]][self.get_zobrist_piece_value(self.board[move.castling_rook_to[0]][move.castling_rook_to[1]])]
        
        # Wenn ein Bauer nicht mehr En-Passant geschlagen werden kann, müssen wir den Hash ändern
        if move.undone_advanced_two_last_move != None and move.undone_advanced_two_last_move != move.captured:
            pawn = move.undone_advanced_two_last_move
            # Bauern der En-Passant geschlagen werden kann raus-XORen
            new_hash ^= self.zobrist_table[pawn.pos[0] * 8 + pawn.pos[1]][self.get_zobrist_piece_value(pawn) + 8]
            # Bauern der nicht En-Passant geschlagen werden kann ein-XORen
            new_hash ^= self.zobrist_table[pawn.pos[0] * 8 + pawn.pos[1]][self.get_zobrist_piece_value(pawn)]

        return new_hash

        
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
                    if not ((color == 0 and row == 0 and col in [0, 7]) or (color == 1 and row == 7 and col in [0, 7])):
                        self.board[col][row].moved = True
                elif char == 'b':
                    self.board[col][row] = Bishop(color, (col, row))
                elif char == 'n':
                    self.board[col][row] = Knight(color, (col, row))
                elif char == 'p':
                    self.board[col][row] = Pawn(color, (col, row))
                    if not ((color == 0 and row == 1) or (color == 1 and row == 6)):
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
                self.en_passantable_pawn = possible_pawn
            else:
                raise ValueError(f"Invalid FEN-String: Invalid En Passant Square {strings[3]} (must be a square where a pawn of the other color can be captured)")
        
        # Teil 5 und Teil 6(Halfmove- und Fullmove-Nummern) sind in diesem Projekt nicht relevant und werden hier ignoriert

    def is_draw_by_repetition(self):
        return self.repetition_table[self.hash] >= 3

    # gibt alle machbaren Züge einer Farbe zurück
    # enthält Züge, die den eigenen König im Schach lassen(illegal)!
    def get_moves(self, color : int) -> list:
        moves = []

        own_pieces = [x for x in self.pieces if x.color == color]

        for piece in own_pieces:
            moves += piece.get_moves(self.board)
        
        return moves
    
    # überprüft, ob eine Farbe in Schach ist
    def is_in_check(self, color : int) -> bool:
        other_pieces = [x for x in self.pieces if x.color != color]
        own_king = self.kings[color]

        return any(piece.attacks_square(own_king.pos, self.board) for piece in other_pieces)


    # gibt alle legalen Züge einer Figur zurück
    def get_legal_moves_from_piece(self, piece : Piece) -> list:
        if not piece in self.pieces:
            raise ValueError("Piece not on board")
        
        moves = []

        king = [x for x in self.pieces if isinstance(x, King) and x.color == piece.color][0]

        for move in piece.get_moves(self.board):
            self.do_move(move, False)
            if not self.is_in_check(piece.color):
                moves.append(move)

            self.undo_move(move, False)
        
        return moves

    # gibt alle legalen Züge einer Figur zurück
    def get_legal_moves_from_pos(self, pos : tuple) -> list:
        self.get_legal_moves_from_piece(self.board[pos[0]][pos[1]])

    # gibt alle legalen Züge eines Spielers zurück
    # wenn die Liste leer ist, dann ist der Spieler Schachmatt
    def get_legal_moves(self, color : int) -> list:
        moves = []

        king = self.kings[color]
        own_pieces = [x for x in self.pieces if x.color == color]
        enemy_pieces = [x for x in self.pieces if x.color != color]

        # Es reicht i.d.R., die gegnerischen Figuren zu betrachten, die den König auf einem sonst leeren Feld in Schach stellen
        potential_enemy_attackers = [x for x in self.pieces if x.color != color and x.attacks_square_on_empty_board(king.pos)]

        for piece in own_pieces:
            for move in piece.get_moves(self.board):
                self.do_move(move, False)

                # Wenn der König bewegt wurde, müssen alle gegnerischen Figuren betrachtet werden
                if isinstance(self.board[move.to[0]][move.to[1]], King):
                    if not self.is_in_check(color):
                        moves.append(move)
                else:
                    if not any(x.attacks_square(king.pos, self.board) for x in potential_enemy_attackers if move.captured != x):
                        moves.append(move)

                self.undo_move(move, False)
            
        return moves
    
    # führt einen Zug aus
    def do_move(self, move : Move, update_hash : bool = True):
        if self.board[move.fr[0]][move.fr[1]] == None:
            raise ValueError("Piece does not exist")

        if move.captured != None:
            self.pieces.remove(move.captured)
            if move.captured == self.en_passantable_pawn:
                move.undone_advanced_two_last_move = self.en_passantable_pawn
                self.en_passantable_pawn = None
        
        moving_piece = self.board[move.fr[0]][move.fr[1]]
        self.board[move.to[0]][move.to[1]] = moving_piece
        self.board[move.fr[0]][move.fr[1]] = None
        moving_piece.pos = move.to
        moving_piece.moved = True

        if isinstance(move, Pawn_Double_Move):
            if self.en_passantable_pawn != None:
                self.en_passantable_pawn.advanced_two_last_move = False
                move.undone_advanced_two_last_move = self.en_passantable_pawn
            
            moving_piece.advanced_two_last_move = True
            self.en_passantable_pawn = moving_piece
        elif isinstance(move, Castling_Move):
            castling_rook = self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]]
            self.board[move.castling_rook_to[0]][move.castling_rook_to[1]] = castling_rook
            self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]] = None
            castling_rook.pos = move.castling_rook_to
        elif isinstance(move, Promotion_Move):
            self.board[move.to[0]][move.to[1]] = move.promotion_piece
            move.promotion_piece.pos = move.to
            self.pieces.remove(move.promoted_piece)
            self.pieces.append(move.promotion_piece)
        elif isinstance(move, En_Passant_Move):
            self.board[move.en_passant_pos[0]][move.en_passant_pos[1]] = None
        
        if self.en_passantable_pawn != None and self.en_passantable_pawn != move.captured:
            if self.en_passantable_pawn != moving_piece or not isinstance(move, Pawn_Double_Move):
                self.en_passantable_pawn.advanced_two_last_move = False
                move.undone_advanced_two_last_move = self.en_passantable_pawn
                self.en_passantable_pawn = None
        
        self.turn = 1 - self.turn

        self.move_history.append(move)

        if update_hash:
            move.hash_before = self.hash
            self.hash = self.get_hash_after_move(move)
            self.repetition_table[self.hash] += 1
    
    # macht einen Zug rückgängig
    def undo_move(self, move : Move, update_hash : bool = True):
        if move != self.move_history[-1]:
            raise ValueError("Can only undo last move")
        
        if update_hash:
            self.repetition_table[self.hash] -= 1
            if self.repetition_table[self.hash] == 0:
                self.repetition_table.pop(self.hash)
        
        moving_piece = self.board[move.to[0]][move.to[1]]

        self.board[move.fr[0]][move.fr[1]] = moving_piece
        self.board[move.to[0]][move.to[1]] = None
        moving_piece.pos = move.fr
        moving_piece.moved = not move.first_move

        if move.captured != None and not isinstance(move, En_Passant_Move):
            self.board[move.to[0]][move.to[1]] = move.captured
            move.captured.pos = move.to
            self.pieces.append(move.captured)
        if isinstance(move, Pawn_Double_Move):
            moving_piece.advanced_two_last_move = False
            self.en_passantable_pawn = None
        elif isinstance(move, Castling_Move):
            castling_rook = self.board[move.castling_rook_to[0]][move.castling_rook_to[1]]
            self.board[move.castling_rook_fr[0]][move.castling_rook_fr[1]] = castling_rook
            self.board[move.castling_rook_to[0]][move.castling_rook_to[1]] = None
            castling_rook.pos = move.castling_rook_fr
        elif isinstance(move, Promotion_Move):
            self.board[move.fr[0]][move.fr[1]] = move.promoted_piece
            move.promoted_piece.pos = move.fr
            self.pieces.remove(move.promotion_piece)
            self.pieces.append(move.promoted_piece)
        elif isinstance(move, En_Passant_Move):
            self.board[move.en_passant_pos[0]][move.en_passant_pos[1]] = move.captured
            move.captured.pos = move.en_passant_pos
            move.captured.advanced_two_last_move = True
            self.pieces.append(move.captured)
        
        if move.undone_advanced_two_last_move != None:
            pawn = move.undone_advanced_two_last_move
            pawn.advanced_two_last_move = True
            self.en_passantable_pawn = pawn
        
        self.turn = 1 - self.turn

        if update_hash:
            if move.hash_before != None:
                self.hash = move.hash_before
            else:
                self.hash = self.__hash__()

        self.move_history.pop()