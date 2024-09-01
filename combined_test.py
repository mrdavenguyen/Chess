from dataclasses import dataclass
from typing import Optional
from typing import Tuple

class Chess:
    def __init__(self):
        self.player = None
        self.is_cpu_opponent = False
        self.cpu_difficulty = None
        self._board = Board()
        self.perspective = self.player
        self.white_player = None
        self.black_player = None
        self.BOARD_SIZE = 8
        self.get_game_settings()
        self.instantiate_players()

    @property
    def board(self):
        return self._board
    
    def get_game_settings(self) -> None:
        while True:
            color: str = input("Do you want to be White or Black?")
            if color.upper() == "WHITE":
                self.player = "white"
                break
            elif color.upper() == "BLACK":
                self.player = "black"
                break
        while True:
            opponent: str = input("Play against a computer? Y/N")
            if opponent.upper() == "Y":
                self.is_cpu_opponent = True
                break
            elif opponent.upper() == "N":
                self.is_cpu_opponent = False
                break
        if self.is_cpu_opponent:
            while True:
                difficulty: str = input("Select computer difficulty (Easy, Medium, Hard):")
                if difficulty.upper() == "EASY":
                    self.cpu_difficulty = "easy"
                    break
                elif difficulty.upper() == "MEDIUM":
                    self.cpu_difficulty = "medium"
                    break
                elif difficulty.upper() == "HARD":
                    self.cpu_difficulty = "hard"
                    break

    def instantiate_players(self) -> None:
        if self.player == "white":
            self.white_player = Player("white", False)
            self.black_player = Player("black", self.is_cpu_opponent, self.cpu_difficulty)
        else:
            self.black_player = Player("black", False)
            self.white_player = Player("white", self.is_cpu_opponent, self.cpu_difficulty)
    
    def get_pos_from_coords(self, coordinates: Tuple[int, int]) -> str:
        square_y, square_x = coordinates
        return self.get_column_pos(square_x) + self.get_row_pos(square_y)
        
    def get_coords_from_pos(self, position: str) -> Tuple[int, int]:
        square_x, square_y = position
        return (self.get_row_coord(square_y), self.get_col_coord(square_x))
        
    def get_row_pos(self, square_y: int) -> str:
        if self.perspective == "white":
            return str(self.BOARD_SIZE - square_y)
        else:
            return str(square_y + 1)
    
    def get_column_pos(self, square_x: int) -> str:
        if self.perspective == "white":
            return chr(ord("a") + square_x)
        else:
            return chr(ord("a") + self.BOARD_SIZE - (square_x + 1))
    
    def get_row_coord(self, square_y: str) -> int:
        if self.perspective == "white":
            return self.BOARD_SIZE - int(square_y)
        else:
            return int(square_y) - 1

    def get_col_coord(self, square_x: str) -> int:
        if self.perspective == "white":
            return ord(square_x) - ord("a")
        else:
            return self.BOARD_SIZE - (ord(square_x) - ord("a")) - 1

