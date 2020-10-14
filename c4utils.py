#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import random


def get_board_maximums() -> c4gui.Coordinates:
	"""
	Get the maximum board dimensions
	"""

	return c4gui.Coordinates(7, 6)
	# Deprecated but may be useful
	# max_y: int = len(board)
	# max_x: int = len(board[0]) if max_y > 0 else 0
	# return c4gui.Coordinates(max_x, max_y)


def check_if_column_full(board: [[]], col: int) -> bool:
	"""
	Check if a given column is full

	board -- the 2D game board
	col -- column to check
	"""

	return board[0][col] != " "


def check_if_board_full(board: [[]]) -> bool:
	"""
	Check if a given board is full

	board -- the 2D game board
	"""

	for i in range(len(board)+1):
		if not check_if_column_full(board, i):
			return False
	return True


def check_win(board: [[]]) -> bool:
	"""
	Check if a player has achieved 4 in a row

	board -- the 2D game board
	"""

	maximum: c4gui.Coordinates = get_board_maximums(board)

	directions: [[]] = [[1, 0], [1, -1], [1, 1], [0, 1]]
	for i in directions:
		y_shift: int = i[0]
		x_shift: int = i[1]
		for y in range(maximum.y):
			for x in range(maximum.x):
				last_y: int = y + (3 * y_shift)
				last_x: int = x + (3 * x_shift)
				if 0 <= last_y < maximum.y and 0 <= last_x < maximum.x:
					string: str = board[y][x]
					if string != " " and string == board[y + y_shift][x + x_shift] and string == board[y + 2 * y_shift][x + 2 * x_shift] and string == board[last_y][last_x]:
						return True
	return False


def cpu_algorithm_easy(board: [[]], letter: chr) -> None:
	"""
	Easy Algorithm for CPU player (chooses column randomly)

	letter -- character to place
	"""

	random_choice: int = random.randint(0, 6)
	while True:
		if not check_if_column_full(board, random_choice):
			for i in range(5, -1, -1):
				if board[i][random_choice] == " ":
					board[i][random_choice] = letter
					return
		else:
			random_choice = random.randint(0, 6)
