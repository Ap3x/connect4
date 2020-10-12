#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import math
import pygame
import sys
from typing import Tuple, Callable


class Game:
	"""Handles game board rendering and animation."""

	def __init__(self, theme: c4gui.Theme, display_width: int, display_height: int, players: c4gui.Players = c4gui.Players(p1_name="Player 1", p1_color=c4gui.styles.COLOR_RED, p2_name="Player 2", p2_color=c4gui.styles.COLOR_YELLOW)) -> None:
		"""
		Set up board elements

		theme -- A c4gui styling theme
		display_width -- The screen display width
		display_height -- The screen display height
		players -- The Players object containing names and colors of each user
		"""

		# Instantiate passed variables
		self.board = [[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "]]
		self.theme = theme
		self.players = players
		self.display_width = display_width
		self.display_height = display_height

		# Calculate dimensions
		self.rows = len(self.board)
		self.cols = len(self.board[0]) if self.rows > 0 else 0
		self.top = self.display_height * c4gui.styles.PADDING_TOP
		self.tile_size = 0

		# Scale everything by the smaller dimension
		self.scale = 1
		if display_height - self.top < display_width:
			self.scale = (self.display_height - self.top) / c4gui.styles.BOARD_HEIGHT
		else:
			self.scale = self.display_width / c4gui.styles.BOARD_WIDTH

		# The radius is for any circular token and the tile is rectangle of the surrounding padding
		self.radius = int(c4gui.styles.TOKEN_RADIUS * self.scale)
		self.tile_size = int((c4gui.styles.GRID_END_X - c4gui.styles.GRID_START_X) * self.scale / self.cols)

		# The board is the entire image
		self.board_width = int(c4gui.styles.BOARD_WIDTH * self.scale)
		self.board_height = int(c4gui.styles.BOARD_HEIGHT * self.scale)
		self.board_start_x = int(self.display_width/2 - self.board_width/2)
		self.board_start_y = int((self.display_height + self.top)/2 - self.board_height/2)

		# The grid is the inside part of the image, just for tiles
		self.grid_start_x = self.board_start_x + c4gui.styles.GRID_START_X*self.scale
		self.grid_start_y = self.board_start_y + c4gui.styles.GRID_START_Y*self.scale
		self.inner_padding = (self.tile_size - self.radius) / 2

		# Finally, button color defaults
		self.p1 = c4gui.styles.COLOR_RED
		self.p2 = c4gui.styles.COLOR_YELLOW

	def update_board(self, board: [[]]) -> None:
		"""
		Update the board stored in the game object

		board -- the new 2D board array with token positions
		"""

		self.board = board

	def set_colors(self, p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> None:
		"""
		Set the token colors for each player

		p1 -- The token color for player 1
		p2 -- The token color for player 2
		"""

		self.p1 = p1
		self.p2 = p2

	def get_board(self) -> [[]]:
		"""Get the 3D board array stored in the game object"""

		return self.board

	def draw_turn(self, surface: pygame.Surface, p1turn: bool) -> None:
		"""
		Draw the text description of whose turn it is

		surface -- The pygame surface to draw on
		p1turn -- True if it's player 1's turn; False if it's player 2's turn
		"""
		name = self.players.p1_name if p1turn else self.players.p2_name
		color = self.players.p1_color if p1turn else self.players.p2_color
		surface.blit(c4gui.styles.FONT.render("%s'%s turn" % (name, "" if name[-1] == "s" else "s"), True, color), (0, 0, 100, 100))

	def draw_board(self, surface: pygame.Surface) -> None:
		"""
		Draw the board onto a surface

		surface -- The pygame surface to draw on
		"""

		# Render the background
		surface.fill(self.theme.background)
		pygame.draw.ellipse(surface, self.theme.shadow, (0, int(self.display_height * 0.8), self.display_width, int(self.display_height * 0.4)))
		surface.blit(pygame.transform.scale(self.theme.board, (self.board_width, self.board_height)), (self.board_start_x, self.board_start_y))

		# Render each cell
		for c in range(self.cols):
			for r in range(self.rows):
				x = self.grid_start_x + c * self.tile_size + c4gui.styles.X_STRETCH * c
				y = self.grid_start_y + r * self.tile_size + c4gui.styles.Y_STRETCH * r
				if self.board[r][c] == " ":

					# Blank spots get rendered as images through rectangles
					surface.blit(pygame.transform.scale(self.theme.empty, ((self.radius - 1) * 2, (self.radius - 1) * 2)), (int(x + c4gui.styles.SPRITE_SCALE * self.scale), int(y + c4gui.styles.SPRITE_SCALE * self.scale)))

				else:

					# Filled spots get rendered as circles, which require an offset
					pygame.draw.circle(surface, self.p1 if self.board[r][c] == "X" else self.p2, (int(x + self.tile_size / 2), int(y + self.tile_size / 2)), self.radius)

	def draw_hovering_token(self, surface: pygame.Surface, x_pos: int, color: Tuple[int, int, int]) -> None:
		"""
		Draw the token above the game board onto a surface

		surface -- The pygame surface to draw on
		"""
		pygame.draw.circle(surface, color, (x_pos, int(self.tile_size / 2)), self.radius)

	def render(self, surface: pygame.Surface, clock: pygame.time.Clock, p1turn: bool, move_callback: Callable) -> None:
		"""
		Render all board elements and loop until user interaction

		surface -- The pygame surface to draw on
		clock -- The pygame clock to iteratively refresh
		p1turn -- True if it's player 1's turn; False if it's player 2's turn
		"""

		# Verify parameters
		if not move_callback or not isinstance(move_callback, Callable):
			raise TypeError("invalid move callback")

		# Draw the first blank
		self.draw_board(surface)
		self.draw_turn(surface, p1turn)
		pygame.display.flip()

		# Loop until a user triggers callback
		while True:

			# Handle and remove all events from the pygame queue from the last tick
			for event in pygame.event.get():

				# Redraw the board
				self.draw_board(surface)
				self.draw_turn(surface, p1turn)

				pressed = pygame.key.get_pressed()
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or (pressed[pygame.K_LALT] or pressed[pygame.K_RALT]) and event.key == pygame.K_F4):

					# Gracefully exit when the system sends SIGINT
					pygame.quit()
					sys.exit()

				elif event.type == pygame.MOUSEMOTION:

					# Draw the x position of the mouse for a token hover effect
					self.draw_hovering_token(surface, event.pos[0], self.p1 if p1turn else self.p2)

				elif event.type == pygame.MOUSEBUTTONDOWN:

					# Check if the mouse clicked within a tile relative to the valid list of columns
					column: int = math.floor((event.pos[0] - self.grid_start_x) / self.tile_size)
					if column in range(self.cols) and move_callback(self, p1turn, column):

						# The move was legal; switch turns and continue
						p1turn = not p1turn

					else:

						# The move was illegal; render as normal
						self.draw_hovering_token(surface, event.pos[0], self.p1 if p1turn else self.p2)

			# Render the whole screen
			pygame.display.flip()
			clock.tick(200)
