from __future__ import annotations
from chess_attributes import ChessAttributes
from piece import Bishop, King, Knight, Pawn, Queen, Rook
from square import Square

class Board(ChessAttributes):
    def __init__(self, perspective: str, white_player: 'Player', black_player: 'Player') -> None:
        super().__init__()
        self.perspective = perspective
        self.white_player = white_player
        self.black_player = black_player
        self._board = [[Square((i, j), perspective) for j in range(self.BOARD_SIZE)] for i in range(self.BOARD_SIZE)]
        self.set_square_colors()
        self.instantiate_chess_pieces()

    def __repr__(self):
        board_representation = []
        for row in self._board:
            row_representation = [repr(square) for square in row]
            board_representation.append(' '.join(row_representation))
        return '\n'.join(board_representation)

    @property
    def board(self):
        return self._board

    def set_square_colors(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 == 0:
                    self._board[row][col].color = "white"
                else:
                    self._board[row][col].color = "black"

    def instantiate_chess_pieces(self):
        white_starting_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        if self.perspective == "white":
            # Create white pieces
            first_rank = self.BOARD_SIZE - 1
            second_rank = self.BOARD_SIZE - 2
            for i in range(self.BOARD_SIZE):
                NewPiece = white_starting_order[i]
                if NewPiece == King:
                    self._board[first_rank][i].piece = NewPiece("white", self.perspective, (first_rank, i), self.black_player.pieces)
                else:
                    self._board[first_rank][i].piece = NewPiece("white", self.perspective, (first_rank, i))
                self.white_player.pieces.append(self._board[first_rank][i].piece)
                self._board[second_rank][i].piece = Pawn("white", self.perspective, (second_rank, i))
                self.white_player.pieces.append(self._board[second_rank][i].piece)
            # Create black pieces
            first_rank = self.BOARD_SIZE - 8
            second_rank = self.BOARD_SIZE - 7
            for i in range(self.BOARD_SIZE):
                NewPiece = white_starting_order[i]
                if NewPiece == King:
                    self._board[first_rank][i].piece = NewPiece("black", self.perspective, (first_rank, i), self.white_player.pieces)
                else:
                    self._board[first_rank][i].piece = NewPiece("black", self.perspective, (first_rank, i))
                self.black_player.pieces.append(self._board[first_rank][i].piece)
                self._board[second_rank][i].piece = Pawn("black", self.perspective, (second_rank, i))
                self.black_player.pieces.append(self._board[second_rank][i].piece)
        else:
            black_starting_order = white_starting_order[::-1]
            # Create black pieces
            first_rank = self.BOARD_SIZE - 1
            second_rank = self.BOARD_SIZE - 2
            for i in range(self.BOARD_SIZE):
                NewPiece = black_starting_order[i]
                if NewPiece == King:
                    self._board[first_rank][i].piece = NewPiece("black", self.perspective, (first_rank, i), self.white_player.pieces)
                else:
                    self._board[first_rank][i].piece = NewPiece("black", self.perspective, (first_rank, i))
                self.black_player.pieces.append(self._board[first_rank][i].piece)
                self._board[second_rank][i].piece = Pawn("black", self.perspective, (second_rank, i))
                self.black_player.pieces.append(self._board[second_rank][i].piece)
            # Create white pieces
            first_rank = self.BOARD_SIZE - 8
            second_rank = self.BOARD_SIZE - 7
            for i in range(self.BOARD_SIZE):
                NewPiece = black_starting_order[i]
                if NewPiece == King:
                    self._board[first_rank][i].piece = NewPiece("white", self.perspective, (first_rank, i), self.black_player.pieces)
                else:
                    self._board[first_rank][i].piece = NewPiece("white", self.perspective, (first_rank, i))
                self.white_player.pieces.append(self._board[first_rank][i].piece)
                self._board[second_rank][i].piece = Pawn("white", self.perspective, (second_rank, i))
                self.white_player.pieces.append(self._board[second_rank][i].piece)