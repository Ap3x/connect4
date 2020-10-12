#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui


def get_board_maximums(board: [[]]) -> c4gui.Coordinates:
	max_y: int = len(board)
	max_x: int = len(board[0]) if max_y > 0 else 0
	return c4gui.Coordinates(max_x, max_y)


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
		x_shift: int = i[0]
		y_shift: int = i[1]
		for x in range(0, maximum.x-1, 1):
			for y in range(0, maximum.y-1, 1):
				last_x: int = x + (3*x_shift)
				last_y: int = y + (3*y_shift)
				if 0 <= last_x < maximum.x-1 and 0 <= last_y < maximum.y-1:
					string: str = board[x][y]
					if string != " " and string == board[x+x_shift][y+y_shift] and string == board[x+2*x_shift][y+2*y_shift] and string == board[last_x][last_y]:
						return True
	return False

