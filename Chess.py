import Board
import ChessComputer

def pick_move(board : Board) -> Board.Move:
    while True:
        user_in = input()
        for move in board.get_legitimate_moves(board.turn):
            if str(move) == user_in.strip():
                return move

WHITE = 0
BLACK = 1

starting_board = Board.Board()

cp = ChessComputer.ChessComputer()

while True:
    cp_move = cp.get_move(starting_board)
    print(f"Move played: {cp_move}")
    starting_board.do_move(cp_move)
    p_move = pick_move(starting_board)
    starting_board.do_move(p_move)