class Board(Chess):
    def __init__(self):
        self._board = [[Square((i, j)) for j in range(self.BOARD_SIZE)] for i in range(self.BOARD_SIZE)]
        self.set_square_colors()
        self.instantiate_chess_pieces()

    def __repr__(self):
        return self.board

    @property
    def board(self):
        return self._board

    def set_square_colors(self):
        for row in range(super().BOARD_SIZE):
            for col in range(super().BOARD_SIZE):
                if (row + col) % 2 == 0:
                    self._board[row][col].color = "white"
                else:
                    self._board[row][col].color = "black"

    def instantiate_chess_pieces(self):
        white_starting_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        if super().perspective == "white":
            # Create white pieces
            first_rank = super().BOARD_SIZE - 1
            second_rank = super().BOARD_SIZE - 2
            for i in range(super().BOARD_SIZE):
                NewPiece = white_starting_order[i]
                self._board[first_rank][i].piece = NewPiece("white", (first_rank, i))
                self.white_player.pieces.append(self._board[first_rank][i].piece)
                self._board[second_rank][i].piece = Pawn("white", (second_rank, i))
                self.white_player.pieces.append(self._board[second_rank][i].piece)
            # Create black pieces
            first_rank = super().BOARD_SIZE - 8
            second_rank = super().BOARD_SIZE - 7
            for i in range(super().BOARD_SIZE):
                NewPiece = white_starting_order[i]
                self._board[first_rank][i].piece = NewPiece("black", (first_rank, i))
                self.black_player.pieces.append(self._board[first_rank][i].piece)
                self._board[second_rank][i].piece = Pawn("black", (second_rank, i))
                self.black_player.pieces.append(self._board[second_rank][i].piece)
        else:
            black_starting_order = white_starting_order[::-1]
            # Create black pieces
            first_rank = super().BOARD_SIZE - 1
            second_rank = super().BOARD_SIZE - 2
            for i in range(super().BOARD_SIZE):
                NewPiece = black_starting_order[i]
                self._board[first_rank][i].piece = NewPiece("black", (first_rank, i))
                self.black_player.pieces.append(self._board[first_rank][i].piece)
                self._board[second_rank][i].piece = Pawn("black", (second_rank, i))
                self.black_player.pieces.append(self._board[second_rank][i].piece)
            # Create white pieces
            first_rank = super().BOARD_SIZE - 8
            second_rank = super().BOARD_SIZE - 7
            for i in range(super().BOARD_SIZE):
                NewPiece = black_starting_order[i]
                self._board[first_rank][i].piece = NewPiece("white", (first_rank, i))
                self.white_player.pieces.append(self._board[first_rank][i].piece)
                self._board[second_rank][i].piece = Pawn("white", (second_rank, i))
                self.white_player.pieces.append(self._board[second_rank][i].piece)

class Player(Chess):
    def __init__(self, color: str, is_cpu: bool, difficulty: Optional[str] = None):
        self.color: str = None
        self.is_cpu: str = False
        self.difficulty: str = None # None, easy, medium or hard
        self.pieces = []
        self.is_in_check = False

class Square(Chess):
    def __init__(self, coordinates: Tuple[int, int]):
        self.coordinates: Tuple[int, int] = coordinates
        self.position: str = super().get_pos_from_coords(coordinates)
        self.color: str = None # Color of the square ("black" or "white")
        self.piece: str = None

    def __repr__(self):
        return f"{self.piece} piece of {self.piece.color} color on {self.position}"
    
    def add_piece(self):
        pass

class Piece(Chess):
    def __init__(self, color, coordinates):
        self.color = color
        self.coordinates = coordinates
        self.position = super().get_pos_from_coords(coordinates)

    def move_piece(self, board, position):
        row_src, col_src = self.coordinates
        dest_coords = super().get_coords_from_pos(position)
        row_dest, col_dest = dest_coords
        if self.is_valid_move(board, row_src, col_src, row_dest, col_dest):
            self.perform_capture_if_capturable(board, row_src, col_src, row_dest, col_dest)
            source_square = self.get_square(board, row_src, col_src)
            dest_square = self.get_square(board, row_dest, col_dest)
            dest_square.piece = source_square.piece
            source_square.piece = None
            self.coordinates = dest_coords
            self.position = super().get_pos_from_coords(dest_coords)
        else:
            pass # return an error

    def test_move_piece(self, board, row_dest, col_dest):
        row_src, col_src = self.coordinates
        source_square = self.get_square(board, row_src, col_src)
        dest_square = self.get_square(board, row_dest, col_dest)
        captured_piece = dest_square.piece
        dest_square.piece = source_square.piece
        source_square.piece = None
        self.coordinates = (row_dest, col_dest)
        self.position = super().get_pos_from_coords(self.coordinates)
        return captured_piece

    def reset_move(self, board, row_dest, col_dest, captured_piece):
        row_src, col_src = self.coordinates
        source_square = self.get_square(board, row_src, col_src)
        dest_square = self.get_square(board, row_dest, col_dest)
        dest_square.piece = source_square.piece
        source_square.piece = captured_piece
        self.coordinates = (row_dest, col_dest)
        self.position = super().get_pos_from_coords(self.coordinates)

    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        return self.is_within_bounds(row_dest, col_dest) and (not self.is_occupied_square(board, row_dest, col_dest) or self.is_capturable_piece(board, row_src, col_src, row_dest, col_dest))

    def is_capturable_piece(self, board, row_src, col_src, row_dest, col_dest):
        src_color = self.get_piece_color(board, row_src, col_src)
        dest_color = self.get_piece_color(board, row_dest, col_dest)
        return self.is_occupied_square(board, row_dest, col_dest) and dest_color is not src_color
    
    def is_occupied_square(self, board, row, col):
        return board[row][col].piece

    def get_square(self, board, row, col) -> Square:
        return board[row][col]
    
    def get_piece_color(self, board, row, col):
        target_square = self.get_square(board, row, col)
        return target_square.piece.color
    
    def is_within_bounds(self, row_dest, col_dest):
        return 0 <= row_dest < super().BOARD_SIZE and 0 <= col_dest < super().BOARD_SIZE

    
