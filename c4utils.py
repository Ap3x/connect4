#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import random
import copy


class Node:
	"""Node object in c4utils hard algorithm move tree"""
	score: int
	alpha: int = -99999
	beta: int = 99999
	depth: int
	board_state: [[]]

	def __init__(self):
		self.children = []

	def set(self, s: int, d: int):
		self.score = s
		self.depth = d
		self.children = []


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

	for i in range(len(board) + 1):
		if not check_if_column_full(board, i):
			return False
	return True


def check_win(board: [[]]) -> bool:
	"""
	Check if a player has achieved 4 in a row

	board -- the 2D game board
	"""

	directions: [[]] = [[1, 0], [1, -1], [1, 1], [0, 1]]
	for i in directions:
		y_shift: int = i[0]
		x_shift: int = i[1]
		for y in range(c4gui.MAX_ROWS):
			for x in range(c4gui.MAX_COLS):
				last_y: int = y + (3 * y_shift)
				last_x: int = x + (3 * x_shift)
				if 0 <= last_y < c4gui.MAX_ROWS and 0 <= last_x < c4gui.MAX_COLS:
					string: str = board[y][x]
					if string != " " and string == board[y + y_shift][x + x_shift] and string == board[y + 2 * y_shift][
						x + 2 * x_shift] and string == board[last_y][last_x]:
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


def cpu_algorithm_hard(board: [[]], letter: chr, depth: int) -> None:
	"""
	Hard Algorithm for CPU player

	letter -- character to place
	depth -- search depth for how many future moves to calculate
	"""

	# Store move letter for opponent
	opponent = "O" if letter == "X" else "X"

	def evaluate_board(tmp: [[]], letter: chr) -> int:
		"""
		Evaluate board state
		Calculates score of board state from number of chains each side has
		Increased score per chain based on chain size
		"""

		count_good: int = 0
		count_bad: int = 0
		direction: [[]] = [[0, -1], [0, 1], [-1, 0], [-1, -1], [-1, 1], [1, 0], [1, -1], [1, 1]]

		for y in range(0, c4gui.MAX_ROWS):

			for x in range(0, c4gui.MAX_COLS):

				if tmp[y][x] == letter:
					for i in direction:
						y_shift = i[0]
						x_shift = i[1]

						# If 2 in a row
						if 0 <= y + y_shift < c4gui.MAX_ROWS and 0 <= x + x_shift < c4gui.MAX_COLS and tmp[y + y_shift][x + x_shift] == letter:
							count_good += 2

							# If 3 in a row
							if 0 <= y + 2 * y_shift < c4gui.MAX_ROWS and 0 <= x + 2 * x_shift < c4gui.MAX_COLS and tmp[y + 2 * y_shift][x + 2 * x_shift] == letter:
								count_good += 9

								# If 4 in a row
								if 0 <= y + 3 * y_shift < c4gui.MAX_ROWS and 0 <= x + 3 * x_shift < c4gui.MAX_COLS and tmp[y + 3 * y_shift][x + 3 * x_shift] == letter:
									count_good += 1000

				if tmp[y][x] == opponent:
					for i in direction:
						y_shift = i[0]
						x_shift = i[1]

						# If 2 in a row for opponent
						if 0 <= y + y_shift < c4gui.MAX_ROWS and 0 <= x + x_shift < c4gui.MAX_COLS and tmp[y + y_shift][
							x + x_shift] == opponent:
							count_bad += 4

							# If 3 in a row for opponent
							if 0 <= y + 2 * y_shift < c4gui.MAX_ROWS and 0 <= x + 2 * x_shift < c4gui.MAX_COLS and tmp[y + 2 * y_shift][x + 2 * x_shift] == opponent:
								count_bad += 9

								# If 4 in a row for opponent
								if 0 <= y + 3 * y_shift < c4gui.MAX_ROWS and 0 <= x + 3 * x_shift < c4gui.MAX_COLS and tmp[y + 3 * y_shift][x + 3 * x_shift] == opponent:
									count_bad += 9999

		return count_good - count_bad

	def a_b_pruning(node: Node) -> None:
		"""
		Recursive alpha beta pruning method

		node -- Board object thats apart of game tree. Initially passed root node. 
		"""

		# Pruning check
		if node.alpha < node.beta:

			# Traverse to leaf depth - 1
			if node.depth < depth - 1:
				if node.depth % 2 == 0:

					# Root node has no parent
					if node.depth == 0:
						for i in range(len(node.children)):
							node.children[i].alpha = node.alpha
							node.children[i].beta = node.beta
							a_b_pruning(node.children[i])

					# Max level
					else:
						for i in range(len(node.children)):
							node.children[i].alpha = node.alpha
							node.children[i].beta = node.beta
							a_b_pruning(node.children[i])
							if node.children[i].beta > node.alpha:
								node.alpha = node.children[i].beta

				# Min level
				elif node.depth % 2 == 1:
					for i in range(len(node.children)):
						node.children[i].alpha = node.alpha
						node.children[i].beta = node.beta
						a_b_pruning(node.children[i])
						if node.children[i].alpha < node.beta:
							node.beta = node.children[i].alpha

			# Evaluating each child for min or max
			for child in node.children:

				# Min level
				if child.depth % 2 == 0:
					if child.alpha < node.beta:
						node.beta = child.alpha
				elif child.depth % 2 == 1:
					if child.beta > node.alpha:
						node.alpha = child.beta

	# Begin function execution
	move_tree: list = []
	tmp_score: int
	tmp_board = copy.deepcopy(board)
	original_board = copy.deepcopy(board)

	# Create game tree for all possible moves
	root: Node = Node()
	root.depth = 0
	root.score = evaluate_board(tmp_board, letter)
	root.board_state = copy.deepcopy(original_board)
	move_tree.append(root)

	# Find remaining moves for given depth
	for item in move_tree:
		if item.depth < depth:

			# Store all possible moves
			for x in range(c4gui.MAX_COLS):

				if not check_if_column_full(board, x):
					for y in range(5, -1, -1):
						if item.board_state[y][x] == " ":
							if item.depth % 2 == 0:
								player = letter
							else:
								player = opponent

							# Candidate move found, store move
							item.board_state[y][x] = player
							tmp_node: Node = Node()
							tmp_node.depth = item.depth + 1
							tmp_node.board_state = copy.deepcopy(item.board_state)
							tmp_node.parent = item

							# Check for immediate win and terminate if found
							if tmp_node.depth == 1 and check_win(tmp_node.board_state):
								board[y][x] = letter
								return

							item.board_state[y][x] = ' '
							move_tree.append(tmp_node)
							item.children.append(tmp_node)
							break

	# Set alpha beta for leaf nodes
	for i in reversed(range(len(move_tree))):
		if move_tree[i].depth == depth:
			move_tree[i].score = evaluate_board(move_tree[i].board_state, letter)
			move_tree[i].alpha = move_tree[i].score
			move_tree[i].beta = move_tree[i].score
		else:
			break

	# Determine best move
	a_b_pruning(move_tree[0])
	minimum = -99999
	best: Node = Node()
	for child in move_tree[0].children:
		if child.beta >= minimum:
			minimum = child.beta
			best = child

	for i in range(c4gui.MAX_COLS):
		for j in range(c4gui.MAX_ROWS):
			if not best.board_state[j][i] == board[j][i]:
				board[j][i] = letter
