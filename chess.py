from typing import Tuple
from board import Board
from chess_attributes import ChessAttributes
from player import Player

class Chess(ChessAttributes):
    def __init__(self):
        super().__init__()
        self.perspective = None
        self.is_cpu_opponent = False
        self.cpu_difficulty = None
        self.white_player = None
        self.black_player = None
        self.current_turn = None
        self.winner = None
        self.get_game_settings()
        self.instantiate_players()
        self._board = Board(self.perspective, self.white_player, self.black_player)
        self.white_player.assign_board(self._board)
        self.black_player.assign_board(self._board)
        self.run_game_loop()
        self.announce_winner()

    @property
    def board(self):
        return self._board
    
    def get_game_settings(self) -> None:
        while True:
            color: str = input("Do you want to be White or Black? ")
            if color.upper() == "WHITE":
                self.perspective = "white"
                break
            elif color.upper() == "BLACK":
                self.perspective = "black"
                break
        while True:
            opponent: str = input("Play against a computer? Y/N ")
            if opponent.upper() == "Y":
                self.is_cpu_opponent = True
                break
            elif opponent.upper() == "N":
                self.is_cpu_opponent = False
                break
        if self.is_cpu_opponent:
            while True:
                difficulty: str = input("Select computer difficulty (Easy, Medium, Hard): ")
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
        if self.perspective == "white":
            self.white_player = Player(self.perspective, "white", False)
            self.black_player = Player(self.perspective, "black", self.is_cpu_opponent, self.cpu_difficulty)
            self.current_turn = "white"
        else:
            self.black_player = Player(self.perspective, "black", False)
            self.white_player = Player(self.perspective, "white", self.is_cpu_opponent, self.cpu_difficulty)
            self.current_turn = "black"

    def run_game_loop(self):
        while not self.winner:
            if self.current_turn == "white":
                self.white_player.take_turn()
                self.current_turn = "black"
            elif self.current_turn == "black":
                self.black_player.take_turn()
                self.current_turn = "white"

    def announce_winner(self):
        if self.winner == "white" or self.winner == "black":
            print(f"{self.winner.title()} player wins.")
        elif self.winner == "stalemate":
            print("Neither player wins due to stalemate.")

chess = Chess()

