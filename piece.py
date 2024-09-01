from __future__ import annotations
from dataclasses import dataclass
from chess_attributes import ChessAttributes

class Piece(ChessAttributes):
    def __init__(self, color, perspective, coordinates):
        super().__init__()
        self.color = color
        self.perspective = perspective
        self.coordinates = coordinates
        self.position = self.get_pos_from_coords(coordinates, self.perspective)

    def move_piece(self, board, row_src, col_src, row_dest, col_dest):
        source_square = self.get_square(board, row_src, col_src)
        dest_square = self.get_square(board, row_dest, col_dest)
        dest_square.piece = source_square.piece
        source_square.piece = None
        self.coordinates = (row_dest, col_dest)
        self.position = self.get_pos_from_coords(self.coordinates, self.perspective)

    def list_valid_moves(self, board, row_src, col_src):
        valid_moves = []
        for row_dest in range(self.BOARD_SIZE):
            for col_dest in range(self.BOARD_SIZE):
                if self.is_valid_move(board, row_src, col_src, row_dest, col_dest):
                    valid_moves.append((row_dest, col_dest))
        return valid_moves

    def get_move_coordinates(self, position):
        row_src, col_src = self.coordinates
        dest_coords = self.get_coords_from_pos(position, self.perspective)
        row_dest, col_dest = dest_coords
        return row_src, col_src, row_dest, col_dest

    def test_move_piece(self, board, row_dest, col_dest):
        row_src, col_src = self.coordinates
        print(f"Source square: {row_src}, {col_src}")
        source_square = self.get_square(board, row_src, col_src)
        print(f"Destination square: {row_dest}, {col_dest}")
        dest_square = self.get_square(board, row_dest, col_dest)
        captured_piece = dest_square.piece
        dest_square.piece = source_square.piece
        source_square.piece = None
        self.coordinates = (row_dest, col_dest)
        self.position = self.get_pos_from_coords(self.coordinates, self.perspective)
        return captured_piece

    def reset_move(self, board, row_dest, col_dest, captured_piece):
        row_src, col_src = self.coordinates
        source_square = self.get_square(board, row_src, col_src)
        dest_square = self.get_square(board, row_dest, col_dest)
        dest_square.piece = source_square.piece
        source_square.piece = captured_piece
        self.coordinates = (row_dest, col_dest)
        self.position = self.get_pos_from_coords(self.coordinates, self.perspective)

    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        return self.is_within_bounds(row_dest, col_dest) and (not self.is_occupied_square(board, row_dest, col_dest) or self.is_capturable_piece(board, row_src, col_src, row_dest, col_dest))

    def is_capturable_piece(self, board, row_src, col_src, row_dest, col_dest):
        if board[row_dest][col_dest].piece:
            src_color = self.get_piece_color(board, row_src, col_src)
            dest_color = self.get_piece_color(board, row_dest, col_dest)
            return self.is_occupied_square(board, row_dest, col_dest) and dest_color is not src_color
        else:
            return False
    
    def is_occupied_square(self, board, row, col):
        return board[row][col].piece

    def get_square(self, board, row, col) -> 'Square':
        return board[row][col]
    
    def get_piece_color(self, board, row, col):
        target_square = self.get_square(board, row, col)
        return target_square.piece.color
    
    def is_within_bounds(self, row_dest, col_dest):
        return 0 <= row_dest < self.BOARD_SIZE and 0 <= col_dest < self.BOARD_SIZE

    
