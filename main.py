#!/usr/bin/env python3

import pygame
import os
import random

class TypeStateInformation:
	"""Contains information necessary between all states"""

	def __init__(self, menu_option: str, player_count: int) -> None:
		"""
		Initializes a typeStateInformation object

		menu_option -- The currently selected menu option
		player_count -- Selected number of human players
		"""

		self.menu_option: str = menu_option
		self.player_count: int = player_count

class TypeBoard:
	"""Contains information and functions necessary for board manipulation"""

	def __init__(self, board: [[]]) -> None:
		"""
		Initializes a board object

		board -- 2D character array to represent the board
		"""

		self.board: [[]] = board

	def print_board(self) -> None:
		"""
		Prints the board object
		"""

		print("   1     2     3     4     5     6     7")
		print("                             ")
		print("| ",self.board[0][0]," | ",self.board[0][1]," | ",self.board[0][2]," | ",self.board[0][3]," | ",self.board[0][4]," | ",self.board[0][5]," | ",self.board[0][6]," |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ",self.board[1][0]," | ",self.board[1][1]," | ",self.board[1][2]," | ",self.board[1][3]," | ",self.board[1][4]," | ",self.board[1][5]," | ",self.board[1][6]," |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ",self.board[2][0]," | ",self.board[2][1]," | ",self.board[2][2]," | ",self.board[2][3]," | ",self.board[2][4]," | ",self.board[2][5]," | ",self.board[2][6]," |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ",self.board[3][0]," | ",self.board[3][1]," | ",self.board[3][2]," | ",self.board[3][3]," | ",self.board[3][4]," | ",self.board[3][5]," | ",self.board[3][6]," |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ",self.board[4][0]," | ",self.board[4][1]," | ",self.board[4][2]," | ",self.board[4][3]," | ",self.board[4][4]," | ",self.board[4][5]," | ",self.board[4][6]," |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ",self.board[5][0]," | ",self.board[5][1]," | ",self.board[5][2]," | ",self.board[5][3]," | ",self.board[5][4]," | ",self.board[5][5]," | ",self.board[5][6]," |")
		print("+-----+-----+-----+-----+-----+-----+-----+")

board: TypeBoard = TypeBoard([[" "," "," "," "," "," "," "],
       [" "," "," "," "," "," "," "],
       [" "," "," "," "," "," "," "],
       [" "," "," "," "," "," "," "],
       [" "," "," "," "," "," "," "],
	   [" "," "," "," "," "," "," "]])

def check_if_column_full(col: int) -> bool:
	"""
	Check if column is full

	col -- column to check
	"""

	if board.board[0][col] != " ":
		return True
	return False

def check_if_board_full() -> bool:
	"""
	Check if board is full
	"""

	for i in range(0,6,1):
		if check_if_column_full(i) == True:
			continue
		else:
			return False
	return True

def cpu_algorithm_easy(letter: chr) -> None:
	"""
	Easy Algorithm for CPU player (chooses column randomly)

	letter -- character to place
	"""

	random_choice = random.randint(0,6)
	for i in range(5,-1,-1):
		if check_if_column_full(random_choice) == False:
			if board.board[i][random_choice] == " ":
				board.board[i][random_choice] = letter
				break
		else:
			random_choice = random.randint(0,6)

class TypePlayer:
	"""Contains information and functions necessary for the player"""

	def __init__(self, turn: callable) -> None:
		"""
		Initializes a player object

		turn -- reference to turn based function
		letter -- player letter, either 'X' or 'O'
		"""

		self.turn: callable = turn

max_x: int = 6
max_y: int = 7

def check_win() -> bool:
	"""
	Check if a player has achieved 4 in a row
	"""

	directions: [[]] = [[1,0], [1,-1], [1,1], [0,1]]
	for i in directions:
		x_shift: int = i[0]
		y_shift: int = i[1]
		for x in range(0,max_x,1):
			for y in range(0,max_y,1):
				last_x: int = x + (3*x_shift)
				last_y: int = y + (3*y_shift)
				if 0 <= last_x and last_x < max_x and 0 <= last_y and last_y < max_y:
					string: str = board.board[x][y]
					if string != " " and string == board.board[x+x_shift][y+y_shift] and string == board.board[x+2*x_shift][y+2*y_shift] and string == board.board[last_x][last_y]:
						return True
	return False

