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
    def __init__(self, from_pos : tuple, to_pos : tuple, promotion_piece, promoted_piece):
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