class King(Piece):
    def __init__(self, color, perspective, coordinates, opponent_pieces):
        super().__init__(color, perspective, coordinates)
        self.type = "king"
        self.character = "♔" if self.color == "white" else "♚"
        self.opponent_pieces = opponent_pieces
        self.has_moved = False

    def __repr__(self):
        return "king"
    
    def move_piece(self, board, position):
        row_src, col_src, row_dest, col_dest = self.get_move_coordinates(position)
        if self.is_valid_single_space_move(board, row_src, col_src, row_dest, col_dest):
            self.perform_single_space_move(board, row_src, col_src, row_dest, col_dest)
            if not self.has_moved:
                self.has_moved = True
            return True
        elif self.is_valid_castling_move(board, row_src, col_src, row_dest, col_dest):
            self.perform_castling_move(board, row_src, col_src, row_dest, col_dest)
            if not self.has_moved:
                self.has_moved = True
            return True
        else:
            return False

    def perform_single_space_move(self, board, row_src, col_src, row_dest, col_dest):
        source_square = self.get_square(board, row_src, col_src)
        dest_square = self.get_square(board, row_dest, col_dest)
        dest_square.piece = source_square.piece
        source_square.piece = None
        self.coordinates = (row_dest, col_dest)
        self.position = self.get_pos_from_coords(self.coordinates, self.perspective)

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
        self.position = self.get_pos_from_coords(self.coordinates, self.perspective)

        # Move rook
        rook_source_square = self.get_square(board, row_src, col_dest)
        rook_col_dest = king_col_dest - castling_direction
        rook_dest_square = self.get_square(board, row_dest, rook_col_dest)
        rook_dest_square.piece = rook_source_square.piece
        rook_source_square.piece = None
        rook_coords = (row_dest, rook_col_dest)
        rook_dest_square.piece.coordinates = rook_coords
        rook_dest_square.piece.position = self.get_pos_from_coords(rook_coords, self.perspective)

    def can_attack_position(self, board, row_src, col_src, row_dest, col_dest):
        """
        This function exists specifically to check whether the opponent king can attack the square that the friendly king is intending to move to.
        """
        return self.is_valid_single_space_move(board, row_src, col_src, row_dest, col_dest)
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        return self.is_valid_single_space_move(board, row_src, col_src, row_dest, col_dest) or self.is_valid_castling_move(board, row_src, col_src, row_dest, col_dest)
    
    def is_valid_single_space_move(self, board, row_src, col_src, row_dest, col_dest):
        if abs(row_dest - row_src) <= 1 and abs(col_dest - col_src) <= 1 and not (abs(row_dest - row_src) == 0 and abs(col_dest - col_src) == 0):
            if self.is_safe_square(board, row_src, col_src, row_dest, col_dest) and super().is_valid_move(board, row_src, col_src, row_dest, col_dest):
                return True
        return False
            
    def is_valid_castling_move(self, board, row_src, col_src, row_dest, col_dest):
        if self.is_friendly_rook(board, row_src, col_src, row_dest, col_dest) and self.has_not_moved_rook(board, row_dest, col_dest):
            if not self.is_in_check(board, row_src, col_src) and self.has_not_moved_king():
                if self.is_clear_path(board, row_src, col_src, col_dest) and self.are_safe_intermediate_squares(board, row_src, col_src, row_dest, col_dest):
                    return True
        return False
    
    def has_not_moved_rook(self, board, row, col):
        return not board[row][col].piece.has_moved
    
    def has_not_moved_king(self):
        print(f"King hasn't moved: {not self.has_moved}")
        return not self.has_moved
                
    def is_clear_path(self, board, row_src, col_src, col_dest):
        dist_x = abs(col_dest - col_src)
        castling_direction = self.get_castling_direction(col_src, col_dest)
        for i in range(1, dist_x):
            if board[row_src][col_src + (i * castling_direction)].piece is not None:
                return False
        return True

    def is_friendly_rook(self, board, row_src, col_src, row_dest, col_dest):
        return board[row_dest][col_dest].piece and board[row_dest][col_dest].piece.type == "rook" and not self.is_capturable_piece(board, row_src, col_src, row_dest, col_dest)

    def are_safe_intermediate_squares(self, board, row_src, col_src, row_dest, col_dest):
        castling_direction = self.get_castling_direction(col_src, col_dest)
        castling_distance = 2
        for i in range(1, castling_distance + 1):
            col_step = col_src + (i * castling_direction)
            if not self.is_safe_square(board, row_src, col_src, row_dest, col_step):
                return False
        return True
    
    def get_castling_direction(self, col_src, col_dest):
        dist_x = abs(col_dest - col_src)
        return (col_dest - col_src) // dist_x
    
    def is_safe_square(self, board, row_src, col_src, row_dest, col_dest):
        captured_piece = self.test_move_piece(board, row_dest, col_dest)
        if self.is_in_check(board, row_dest, col_dest):
            self.reset_move(board, row_src, col_src, captured_piece)
            return False
        self.reset_move(board, row_src, col_src, captured_piece)
        return True
    
    def is_in_check(self, board, row, col):
        for piece in self.opponent_pieces:
            opponent_row, opponent_col = piece.coordinates
            if piece.can_attack_position(board, opponent_row, opponent_col, row, col):
                return True
        return False

