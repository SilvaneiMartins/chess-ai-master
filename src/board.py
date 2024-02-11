import copy

from const import *
from square import Square
from piece import *
from move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # atualização de movimentação da placa do console
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # atualização de movimentação da placa do objeto
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # mover
        piece.moved = True

        # limpa valores de movimento
        piece.clear_moves()

        # seta ultima movimentação
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        
        return False

    def calc_moves(self, piece, row, col):
        '''	
            Calcule todos os movimentos possíveis (válidos) de uma peça
            específica em uma posição específica.
        '''

        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # movimento na vertical
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # crie quadrados de movimento inicial e final
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)

                        # crie novo um movimento
                        move = Move(initial, final)

                        # adicione o movimento à lista de movimentos
                        piece.add_move(move)
                    # bloqueio de movimento
                    else:
                        break
                # fora de alcance
                else:
                    break

            # movimento diagonal
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # crie quadrados de movimento inicial e final
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # crie novo um movimento
                        move = Move(initial, final)

                        # adicione o movimento à lista de movimentos
                        piece.add_move(move)

        def kinght_moves():
            # 8 possíveis movimentos do cavalo
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # crie quadrados do novo movimento
                        initial = Square(row, col)
                        final = Square(possible_move_row,
                                       possible_move_col)  # piece=piece

                        # cria um movimento movimento
                        move = Move(initial, final)

                        # adicione o movimento à lista de movimentos
                        piece.add_move(move)

        def straigntline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # cria um possivel movimento
                        move = Move(initial, final)

                        # vazio - continua o movimento
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # adiciona o movimento à lista de movimentos
                            piece.add_move(move)

                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # adiciona o movimento à lista de movimentos
                            piece.add_move(move)
                            break

                        # bloqueio de movimento - para o loop
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # fora de alcance
                    else:
                        break

                    # incrementa a posição
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0),  # up
                (row-1, col+1),  # up-right
                (row+0, col+1),  # right
                (row+1, col+1),  # down-right
                (row+1, col+0),  # down
                (row+1, col-1),  # down-left
                (row+0, col-1),  # left
                (row-1, col-1),  # up-left
            ]

            # movimentos normais
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # crie quadrados do novo movimento
                        initial = Square(row, col)
                        final = Square(possible_move_row,
                                       possible_move_col)  # piece=piece

                        # criar novo movimento
                        move = Move(initial, final)

                        # verificar verificações potenciais
                        if bool:
                            if not self.in_check(piece, move):
                                # anexar novo movimento
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # anexar novo movimento
                            piece.add_move(move)

            # movimentos de roque
            if not piece.moved:
                # roque da rainha
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # o roque não é possível porque há peças no meio?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # adiciona torre esquerda ao rei
                                piece.left_rook = left_rook

                                # movimento de torre
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # movimento do rei
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # verificar verificações potenciais
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # anexar novo movimento à torre
                                        left_rook.add_move(moveR)
                                        # anexar novo movimento ao rei
                                        piece.add_move(moveK)
                                else:
                                    # anexar novo movimento à torre
                                    left_rook.add_move(moveR)
                                    # anexar novo movimento rei
                                    piece.add_move(moveK)

                # roque do rei
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # o roque não é possível porque há peças no meio?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # adiciona a torre direita ao rei
                                piece.right_rook = right_rook

                                # movimento de torre
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # movimento do rei
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # verificar verificações potenciais
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # anexar novo movimento à torre
                                        right_rook.add_move(moveR)
                                        # anexar novo movimento ao rei
                                        piece.add_move(moveK)
                                else:
                                    # anexar novo movimento à torre
                                    right_rook.add_move(moveR)
                                    # anexar novo movimento rei
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            kinght_moves()

        elif isinstance(piece, Bishop):
            straigntline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
            ])

        elif isinstance(piece, Rook):
            straigntline_moves([
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1),  # left
            ])

        elif isinstance(piece, Queen):
            straigntline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1),  # left
            ])

        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
