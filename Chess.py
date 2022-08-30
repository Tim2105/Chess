import Board
import ChessComputer

def pick_move(board : Board) -> Board.Move:
    while True:
        user_in = input()
        for move in board.get_legal_moves(board.turn):
            if str(move) == user_in.strip():
                return move
        print("Invalid move")

WHITE = 0
BLACK = 1

starting_board = Board.Board("8/P7/8/8/8/6pn/5pkb/K4nb1 w - - 0 1")

cp = ChessComputer.ChessComputer()

while True:
    cp_move = cp.get_move(starting_board)
    print(f"Move played: {cp_move}")
    starting_board.do_move(cp_move)
    p_move = pick_move(starting_board)
    starting_board.do_move(p_move)