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

		print("   0     1     2     3     4     5     6")
		print("                             ")
		print("| ", self.board[0][0], " | ", self.board[0][1], " | ", self.board[0][2], " | ", self.board[0][3], " | ", self.board[0][4], " | ", self.board[0][5], " | ", self.board[0][6], " |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ", self.board[1][0], " | ", self.board[1][1], " | ", self.board[1][2], " | ", self.board[1][3], " | ", self.board[1][4], " | ", self.board[1][5], " | ", self.board[1][6], " |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ", self.board[2][0], " | ", self.board[2][1], " | ", self.board[2][2], " | ", self.board[2][3], " | ", self.board[2][4], " | ", self.board[2][5], " | ", self.board[2][6], " |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ", self.board[3][0], " | ", self.board[3][1], " | ", self.board[3][2], " | ", self.board[3][3], " | ", self.board[3][4], " | ", self.board[3][5], " | ", self.board[3][6], " |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ", self.board[4][0], " | ", self.board[4][1], " | ", self.board[4][2], " | ", self.board[4][3], " | ", self.board[4][4], " | ", self.board[4][5], " | ", self.board[4][6], " |")
		print("+-----+-----+-----+-----+-----+-----+-----+")
		print("| ", self.board[5][0], " | ", self.board[5][1], " | ", self.board[5][2], " | ", self.board[5][3], " | ", self.board[5][4], " | ", self.board[5][5], " | ", self.board[5][6], " |")
		print("+-----+-----+-----+-----+-----+-----+-----+")


