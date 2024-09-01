from __future__ import annotations
import sys
from typing import Optional
from chess_attributes import ChessAttributes

class Player(ChessAttributes):
    def __init__(self, perspective: str, color: str, is_cpu: bool, difficulty: Optional[str] = None, board: 'Board' = None):
        super().__init__()
        self.board = board
        self.perspective = perspective
        self.color: str = color
        self.is_cpu: str = is_cpu
        self.difficulty: str = difficulty # None, easy, medium or hard
        self.pieces = []
        self.valid_moves = []
        self.is_in_check = False

    def assign_board(self, board: 'Board'):
        self.board = board.board

    def take_turn(self):
        self.display_board()
        self.update_en_passant_statuses()
        # if self.is_in_check():

        # else:
        print(f"{self.color.title()}'s turn to move.")
        while True:
            src_pos, dest_pos = self.get_player_input()
            row, col = self.get_coords_from_pos(src_pos, self.perspective)
            chosen_piece = self.board[row][col].piece
            if chosen_piece.move_piece(self.board, dest_pos):
                return
            else:
                print("Invalid move.")

    def get_player_input(self):
        while True:
            while True:
                response = input('Please enter the position (e.g. "c5") of the piece that you want to move, or "resign" to end the game: ')
                if response.upper() == "RESIGN":
                    return self.resign_game()
                elif self.is_valid_position(response) and self.is_friendly_piece(response):
                    src_pos = response
                    break
                print("Invalid position.")
            self.show_valid_moves(src_pos)
            response = input('Please enter the position (e.g. "c5") that you want to move the piece to: ')
            if self.is_valid_position(response):
                dest_pos = response
                break
            print("Invalid position.")
        return src_pos, dest_pos
    
    def show_valid_moves(self, src_pos):
        row, col = self.get_coords_from_pos(src_pos, self.perspective)
        chosen_piece = self.board[row][col].piece
        self.valid_moves = chosen_piece.list_valid_moves(self.board, row, col)
        self.display_board()
        self.valid_moves = []


    def is_valid_position(self, position):
        def is_valid_length(position):
            return len(position) == 2
        
        def is_valid_letter(position):
            return position[0].lower() in "abcdefgh"
        
        def is_valid_number(position):
            return position[1] in "12345678"

        return is_valid_length(position) and is_valid_letter(position) and is_valid_number(position)
    
    def is_friendly_piece(self, position):
        row, col = self.get_coords_from_pos(position, self.perspective)
        target_position = self.board[row][col]
        return target_position.piece and target_position.piece.color == self.color


    def resign_game(self):
        if self.color == "white":
            print("White resigned. Black wins the game.")
        else:
            print("Black resigned. White wins the game.")
        sys.exit()

    def update_en_passant_statuses(self):
        for piece in self.pieces:
            if piece.type == "pawn" and piece.en_passant_capture.can_be_captured:
                # If the pawn can be captured, and has been in this state for less than one turn, increment num_turns_true by one
                if piece.en_passant_capture.num_turns_true == 0:
                    piece.en_passant_capture.num_turns_true += 1
                # If the pawn has been in this state for one or more turns, reset can_be_captured to False and num_turns_true to zero
                elif piece.en_passant_capture.num_turns_true > 0:
                    piece.en_passant_capture.can_be_captured = False
                    piece.en_passant_capture.num_turns_true = 0

    def display_board(self):
        for row in range(self.BOARD_SIZE + 1):
            for col in range(self.BOARD_SIZE + 1):
                if (row == self.BOARD_SIZE) or (col == 0):
                    if (row == self.BOARD_SIZE) and (col == 0):
                        print("  ", end="")
                    position = self.get_pos_from_coords((row, col), self.perspective)
                    if row == self.BOARD_SIZE and col < self.BOARD_SIZE:
                        print(f" {position[0].upper()}", end="")
                    elif col == 0:
                        print(f" {position[1]}", end="")
                else:
                    if (row, col - 1) in self.valid_moves:
                        sq_color = self.get_move_highlight_color(row, col - 1)
                    else:
                        sq_color = self.convert_color_to_escape_code(row, col - 1)
                    if chess_piece := self.board[row][col - 1].piece:
                        character = chess_piece.character
                        print(f"\033[30;{sq_color}m {character}", end="")
                        print("\033[0m", end="")
                    else:
                        print(f"\033[30;{sq_color}m  ", end="")
                        print("\033[0m", end="")
            print()

    def convert_color_to_escape_code(self, row, col):
        color = self.board[row][col].color
        if color == "white":
            return "107"
        else:
            return "104"
        
    def get_move_highlight_color(self, row, col):
        color = self.board[row][col].color
        if color == "white":
            return "101"
        else:
            return "41"