class King(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "king"
        self.character = "♔" if self.color == "white" else "♚"
        self.has_moved = False

    def __repr__(self):
        return "king"
    
    def move_piece(self, board, position):
        row_src, col_src = self.coordinates
        dest_coords = super().get_coords_from_pos(position)
        row_dest, col_dest = dest_coords
        if super().is_within_bounds(row_dest, col_dest):
            if self.is_valid_single_space_move(board, row_src, col_src, row_dest, col_dest):
                self.perform_single_space_move(board, row_src, col_src, row_dest, col_dest)
            elif self.is_valid_castling_move(board, row_src, col_src, row_dest, col_dest):
                self.perform_castling_move(board, row_src, col_src, row_dest, col_dest)
            else:
                pass # Return an error

    def perform_single_space_move(self, board, row_src, col_src, row_dest, col_dest):
        source_square = self.get_square(board, row_src, col_src)
        dest_square = self.get_square(board, row_dest, col_dest)
        dest_square.piece = source_square.piece
        source_square.piece = None
        self.coordinates = (row_dest, col_dest)
        self.position = super().get_pos_from_coords(self.coordinates)

    def perform_castling_move(self, board, row_src, col_src, row_dest, col_dest):
        castling_direction = self.get_castling_direction(col_src, col_dest)
        castling_distance = 2

        # Move king
        king_source_square = self.get_square(board, row_src, col_src)
        king_col_dest = col_src + (castling_distance * castling_direction)
        king_dest_square = self.get_square(board, row_dest, king_col_dest)
        king_dest_square.piece = king_source_square.piece
        king_source_square.piece = None
        self.coordinates = (row_dest, king_col_dest)
        self.position = super().get_pos_from_coords(self.coordinates)

        # Move rook
        rook_source_square = self.get_square(board, row_src, col_dest)
        rook_col_dest = king_col_dest - castling_direction
        rook_dest_square = self.get_square(board, row_dest, rook_col_dest)
        rook_dest_square.piece = rook_source_square.piece
        rook_source_square.piece = None
        rook_coords = (row_dest, rook_col_dest)
        rook_dest_square.piece.coordinates = rook_coords
        rook_dest_square.piece.position = super().get_pos_from_coords(rook_coords)

    def set_has_moved(self):
        if not self.has_moved:
            self.has_moved = True
    
    def is_valid_single_space_move(self, board, row_src, col_src, row_dest, col_dest):
        if abs(row_dest - row_src) <= 1 and abs(col_dest - col_src) <= 1 and not (abs(row_dest - row_src) == 0 and abs(col_dest - col_src) == 0):
            if self.is_safe_square(board, row_src, col_src, row_dest, col_dest):
                return True
        return False
            
    def is_valid_castling_move(self, board, row_src, col_src, row_dest, col_dest):
        if self.has_not_moved_rook() and self.is_friendly_rook(board, row_src, col_src, row_dest, col_dest):
            if self.has_not_moved_king and not self.is_in_check(board, row_src, col_src):
                if self.is_clear_path(board, row_src, col_src, col_dest) and self.are_safe_intermediate_squares(board, row_src, col_src, row_dest, col_dest):
                    return True
        return False
    
    def has_not_moved_rook(self, board, row, col):
        return not board[row][col].piece.has_moved
    
    def has_not_moved_king(self):
        return not self.has_moved
                
    def is_clear_path(self, board, row_src, col_src, col_dest):
        dist_x = abs(col_dest - col_src)
        castling_direction = self.get_castling_direction(col_src, col_dest)
        for i in range(1, dist_x):
            if board[row_src][col_src + (i * castling_direction)].piece is not None:
                return False
        return True

    def is_friendly_rook(self, board, row_src, col_src, row_dest, col_dest):
        return board[row_dest][col_dest].piece.type == "rook" and not super().is_capturable_piece(board, row_src, col_src, row_dest, col_dest)

    def are_safe_intermediate_squares(self, board, row_src, col_src, row_dest, col_dest):
        castling_direction = self.get_castling_direction(col_src, col_dest)
        castling_distance = 2
        for i in range(1, castling_distance + 1):
            col_step = col_dest + (i * castling_direction)
            if not self.is_safe_square(board, row_src, col_src, row_dest, col_step):
                return False
        return True
    
    def get_castling_direction(self, col_src, col_dest):
        dist_x = abs(col_dest - col_src)
        return (col_dest - col_src) // dist_x
    
    def is_safe_square(self, board, row_src, col_src, row_dest, col_dest):
        captured_piece = super().test_move_piece(board, row_dest, col_dest)
        if self.is_in_check(board, row_dest, col_dest):
            super().reset_move(board, row_src, col_src, captured_piece)
            return False
        super().reset_move(board, row_src, col_src, captured_piece)
        return True
    
    def is_in_check(self):
        pass

class Queen(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "queen"
        self.character = "♕" if self.color == "white" else "♛"

    def __repr__(self):
        return "queen"
    
    def move_piece(self, board, position):
        super().move_piece(board, position)
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_valid_move(board, row_src, col_src, row_dest, col_dest):
            if self.is_linear_move(row_src, col_src, row_dest, col_dest) or self.is_diagonal_move(row_src, col_src, row_dest, col_dest):
                if self.is_clear_path(board, row_src, col_src, row_dest, col_dest):
                    return True
        return False

    def is_linear_move(self, row_src, col_src, row_dest, col_dest):
        return (row_dest == row_src) ^ (col_dest == col_src)
    
    def is_diagonal_move(self, row_src, col_src, row_dest, col_dest):
        return abs(row_dest - row_src) == abs(col_dest - col_src) and abs(row_dest - row_src) != 0
    
    def is_clear_path(self, board, row_src, col_src, row_dest, col_dest):
        dist_y = abs(row_dest - row_src)
        dist_x = abs(col_dest - col_src)
        if dist_y > dist_x:
            return self.is_clear_vertical(board, row_src, col_src, row_dest)
        elif dist_y < dist_x:
            return self.is_clear_horizontal(board, row_src, col_src, col_dest)
        else:
            return self.is_clear_diagonal(board, row_src, col_src, row_dest, col_dest)

    def is_clear_vertical(self, board, row_src, col_src, row_dest):
        dist_y = abs(row_dest - row_src)
        row_step = (row_dest - row_src) // dist_y
        for i in range(1, dist_y):
            if board[row_src + (i * row_step)][col_src].piece is not None:
                return False
        return True
    
    def is_clear_horizontal(self, board, row_src, col_src, col_dest):
        dist_x = abs(col_dest - col_src)
        col_step = (col_dest - col_src) // dist_x
        for i in range(1, dist_x):
            if board[row_src][col_src + (i * col_step)].piece is not None:
                return False
        return True
    
    def is_clear_diagonal(self, board, row_src, col_src, row_dest, col_dest):
        distance = abs(row_dest - row_src)
        row_step = (row_dest - row_src) // distance
        col_step = (col_dest - col_src) // distance
        for i in range(1, distance):
            if board[row_src + (i * row_step)][col_src + (i * col_step)].piece is not None:
                return False
        return True
    
class Bishop(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "bishop"
        self.character = "♗" if self.color == "white" else "♝"

    def __repr__(self):
        return "bishop"
    
    def move_piece(self, board, position):
        super().move_piece(board, position)
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_valid_move(board, row_src, col_src, row_dest, col_dest) and self.is_diagonal_move(self, row_src, col_src, row_dest, col_dest):
            if self.is_clear_path(board, row_src, col_src, row_dest, col_dest):
                return True
        return False
    
    def is_diagonal_move(self, row_src, col_src, row_dest, col_dest):
        return abs(row_dest - row_src) == abs(col_dest - col_src) and abs(row_dest - row_src) != 0
    
    def is_clear_path(self, board, row_src, col_src, row_dest, col_dest):
        distance = abs(row_dest - row_src)
        row_step = (row_dest - row_src) // distance
        col_step = (col_dest - col_src) // distance
        for i in range(1, distance):
            if board[row_src + (i * row_step)][col_src + (i * col_step)].piece is not None:
                return False
        return True
    
class Rook(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "rook"
        self.character = "♖" if self.color == "white" else "♜"
        self.has_moved = False

    def __repr__(self):
        return "rook"

    def move_piece(self, board, position):
        super().move_piece(board, position)
        if not self.has_moved:
            self.has_moved = True
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_valid_move(board, row_src, col_src, row_dest, col_dest) and self.is_linear_move(row_src, col_src, row_dest, col_dest):
            if self.is_clear_path(board, row_src, col_src, row_dest, col_dest):
                return True
        return False
    
    def is_linear_move(self, row_src, col_src, row_dest, col_dest):
        return (row_dest == row_src) ^ (col_dest == col_src)

    def is_clear_path(self, board, row_src, col_src, row_dest, col_dest):
        dist_y = abs(row_dest - row_src)
        dist_x = abs(col_dest - col_src)
        if dist_y > dist_x:
            return self.is_clear_vertical(board, row_src, col_src, row_dest)
        elif dist_y < dist_x:
            return self.is_clear_horizontal(board, row_src, col_src, col_dest)

    def is_clear_vertical(self, board, row_src, col_src, row_dest):
        dist_y = abs(row_dest - row_src)
        row_step = (row_dest - row_src) // dist_y
        for i in range(1, dist_y):
            if board[row_src + (i * row_step)][col_src].piece is not None:
                return False
        return True
    
    def is_clear_horizontal(self, board, row_src, col_src, col_dest):
        dist_x = abs(col_dest - col_src)
        col_step = (col_dest - col_src) // dist_x
        for i in range(1, dist_x):
            if board[row_src][col_src + (i * col_step)].piece is not None:
                return False
        return True
    
class Knight(Piece):
    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "knight"
        self.character = "♘" if self.color == "white" else "♞"

    def __repr__(self):
        return "knight"
    
    def move_piece(self, board, position):
        super().move_piece(board, position)
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_valid_move(board, row_src, col_src, row_dest, col_dest):
            if self.is_l_shaped_move(row_src, col_src, row_dest, col_dest):
                return True
        return False
    
    def is_l_shaped_move(self, row_src, col_src, row_dest, col_dest):
        dist_y = abs(row_dest - row_src)
        dist_x = abs(col_dest - col_src)
        return (dist_y == 2 and dist_x == 1) or (dist_y == 1 and dist_x == 2)
    
class Pawn(Piece):
    @dataclass
    class EnPassant:
        can_be_captured: bool
        num_turns_true: int

    def __init__(self, color, coordinates):
        super().__init__(color, coordinates)
        self.type = "pawn"
        self.character = "♙" if self.color == "white" else "♟"
        self.en_passant_capture = self.EnPassant(False, 0)
        self.has_moved = False
        
    def __repr__(self):
        return "pawn"
    
    def move_piece(self, board, position):
        super().move_piece(board, position)
        if not self.has_moved:
            self.has_moved = True

        # If en passant capture, delete the piece
        # If at the end of the board, promote the pawn
        if self.is_final_rank():
            self.promote_pawn(board)
        # Remember to increment or reset can_be_captured every turn

    def is_final_rank(self):
        return (self.color == "white" and self.coordinates[0] == 0) or (self.color == "black" and self.coordinates[0] == 7)

    def promote_pawn(self, board):
        while True:
            new_piece = input('Choose a piece - Queen("Q"), Knight("N"), Rook("R") or Bishop("B"): ')
            if new_piece.upper() == "Q" or new_piece.title() == "Queen":
                PieceType = Queen()
                break
            elif new_piece.upper() == "N" or new_piece.title() == "Knight":
                PieceType = Knight()
                break
            elif new_piece.upper() == "R" or new_piece.title() == "Rook":
                PieceType = Rook()
                break
            elif new_piece.upper() == "B" or new_piece.title() == "Bishop":
                PieceType = Bishop()
                break
            print("Invalid selection.")
        row, col = self.coordinates
        board[row][col].piece = PieceType(self.color, self.coordinates)


    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_within_bounds(row_dest, col_dest):
            if self.is_single_space_forward_move(row_src, col_src, row_dest, col_dest) and not super().is_occupied_square(board, row_dest, col_dest):
                return True
            elif self.is_double_space_forward_move(row_src, col_src, row_dest, col_dest) and not super().is_occupied_square(board, row_dest, col_dest) and self.is_clear_path(board, row_src, col_src, row_dest) and not self.has_moved:
                return True
            elif self.is_diagonal_move(row_src, col_src, row_dest, col_dest):
                if super().is_capturable_piece(board, row_src, col_src, row_dest, col_dest):
                    return True
                elif self.can_en_passant_capture(board, row_dest, col_dest):
                    return True
        return False
    
    def perform_capture_if_capturable(self, board, row_src, col_src, row_dest, col_dest):
        if self.is_diagonal_move(row_src, col_src, row_dest, col_dest):
            if super().is_capturable_piece(board, row_src, col_src, row_dest, col_dest):
                self.capture_piece(board, row_dest, col_dest)
            elif self.can_en_passant_capture(board, row_dest, col_dest):
                direction = self.get_en_passant_direction()
                capture_row = row_dest + direction
                self.capture_piece(board, capture_row, col_dest)
    
    def capture_piece(self, board, row_dest, col_dest):
        board[row_dest][col_dest].piece = None
            
    def is_single_space_forward_move(self, row_src, col_src, row_dest, col_dest):
        direction = -1 if self.color == "white" else 1
        return row_dest == row_src + direction and col_dest == col_src
            
    def is_double_space_forward_move(self, row_src, col_src, row_dest, col_dest):
        direction = -2 if self.color == "white" else 2
        return row_dest == row_src + direction and col_dest == col_src
            
    def is_diagonal_move(self, row_src, col_src, row_dest, col_dest):
        direction = -1 if self.color == "white" else 1
        return row_dest == row_src + direction and abs(col_dest - col_src) == 1
        
    def can_en_passant_capture(self, board, row_dest, col_dest):
        direction = self.get_en_passant_direction()
        target_row = row_dest + direction
        target_square = super().get_square(board, target_row, col_dest)
        return target_square.piece.type == "pawn" and target_square.piece.en_passant_capture.can_be_captured
    
    def get_en_passant_direction(self):
        return 1 if self.color == "white" else -1
    
    def is_clear_path(self, board, row_src, col_src, row_dest):
        direction = -1 if self.color == "white" else 1
        distance = abs(row_dest - row_src)
        for i in range(1, distance):
            current_row = row_src + (i * direction)
            if board[current_row][col_src].piece is not None:
                return False
        return True
    
chess = Chess()
print(chess.board.board)