def state_game(state_information_instance: TypeStateInformation, player1: TypePlayer, player2: TypePlayer) -> None:
	"""
	Game state

	state_information_instance -- Instance containing state information
	player1 -- First player (Human/CPU)
	player2 -- Second player (Human/CPU)
	"""

	board.board = [[" "," "," "," "," "," "," "],
       [" "," "," "," "," "," "," "],
       [" "," "," "," "," "," "," "],
       [" "," "," "," "," "," "," "],
       [" "," "," "," "," "," "," "],
	   [" "," "," "," "," "," "," "]]
	player_flag: int = 0
	while player_flag != -1:
		os.system("cls" if os.name == "nt" else "clear")
		board.print_board()
		print("Player 1: X")
		print("Player 2: O")
		input("Press Enter To Continue: ")
		if check_if_board_full() == True:
			os.system("cls" if os.name == "nt" else "clear")
			print("It's a Tie!")
			break
		if check_win() == True:
			os.system("cls" if os.name == "nt" else "clear")
			print("Player ", (player_flag % 2) ," has won!")
			break
		if player_flag % 2 == 0:
			player1.turn('X')
		else:
			player2.turn('O')
		player_flag += 1
	board.print_board()
	print("Player 1: X")
	print("Player 2: O")
	input("Press Enter To Continue: ")

def state_gamesetup(state_information_instance: TypeStateInformation, sub_menu_string: str) -> None:
	"""
	Game-setup state

	state_information_instance -- Instance containing state information
	sub_menu_string -- Indicates which submenu text to display in menu ("local"/"network")
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		if sub_menu_string == "local":
			print("|       Local-play      |")
		elif sub_menu_string == "network":
			print("|     Network-play      |")
		print("+-----------------------+")
		print("|       Game Setup      |")
		print("+-----------------------+")
		print("| 1. SFX: ON / [OFF]    |")
		if state_information_instance.player_count < 2:
			print("| 2. CPU #1 Difficulty: |")
			if state_information_instance.player_count < 1:
				print("| 3. CPU #2 Difficulty: |")
		print("| 9. Start game         |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			print("##TODO##")
		elif state_information_instance.menu_option == "2":
			print("##TODO##")
		elif state_information_instance.menu_option == "3":
			print("##TODO##")
		elif state_information_instance.menu_option == "9":
			cpu1: TypePlayer = TypePlayer(cpu_algorithm_easy)
			cpu2: TypePlayer = TypePlayer(cpu_algorithm_easy)
			state_game(state_information_instance, cpu1, cpu2)
	state_information_instance.menu_option = "-1"


def state_localplay(state_information_instance: TypeStateInformation):
	"""
	Local-play state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("|       Local-play      |")
		print("+-----------------------+")
		print("| 1. 1-player           |")
		print("| 2. 2-player           |")
		print("| 3. Spectate           |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			state_information_instance.player_count = 1
			state_gamesetup(state_information_instance, "local")
		elif state_information_instance.menu_option == "2":
			state_information_instance.player_count = 2
			state_gamesetup(state_information_instance, "local")
		elif state_information_instance.menu_option == "3":
			state_information_instance.player_count = 0
			state_gamesetup(state_information_instance, "local")
	state_information_instance.menu_option = "-1"


def state_networkplay(state_information_instance: TypeStateInformation):
	"""
	Network-play state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("|      Network-play     |")
		print("+-----------------------+")
		print("| 1. Host game          |")
		print("| 2. Join game          |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			print("##TODO##")
		elif state_information_instance.menu_option == "2":
			print("##TODO##")
	state_information_instance.menu_option = "-1"


def state_options(state_information_instance: TypeStateInformation):
	"""
	Options state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("|        Options        |")
		print("+-----------------------+")
		print("| 1. Resolution         |")
		print("| 2. Display Name       |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			print("##TODO##")
		elif state_information_instance.menu_option == "2":
			print("##TODO##")
	state_information_instance.menu_option = "-1"


def state_mainmenu(state_information_instance: TypeStateInformation):
	"""
	Main Menu state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("| 1. Local-play         |")
		print("| 2. Network-play       |")
		print("| 3. Options            |")
		print("| 0. Quit               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			state_localplay(state_information_instance)
		elif state_information_instance.menu_option == "2":
			state_networkplay(state_information_instance)
		elif state_information_instance.menu_option == "3":
			state_options(state_information_instance)
	state_information_instance.menu_option = "-1"


def main():
	state_information_instance: TypeStateInformation = TypeStateInformation("-1", -1)
	state_mainmenu(state_information_instance)


if __name__ == "__main__":
	main()