class Queen(Piece):
    def __init__(self, color, perspective, coordinates):
        super().__init__(color, perspective, coordinates)
        self.type = "queen"
        self.character = "♕" if self.color == "white" else "♛"

    def __repr__(self):
        return "queen"
    
    def move_piece(self, board, position):
        row_src, col_src, row_dest, col_dest = self.get_move_coordinates(position)
        if self.is_valid_move(board, row_src, col_src, row_dest, col_dest):
            super().move_piece(board, row_src, col_src, row_dest, col_dest)
            return True
        else:
            return False
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_valid_move(board, row_src, col_src, row_dest, col_dest):
            if self.is_linear_move(row_src, col_src, row_dest, col_dest) or self.is_diagonal_move(row_src, col_src, row_dest, col_dest):
                if self.is_clear_path(board, row_src, col_src, row_dest, col_dest):
                    return True
        return False
    
    def can_attack_position(self, board, row_src, col_src, row_dest, col_dest):
        return self.is_valid_move(board, row_src, col_src, row_dest, col_dest)

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
    def __init__(self, color, perspective, coordinates):
        super().__init__(color, perspective, coordinates)
        self.type = "bishop"
        self.character = "♗" if self.color == "white" else "♝"

    def __repr__(self):
        return "bishop"
    
    def move_piece(self, board, position):
        row_src, col_src, row_dest, col_dest = self.get_move_coordinates(position)
        if self.is_valid_move(board, row_src, col_src, row_dest, col_dest):
            super().move_piece(board, row_src, col_src, row_dest, col_dest)
            return True
        else:
            return False
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_valid_move(board, row_src, col_src, row_dest, col_dest) and self.is_diagonal_move(row_src, col_src, row_dest, col_dest):
            if self.is_clear_path(board, row_src, col_src, row_dest, col_dest):
                return True
        return False
    
    def can_attack_position(self, board, row_src, col_src, row_dest, col_dest):
        return self.is_valid_move(board, row_src, col_src, row_dest, col_dest)
    
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
    def __init__(self, color, perspective, coordinates):
        super().__init__(color, perspective, coordinates)
        self.type = "rook"
        self.character = "♖" if self.color == "white" else "♜"
        self.has_moved = False

    def __repr__(self):
        return "rook"

    def move_piece(self, board, position):
        row_src, col_src, row_dest, col_dest = self.get_move_coordinates(position)
        if self.is_valid_move(board, row_src, col_src, row_dest, col_dest):
            super().move_piece(board, row_src, col_src, row_dest, col_dest)
            if not self.has_moved:
                self.has_moved = True
            return True
        else:
            return False
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_valid_move(board, row_src, col_src, row_dest, col_dest) and self.is_linear_move(row_src, col_src, row_dest, col_dest):
            if self.is_clear_path(board, row_src, col_src, row_dest, col_dest):
                return True
        return False
    
    def can_attack_position(self, board, row_src, col_src, row_dest, col_dest):
        return self.is_valid_move(board, row_src, col_src, row_dest, col_dest)
    
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
    def __init__(self, color, perspective, coordinates):
        super().__init__(color, perspective, coordinates)
        self.type = "knight"
        self.character = "♘" if self.color == "white" else "♞"

    def __repr__(self):
        return "knight"
    
    def move_piece(self, board, position):
        row_src, col_src, row_dest, col_dest = self.get_move_coordinates(position)
        if self.is_valid_move(board, row_src, col_src, row_dest, col_dest):
            super().move_piece(board, row_src, col_src, row_dest, col_dest)
            return True
        else:
            return False
    
    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if super().is_valid_move(board, row_src, col_src, row_dest, col_dest):
            if self.is_l_shaped_move(row_src, col_src, row_dest, col_dest):
                return True
        return False
    
    def can_attack_position(self, board, row_src, col_src, row_dest, col_dest):
        return self.is_valid_move(board, row_src, col_src, row_dest, col_dest)
    
    def is_l_shaped_move(self, row_src, col_src, row_dest, col_dest):
        dist_y = abs(row_dest - row_src)
        dist_x = abs(col_dest - col_src)
        return (dist_y == 2 and dist_x == 1) or (dist_y == 1 and dist_x == 2)
    
