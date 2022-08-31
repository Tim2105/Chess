from Board import *

from enum import Enum
from math import exp
from threading import Timer

# Enumeration für alle möglichen Typen von TT-Einträgen
class Transposition_Table_Entry_Type(Enum):
    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2
    QUIESCENT = 3

# Kapselt einen Eintrag in der Transpositionstabelle
class Transposition_Table_Entry:
    def __init__(self, value : int, depth: int, entry_type : Transposition_Table_Entry_Type):
        self.value = value
        self.depth = depth
        self.entry_type = entry_type
        self.move = None
        self.killer_moves = [None, None]

# Enthält alle Attribute und Methoden, die ein Schachcomputer benötigt
class ChessComputer:
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
            [  0,  0,  0,  0,  0,  0,  0,  0],
            [ 50, 50, 50, 50, 50, 50, 50, 50],
            [ 10, 10, 20, 30, 30, 20, 10, 10],
            [  5,  5, 10, 25, 25, 10,  5,  5],
            [  0,  0,  0, 20, 20,  0,  0,  0],
            [  5, -5,-10,  0,  0,-10, -5,  5],
            [  5, 10, 10,-20,-20, 10, 10,  5],
            [  0,  0,  0,  0,  0,  0,  0,  0]
        ],
        Knight : [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ],
        Bishop : [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ],
        Rook : [
            [  0,  0,  0,  0,  0,  0,  0,  0],
            [  5, 10, 10, 10, 10, 10, 10,  5],
            [ -5,  0,  0,  0,  0,  0,  0, -5],
            [ -5,  0,  0,  0,  0,  0,  0, -5],
            [ -5,  0,  0,  0,  0,  0,  0, -5],
            [ -5,  0,  0,  0,  0,  0,  0, -5],
            [ -5,  0,  0,  0,  0,  0,  0, -5],
            [  0,  0,  0,  5,  5,  0,  0,  0]
        ],
        Queen : [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [ -5,  0,  5,  5,  5,  5,  0, -5],
            [  0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ],
        King : [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [ 20, 20,  0,  0,  0,  0, 20, 20],
            [ 20, 30, 10,  0,  0, 10, 30, 20]
        ]
    }

    # Piece-Square Tables für das Endspiel
    # nur relevant für König und Bauern
    pst_endgame = {
        Pawn : [
            [  0,  0,  0,  0,  0,  0,  0,  0],
            [ 80, 80, 80, 80, 80, 80, 80, 80],
            [ 40, 40, 50, 50, 50, 50, 40, 40],
            [ 15, 15, 20, 30, 30, 20, 15, 15],
            [  0,  0,  0, 20, 20,  0,  0,  0],
            [  5, -5,-10,  0,  0,-10, -5,  5],
            [  5, 10, 10,-20,-20, 10, 10,  5],
            [  0,  0,  0,  0,  0,  0,  0,  0]
        ],
        Knight : pst_midgame[Knight],
        Bishop : pst_midgame[Bishop],
        Rook : pst_midgame[Rook],
        Queen : pst_midgame[Queen],
        King : [
            [-50,-40,-30,-20,-20,-30,-40,-50],
            [-30,-20,-10,  0,  0,-10,-20,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-30,  0,  0,  0,  0,-30,-30],
            [-50,-30,-30,-30,-30,-30,-30,-50]
        ]
    }

    MATE_SCORE : int = 100000
    INFINITY : int = 1 << 32
    MAX_QUIESCENCE_CHECK_DEPTH : int = 4

    def __init__(self):
        self.searching = False
        self.curr_depth = 0
        self.transposition_table = {}
        self.best_move = None
        self.last_search_interrupted = False
        self.mate_found = False

    # gibt den PST-Wert für eine Figur zurück
    def get_pst_value(self, piece : Piece, use_endgame_values = False) -> int:
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
    # und gibt die Veränderung im Material zurück(- -> verloren, + -> gewonnen oder 0)
    # tatsächlich gibt SEE nie eine negative Zahl zurück, weil der momentane Spieler die Schlagkette nicht anfangen muss,
    # wenn er verlieren würde : SEE gibt in diesem Fall 0 zurück
    # Quelle : https://www.researchgate.net/publication/298853351_STATIC_EXCHANGE_EVALUATION_WITH_alpha_beta-APPROACH
    def see(self, board : Board, pos : tuple) -> int:
        # SEE funktioniert nur auf Feldern wo eine Figur des Spielers steht,
        # der momentan nicht ziehen kann
        if board.board[pos[0]][pos[1]] == None or board.board[pos[0]][pos[1]].color == board.turn:
            return 0

        value = 0

        own_pieces = [piece for piece in board.pieces if piece.color == board.turn]

        # finde die kleinste Figur, die sqaure angreifen kann
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
                board.do_move(capture_move, False)
                value = max(0, self.piece_value[type(capture_move.captured)] - self.see(board, pos))
                board.undo_move(False)
        
        return value
    
    # führt eine statische Evaluation des Spielfeldes durch
    # Quelle : https://www.chessprogramming.org/Simplified_Evaluation_Function
    def evaluate(self, board : Board, color : int, last_move : Move = None) -> int:
        value = 0

        own_queens = 0
        other_queens = 0

        own_minor_pieces = 0
        other_minor_pieces = 0

        own_piece_value = 0
        other_piece_value = 0

        # Addiere Figurenbewertungen und zähle die Anzahl der Damen und Leichtfiguren (+ Turm)
        for piece in board.pieces:
            if piece.color == color:
                own_piece_value += self.piece_value[type(piece)]
                if isinstance(piece, Queen):
                    own_queens += 1
                
                if isinstance(piece, (Knight, Bishop)):
                    own_minor_pieces += 1
            else:
                other_piece_value += self.piece_value[type(piece)]
                if isinstance(piece, Queen):
                    other_queens += 1

                if isinstance(piece, (Knight, Bishop)):
                    other_minor_pieces += 1
        
        value += own_piece_value - other_piece_value
        
        # Überprüfe, ob wir uns im Endspiel befinden
        self_in_endgame = own_queens == 0 or own_minor_pieces < 2
        other_in_endgame = other_queens == 0 or other_minor_pieces < 2

        endgame = self_in_endgame and other_in_endgame

        own_pieces = [piece for piece in board.pieces if piece.color == color]
        other_pieces = [piece for piece in board.pieces if piece.color != color]

        if endgame and own_piece_value != other_piece_value:
            # Im Endspiel möchte der Spieler mit mehr Material seinen König
            # soweit an den gegnersichen König bewegen wie möglich
            endgame_weight = 8 - exp(0.065 * len(board.pieces))

            own_king = board.kings[color]
            other_king = board.kings[1 - color]

            other_king_dst_to_centre = max(max(3 - other_king.pos[0], other_king.pos[0] - 4), max(3 - other_king.pos[1], other_king.pos[1] - 4))
            king_distance = max(abs(own_king.pos[0] - other_king.pos[0]), abs(own_king.pos[1] - other_king.pos[1]))

            king_value = other_king_dst_to_centre + 7 - king_distance

            if own_piece_value > other_piece_value:
                value += int(round(king_value * endgame_weight))
            elif own_piece_value < other_piece_value:
                value -= int(round(king_value * endgame_weight))

        # Addiere alle PST-Bewertungen der eigenen Figuren
        for piece in own_pieces:
            value += self.get_pst_value(piece, endgame)
        
        # Subtrahiere alle PST-Bewertungen der gegnerischen Figuren
        for piece in other_pieces:
            value -= self.get_pst_value(piece, endgame)

        return value

    # sortiert die Züge
    # Quelle : https://www.chessprogramming.org/Move_Ordering
    def order_moves(self, moves : list, board : Board, depth : int, quiescence_order : bool = False) -> list:
        moves_copy = moves.copy()

        # Bestimme, wenn möglich, den Hash-Zug
        hash_move = []

        if board.hash in self.transposition_table:
            tt_entry = self.transposition_table[board.hash]
            if tt_entry.entry_type == Transposition_Table_Entry_Type.EXACT or tt_entry.entry_type == Transposition_Table_Entry_Type.LOWER_BOUND:
                if tt_entry.move in moves_copy:
                    hash_move.append(tt_entry.move)
                    moves_copy.remove(tt_entry.move)

        # bestimme mit SEE die Schlagabfolgen, die Material gewinnen/neutral sind und die Material verlieren
        # nicht 100% sicher, weil ein Spieler auch eine Figur schlagen kann, die sich woanders befindet
        # Filter außerdem Doppelzüge von Bauern heraus
        winning_captures = []
        losing_captures = []
        killer_moves = []
        pawn_double_moves = []

        for move in moves_copy.copy():
            if move.captured != None:
                board.do_move(move, False)
                material_diff = self.piece_value[type(move.captured)] - self.piece_value[type(board.board[move.to[0]][move.to[1]])]
                # Wenn man eine Figur mit weniger Material schlägt, müssen wir kein SEE anwenden
                if material_diff > 0:
                    winning_captures.append(move)
                    moves_copy.remove(move)
                else:
                    val = self.piece_value[type(move.captured)] - self.see(board, move.to)
                    if val >= 0:
                        winning_captures.append(move)
                        moves_copy.remove(move)
                    else:
                        losing_captures.append(move)
                        moves_copy.remove(move)
                        
                board.undo_move(False)
            elif not quiescence_order:
                if board.hash in self.transposition_table:
                    for move in moves_copy:
                        if move in self.transposition_table[board.hash].killer_moves:
                            killer_moves.append(move)
                            moves_copy.remove(move)
                elif isinstance(move, Pawn_Double_Move):
                    # filtere Doppelzüge von Bauern
                    pawn_double_moves.append(move)
                    moves_copy.remove(move)
        
        # In der Quiescencesuche brauchen wir keine Schlagzüge simulieren, wenn die SEE schon < 0 ist
        if quiescence_order:
            losing_captures.clear()
        
        return hash_move + winning_captures + killer_moves + pawn_double_moves + moves_copy + losing_captures


    # Quiescence-Suche
    # Traversiert den Spielbaum nur noch mit Schlagzügen, Züge die den Gegner in Schach setzen und Bauernaufwertungen
    def quiescence(self, board : Board, depth : int, alpha : int, beta : int) -> int:
        # überprüfe, ob das Spielfeld schonmal evaluiert wurde
        if board.hash in self.transposition_table:
            tt_entry = self.transposition_table[board.hash]
            if tt_entry.entry_type == Transposition_Table_Entry_Type.EXACT or tt_entry.entry_type == Transposition_Table_Entry_Type.QUIESCENT:
                return tt_entry.value
            elif tt_entry.entry_type == Transposition_Table_Entry_Type.LOWER_BOUND:
                if tt_entry.value >= beta:
                    beta = tt_entry.value
            elif tt_entry.entry_type == Transposition_Table_Entry_Type.UPPER_BOUND:
                if tt_entry.value <= alpha:
                    alpha = tt_entry.value
            
            # Wenn sich Alpha und Beta überschneiden, dann ist die Bewertung des aktuellen Knotens nicht mehr relevant
            if alpha >= beta:
                return tt_entry.value

        own_king = board.kings[board.turn]
        other_king = board.kings[1 - board.turn]
        own_pieces = [x for x in board.pieces if x.color == board.turn]
        other_pieces = [x for x in board.pieces if x.color != board.turn]

        check = board.is_in_check(board.turn)
        moves = []

        if not check:
            # Wenn wir uns nicht im Schach befinden,
            # filter nach Zügen, die
            # 1. Eine Figur schlagen
            # 2. Den Gegner in Schach setzen (mit begrenzter Tiefe)
            # 3. Einen Bauern aufwerten
            val = self.evaluate(board, board.turn)

            if board.is_draw_by_repetition():
                val = max(0, val)

            if val >= beta:
                return beta
            
            if val > alpha:
                alpha = val

            legal_moves = board.get_legal_moves(board.turn)

            # Wenn wir nicht im Schach stehen und keine legalen Züge haben, sind wir Patt
            if len(legal_moves) == 0:
                if board.hash not in self.transposition_table:
                    tt_entry = Transposition_Table_Entry(0, -1, Transposition_Table_Entry_Type.QUIESCENT)
                    self.transposition_table[board.hash] = tt_entry
                return 0

            for move in legal_moves:
                if move.captured != None:
                    moves.append(move)
                elif isinstance(move, Promotion_Move):
                    moves.append(move)
                elif depth > 0:
                    board.do_move(move, False)

                    if board.is_in_check(board.turn):
                        moves.append(move)

                    board.undo_move(False)
        else:
            # Wenn wir im Schach sind, simulieren wir alle Züge, die uns aus dem Schach befördern(wenn möglich)
            # Wenn es keine legalen Züge gibt, sind wir Schachmatt
            moves = board.get_legal_moves(board.turn)
            if len(moves) == 0:
                score = -self.MATE_SCORE + self.curr_depth
                if board.hash not in self.transposition_table:
                    tt_entry = Transposition_Table_Entry(score, -1, Transposition_Table_Entry_Type.QUIESCENT)
                    self.transposition_table[board.hash] = tt_entry
                return score

        tt_type = None

        # NegaMax ähnliches Suchverfahren
        for move in self.order_moves(moves, board, 0, True):
            board.do_move(move)
            val = -self.quiescence(board, depth - 1, -beta, -alpha)
            board.undo_move()
            if val >= beta:
                return beta
            
            if val > alpha:
                alpha = val
                tt_type = Transposition_Table_Entry_Type.QUIESCENT
            
        # Speichere das Ergebnis der Evaluation in der Transpositionstabelle
        if tt_type != None and not board.hash in self.transposition_table:
            tt_entry = Transposition_Table_Entry(alpha, -1, tt_type)
            self.transposition_table[board.hash] = tt_entry
            
        return alpha

    # NegaScout Variante der Alpha-Beta-Suche
    def alpha_beta(self, board : Board, depth : int, alpha : int, beta : int) -> int:    
        # überprüfe, ob die Spielposition in der Transpositionstabelle enthalten ist
        if board.hash in self.transposition_table:
            tt_entry = self.transposition_table[board.hash]
            # der Eintrag in der Transpositionstabelle kann nur verwendet werden,
            # wenn die Suchtiefe nach dem Eintrag größer oder gleich der Suchtiefe ist,
            # mit der dieser Knoten noch bewertet werden soll
            if tt_entry.depth >= depth:
                # Wenn der Eintrag in der Transpositionstabelle ein exakter Eintrag ist,
                # dann wurden alle Kinder bewertet und wir wissen, dass das die tatsächliche Bewertung ist
                if tt_entry.entry_type == Transposition_Table_Entry_Type.EXACT:
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

        # An Blattknoten wird die Quiescence-Suche gestartet
        if depth == 0:
            return self.quiescence(board, self.MAX_QUIESCENCE_CHECK_DEPTH, alpha, beta)

        tt_type = Transposition_Table_Entry_Type.UPPER_BOUND

        b = beta
        i = 0

        moves = board.get_legal_moves(board.turn)

        if len(moves) == 0:
            score = 0
            own_king = board.kings[board.turn]
            other_pieces = [x for x in board.pieces if x.color != board.turn]
            # sind wir Schachmatt oder Patt?
            if board.is_in_check(board.turn):
                score = -self.MATE_SCORE + (self.curr_depth - depth)
            
            tt_entry = Transposition_Table_Entry(score, depth, Transposition_Table_Entry_Type.EXACT)
            self.transposition_table[board.hash] = tt_entry
            return score
        
        best_move = None

        # simuliere alle möglichen Züge
        for move in self.order_moves(moves, board, depth):
            i += 1
            board.do_move(move)
            # Suche mit Nullfenster
            val = -self.alpha_beta(board, depth - 1, -b, -alpha)

            # Wenn die Nullfenstersuche fehlgeschlagen ist, müssen wir mit regulärem Fenster neu suchen
            if val > alpha and val < beta and i > 1 and depth < self.curr_depth:
                val = -self.alpha_beta(board, depth - 1, -beta, -val)

            if board.is_draw_by_repetition():
                val = max(0, val)

            board.undo_move()

            # Beta-Schnitt
            if val >= beta:
                tt_entry = Transposition_Table_Entry(beta, depth, Transposition_Table_Entry_Type.LOWER_BOUND)
                tt_entry.move = move
                # Speichere Killer-Move ab
                if move.captured == None:
                    prev_killer_moves = [None, None]
                    if board.hash in self.transposition_table:
                        prev_killer_moves = self.transposition_table[board.hash].killer_moves
                    
                    prev_killer_moves[0] = prev_killer_moves[1]
                    prev_killer_moves[1] = move
                    tt_entry.killer_moves = prev_killer_moves
                self.transposition_table[board.hash] = tt_entry
                return beta

            # Wir konnten mit diesem Zug das Alpha verbessern
            if val > alpha:
                tt_type = Transposition_Table_Entry_Type.EXACT
                best_move = move
                alpha = val

                # Wenn wir an der Wurzel sind und Matt gefunden haben(-> garantiert)
                # können wir die Suche abbrechen
                if self.curr_depth == depth and alpha >= self.MATE_SCORE - depth:
                    tt_entry = Transposition_Table_Entry(alpha, depth, Transposition_Table_Entry_Type.EXACT)
                    tt_entry.move = move
                    self.transposition_table[board.hash] = tt_entry
                    self.mate_found = True
                    return alpha
            
            # Wenn die Zeit abgelaufen ist und wir ein Ergebnis haben(aus vorheriger Tiefe), dann brechen wir ab
            if not self.searching and self.best_move != None:
                self.last_search_interrupted = True
                return alpha
            
            b = alpha + 1
            
        # Eintrag in die Transpositionstabelle hinzufügen
        tt_entry = Transposition_Table_Entry(alpha, depth, tt_type)
        if tt_type == Transposition_Table_Entry_Type.EXACT:
            tt_entry.move = best_move
        self.transposition_table[board.hash] = tt_entry

        return alpha
    
    # bricht die Iterative Tiefensuche ab
    def stop_search(self):
        self.searching = False
    
    # sucht mittels iterativer Tiefensuche nach dem besten Zug auf dem gegeben Schachbrett
    # sucht nach einem Zug für den Spieler, der nach board am Zug ist
    def get_move(self, board : Board, search_time : float = 2) -> Move:
        self.curr_depth = 0
        self.searching = True
        self.last_search_interrupted = False
        self.mate_found = False
        self.transposition_table.clear()

        timer = Timer(search_time, self.stop_search)
        timer.start()

        # iterative Tiefensuche
        while self.searching:
            self.curr_depth += 1

            val = self.alpha_beta(board, self.curr_depth, -self.INFINITY, self.INFINITY)

            # Statusmeldung ausgeben und besten Zug abspeichern
            if not self.last_search_interrupted:
                self.best_move = self.transposition_table[board.hash].move

            # Wenn wir Matt gefunden haben, können wir abbrechen
            if self.mate_found:
                timer.cancel()
                break

        return self.best_move