board: TypeBoard = TypeBoard([[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "]])


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

	for i in range(0, 6, 1):
		if not check_if_column_full(i):
			return False
	return True

def check_if_board_empty() -> bool:
	"""
	Check if board is empty
	"""

	for y in range(0,6,1):
		for x in range (0,7,1):
			if board.board[y][x] != " ":
				return False
	return True

max_x: int = 6
max_y: int = 7

def cpu_algorithm_easy(letter: chr) -> None:
	"""
	Easy Algorithm for CPU player (chooses column randomly)

	letter -- character to place
	"""

	random_choice: int = random.randint(0, 6)
	while True:
		if not check_if_column_full(random_choice):
			for i in range(5, -1, -1):
				if board.board[i][random_choice] == " ":
					board.board[i][random_choice] = letter
					return
		else:
			random_choice = random.randint(0, 6)

def evaluate_board(tmp: TypeBoard, last_played: int) -> int:
	"""
	Evaluate board state

	tmp -- evaluation board

	rating -- score based on board evaluation

	last_played -- indicator for which computer last played
	"""
	count_good:int = 0
	count_bad:int = 0
	rating:int = 0
	direction: [[]] = [[0,-1],[0,1],[-1,0],[-1,-1],[-1,1],[1,0],[1,-1],[1,1]]
	for y in range(5,-1,-1):
		for x in range(0,7,1):
			if tmp.board[y][x] == 1:
				for i in direction:
					y_shift = i[0]
					x_shift = i[1]
					if y+y_shift >= 0 and y+y_shift <= 5 and x+x_shift >=0 and x+x_shift <= 6 and tmp.board[y+y_shift][x+x_shift] == 1:
						count_good += 1
						if y+2*y_shift >= 0 and y+2*y_shift <= 5 and x+2*x_shift >=0 and x+2*x_shift <= 6 and tmp.board[y+2*y_shift][x+2*x_shift] == 1:
							count_good += 5
							if y+3*y_shift >= 0 and y+3*y_shift <= 5 and x+3*x_shift >=0 and x+3*x_shift <= 6 and tmp.board[y+3*y_shift][x+3*x_shift] == 1:
								count_good += 1500
							elif last_played == -1 and (y+3*y_shift >= 0 and y+3*y_shift <= 5 and x+3*x_shift >=0 and x+3*x_shift <= 6 and tmp.board[y+3*y_shift][x+3*x_shift] == 0):
								count_good += 1000
			if tmp.board[y][x] == -1:
				for i in direction:
					y_shift = i[0]
					x_shift = i[1]
					if y+y_shift >= 0 and y+y_shift <= 5 and x+x_shift >=0 and x+x_shift <= 6 and tmp.board[y+y_shift][x+x_shift] == -1:
						count_bad += 1
						if y+2*y_shift >= 0 and y+2*y_shift <= 5 and x+2*x_shift >=0 and x+2*x_shift <= 6 and tmp.board[y+2*y_shift][x+2*x_shift] == -1:
							count_bad += 5
							if y+3*y_shift >= 0 and y+3*y_shift <= 5 and x+3*x_shift >=0 and x+3*x_shift <= 6 and tmp.board[y+3*y_shift][x+3*x_shift] == -1:
								count_bad += 1500
							elif last_played == 1 and (y+3*y_shift >= 0 and y+3*y_shift <= 5 and x+3*x_shift >=0 and x+3*x_shift <= 6 and tmp.board[y+3*y_shift][x+3*x_shift] == 0):
								count_bad += 500
	rating = count_good - count_bad
	return rating

def cpu_algorithm_hard(letter: chr) -> None:
	"""
	Hard Algorithm for CPU player (chooses column randomly)

	letter -- character to place

	candidate -- new board matrix for candidate moves

	opponent_letter -- the opponents mark; 'X' if player is 'O' and vice versa

	rating -- calculated rating based on how favorable the future board state is to the CPU
	"""
	if letter == 'X':
		opponent_letter = 'O'
	else:
		opponent_letter = 'X'
	candidate: TypeBoard = TypeBoard([[-2,-2,-2,-2,-2,-2,-2],
	[-2,-2,-2,-2,-2,-2,-2],
	[-2,-2,-2,-2,-2,-2,-2],
	[-2,-2,-2,-2,-2,-2,-2],
	[-2,-2,-2,-2,-2,-2,-2],
	[-2,-2,-2,-2,-2,-2,-2]]) 
	if check_if_board_empty():
		board.board[5][3] = letter
	else:
		for x in range(0,7,1):
			for y in range(5, -1, -1):
				if board.board[y][x] == " ":
					candidate.board[y][x] = 0
					break
				elif board.board[y][x] == opponent_letter:
					candidate.board[y][x] = -1
				elif board.board[y][x] == letter:
					candidate.board[y][x] = 1
		max_rating: int = -9999
		min_rating: int = 9999
		inter_rating: int
		rating: int
		rating1: int
		sel_y: int = 0
		sel_x: int = 0
		opp_y2: int = 0
		opp_x2: int = 0
		for a in range(5,-1,-1):
			for b in range(0,7,1):
				if candidate.board[a][b] == 0:
					candidate.board[a][b] = 1
					rating1 = evaluate_board(candidate,1)
					if rating1 >= 500:
						board.board[a][b] = letter
						print("[%d,%d](%d)" % (a,b,rating1))	
						return
					min_rating = 9999
					for c in range(5,-1,-1):
						for d in range(0,7,1):
							if candidate.board[c][d] == 0:
								candidate.board[c][d] = -1
								inter_rating = evaluate_board(candidate,-1)
								if inter_rating < -1000:
									if board.board[c][d] == " ":
										print("[%d,%d]->[%d,%d](%d)" % (a,b,c,d,rating1))	
										board.board[c][d] = letter
										return
								for e in range(5,-1,-1):
									for f in range(0,7,1):
										if candidate.board[e][f] == 0:
											candidate.board[e][f] = 1
											rating = evaluate_board(candidate,1)
											min_rating = 9999
											for g in range(5,-1,-1):
												for h in range(0,7,1):
													if candidate.board[g][h] == 0:
														candidate.board[g][h] = -1
														inter_rating = evaluate_board(candidate,-1)
														if inter_rating < min_rating:
															min_rating = inter_rating
															opp_y2 = g
															opp_x2 = h
														candidate.board[g][h] = 0
											candidate.board[opp_y2][opp_x2] = -1
											rating = evaluate_board(candidate,-1)
											#print("[%d,%d]->[%d,%d](%d), [%d,%d]->[%d,%d](%d) " % (a,b,c,d,rating1,e,f,opp_y2,opp_x2,rating))	
											if rating > max_rating:
												max_rating = rating
												sel_y = a
												sel_x = b
											candidate.board[e][f] = 0
											candidate.board[opp_y2][opp_x2] = 0
								candidate.board[c][d] = 0
								candidate.board[a][b] = 0					
		board.board[sel_y][sel_x] = letter

def human_algorithm(letter: chr) -> None:
	"""
	Algorithm for Human player (allows human input for choice in column)

	letter -- character to place
	"""

	while True:
		print("Player ", letter, ", select a column to move: ")
		try:
			column_choice = int(input())
			if not check_if_column_full(column_choice) and 0 <= column_choice <= 6:
				for i in range(5, -1, -1):
					if board.board[i][column_choice] == " ":
						board.board[i][column_choice] = letter
						return
			else:
				print("Invalid move, please enter a number from 0-6.")
		except(ValueError, IndexError):
			print("Invalid move, please enter a number from 0-6.")


class TypePlayer:
	"""Contains information and functions necessary for the player"""

	def __init__(self, turn: callable) -> None:
		"""
		Initializes a player object

		turn -- reference to turn based function
		"""

		self.turn: callable = turn

def check_win(state: TypeBoard) -> bool:
	"""
	Check if a player has achieved 4 in a row
	"""

	directions: [[]] = [[1, 0], [1, -1], [1, 1], [0, 1]]
	for i in directions:
		x_shift: int = i[0]
		y_shift: int = i[1]
		for x in range(0, max_x, 1):
			for y in range(0, max_y, 1):
				last_x: int = x + (3*x_shift)
				last_y: int = y + (3*y_shift)
				if 0 <= last_x < max_x and 0 <= last_y < max_y:
					string: str = state.board[x][y]
					if string != " " and string == state.board[x+x_shift][y+y_shift] and string == state.board[x+2*x_shift][y+2*y_shift] and string == state.board[last_x][last_y]:
						return True
	return False


def state_game(state_information_instance: TypeStateInformation, player1: TypePlayer, player2: TypePlayer) -> None:
	"""
	Game state

	state_information_instance -- Instance containing state information
	player1 -- First player (Human/CPU)
	player2 -- Second player (Human/CPU)
	"""

	board.board = [[" ", " ", " ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " ", " ", " "]]
	player_flag: int = 0
	while player_flag != -1:
		os.system("cls" if os.name == "nt" else "clear")
		board.print_board()
		print("Player 1: X")
		print("Player 2: O")
		if player_flag % 2 == 0:
			player1.turn('X')
			if state_information_instance.player_count == 0:
				input("Press Enter To Continue.")
		else:
			player2.turn('O')
			if state_information_instance.player_count != 2:
				input("Press Enter To Continue.")
		if check_if_board_full():
			os.system("cls" if os.name == "nt" else "clear")
			print("It's a Tie!")
			break
		if check_win(board):
			os.system("cls" if os.name == "nt" else "clear")
			print("Player ", (player_flag % 2) + 1, " has won!")
			break
		player_flag += 1
	board.print_board()
	print("Player 1: X")
	print("Player 2: O")
	input("Press Enter To Continue.")

def state_cpuchoice(state_information_instance: TypeStateInformation, sub_menu_string: str) -> TypePlayer:
	"""
	CPU difficulty choice state

	state_information_instance -- Instance containing state information
	sub_menu_string -- Indicates CPU difficulty to edit
	"""
	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		if sub_menu_string == "2":
			print("|    CPU 1 Difficulty   |")
		elif sub_menu_string == "3":
			print("|    CPU 1 Difficulty   |")
		print("+-----------------------+")
		print("|   Difficulty Choice   |")
		print("+-----------------------+")
		print("| 1. Easy               |")
		print("| 2. Hard               |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			cpu: TypePlayer = TypePlayer(cpu_algorithm_easy)
			return cpu
		elif state_information_instance.menu_option == "2":
			cpu: TypePlayer = TypePlayer(cpu_algorithm_hard)
			return cpu
	state_information_instance.menu_option = "-1"


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
			cpu1 = state_cpuchoice(state_information_instance, state_information_instance.menu_option)
		elif state_information_instance.menu_option == "3":
			cpu2 = state_cpuchoice(state_information_instance, state_information_instance.menu_option)
		elif state_information_instance.menu_option == "9":
			if state_information_instance.player_count == 1:
				human1: TypePlayer = TypePlayer(human_algorithm)
				# cpu2: TypePlayer = TypePlayer(cpu_algorithm_easy)
				state_game(state_information_instance, human1, cpu2)
			elif state_information_instance.player_count == 2:
				human1: TypePlayer = TypePlayer(human_algorithm)
				human2: TypePlayer = TypePlayer(human_algorithm)
				state_game(state_information_instance, human1, human2)
			elif state_information_instance.player_count == 0:
				# cpu1: TypePlayer = TypePlayer(cpu_algorithm_easy)
				# cpu2: TypePlayer = TypePlayer(cpu_algorithm_hard)
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