class Pawn(Piece):
    @dataclass
    class EnPassant:
        can_be_captured: bool
        num_turns_true: int

    def __init__(self, color, perspective, coordinates):
        super().__init__(color, perspective, coordinates)
        self.type = "pawn"
        self.character = "♙" if self.color == "white" else "♟"
        self.en_passant_capture = self.EnPassant(False, 0)
        self.has_moved = False
        
    def __repr__(self):
        return "pawn"
    
    def move_piece(self, board, position):
        row_src, col_src, row_dest, col_dest = self.get_move_coordinates(position)
        if self.is_valid_move(board, row_src, col_src, row_dest, col_dest):
            self.perform_capture_if_capturable(board, row_src, col_src, row_dest, col_dest)
            super().move_piece(board, row_src, col_src, row_dest, col_dest)
            if not self.has_moved:
                self.has_moved = True
            # If at the end of the board, promote the pawn
            if self.is_final_rank():
                self.promote_pawn(board)
            return True
        else:
            return False

    def is_final_rank(self):
        return (self.color == "white" and self.coordinates[0] == 0) or (self.color == "black" and self.coordinates[0] == 7)

    def promote_pawn(self, board):
        while True:
            new_piece = input('Choose a piece - Queen("Q"), Knight("N"), Rook("R") or Bishop("B"): ')
            if new_piece.upper() == "Q" or new_piece.title() == "Queen":
                PieceType = Queen
                break
            elif new_piece.upper() == "N" or new_piece.title() == "Knight":
                PieceType = Knight
                break
            elif new_piece.upper() == "R" or new_piece.title() == "Rook":
                PieceType = Rook
                break
            elif new_piece.upper() == "B" or new_piece.title() == "Bishop":
                PieceType = Bishop
                break
            print("Invalid selection.")
        row, col = self.coordinates
        board[row][col].piece = PieceType(self.color, self.perspective, self.coordinates)

    def is_valid_move(self, board, row_src, col_src, row_dest, col_dest):
        if self.is_within_bounds(row_dest, col_dest):
            if self.is_single_space_forward_move(row_src, col_src, row_dest, col_dest) and not self.is_occupied_square(board, row_dest, col_dest):
                return True
            elif self.is_double_space_forward_move(row_src, col_src, row_dest, col_dest) and not self.is_occupied_square(board, row_dest, col_dest) and self.is_clear_path(board, row_src, col_src, row_dest) and not self.has_moved:
                self.en_passant_capture.can_be_captured = True
                return True
            elif self.is_diagonal_move(row_src, col_src, row_dest, col_dest):
                if self.is_capturable_piece(board, row_src, col_src, row_dest, col_dest):
                    return True
                elif self.can_en_passant_capture(board, row_dest, col_dest):
                    return True
        return False
    
    def can_attack_position(self, board, row_src, col_src, row_dest, col_dest):
        if self.is_diagonal_move(row_src, col_src, row_dest, col_dest):
            if self.is_capturable_piece(board, row_src, col_src, row_dest, col_dest):
                return True
        return False
    
    def perform_capture_if_capturable(self, board, row_src, col_src, row_dest, col_dest):
        if self.is_diagonal_move(row_src, col_src, row_dest, col_dest):
            if self.is_capturable_piece(board, row_src, col_src, row_dest, col_dest):
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
        target_square = self.get_square(board, target_row, col_dest)
        return target_square.piece and target_square.piece.type == "pawn" and target_square.piece.en_passant_capture.can_be_captured
    
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
    
    