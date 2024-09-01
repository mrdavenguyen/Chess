from typing import Tuple
from chess_attributes import ChessAttributes

BOARD_SIZE = 8

class Square(ChessAttributes):
    def __init__(self, coordinates: Tuple[int, int], perspective: str) -> None:
        super().__init__()
        self.coordinates: Tuple[int, int] = coordinates
        self.perspective = perspective
        self.position: str = self.get_pos_from_coords(coordinates, self.perspective)
        self.color: str = None # Color of the square ("black" or "white")
        self.piece: str = None

    def __repr__(self):
        return f"{self.piece.color.title()} {self.piece} on {self.position}" if self.piece else f"Blank square at {self.position}"
    
    def add_piece(self):
        pass

