from typing import Tuple

class ChessAttributes:
    def __init__(self):
        self.BOARD_SIZE = 8

    def get_pos_from_coords(self, coordinates: Tuple[int, int], perspective: str) -> str:
        square_y, square_x = coordinates
        return self.get_column_pos(square_x, perspective) + self.get_row_pos(square_y, perspective)
        
    def get_coords_from_pos(self, position: str, perspective: str) -> Tuple[int, int]:
        square_x, square_y = position
        return (self.get_row_coord(square_y, perspective), self.get_col_coord(square_x, perspective))
        
    def get_row_pos(self, square_y: int, perspective: str) -> str:
        if perspective == "white":
            return str(self.BOARD_SIZE - square_y)
        else:
            return str(square_y + 1)
    
    def get_column_pos(self, square_x: int, perspective: str) -> str:
        if perspective == "white":
            return chr(ord("a") + square_x)
        else:
            return chr(ord("a") + self.BOARD_SIZE - (square_x + 1))
    
    def get_row_coord(self, square_y: str, perspective: str) -> int:
        if perspective == "white":
            return self.BOARD_SIZE - int(square_y)
        else:
            return int(square_y) - 1

    def get_col_coord(self, square_x: str, perspective: str) -> int:
        if perspective == "white":
            return ord(square_x) - ord("a")
        else:
            return self.BOARD_SIZE - (ord(square_x) - ord("a")) - 1