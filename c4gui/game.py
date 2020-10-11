#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import pygame
import sys
from typing import Tuple


class Game:
	"""Handles game board rendering and animation."""

	def __init__(self, theme: c4gui.Theme, display_width: int, display_height: int) -> None:
		"""
		Set up board elements

		theme -- A c4gui styling theme
		display_width -- The screen display width
		display_height -- The screen display height
		"""

		# Instantiate passed variables
		self.board = [[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "]]
		self.theme = theme
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
					surface.blit(pygame.transform.scale(self.theme.empty, ((self.radius - 1) * 2, (self.radius - 1) * 2)), ( int(x + c4gui.styles.SPRITE_SCALE * self.scale), int(y + c4gui.styles.SPRITE_SCALE * self.scale)))

				else:

					# Filled spots get rendered as circles, which require an offset
					pygame.draw.circle(surface, self.p1 if self.board[r][c] == "X" else self.p2, (int(x + self.tile_size / 2), int(y + self.tile_size / 2)), self.radius)

	def render(self, surface: pygame.Surface, clock: pygame.time.Clock, p1turn: bool) -> None:
		"""
		Render all board elements and loop until user interaction

		surface -- The pygame surface to draw on
		clock -- The pygame clock to iteratively refresh
		p1turn -- True if it's player 1's turn; False if it's player 2's turn
		"""

		# Draw the first blank
		self.draw_board(surface)
		pygame.display.flip()

		# Loop until a user triggers callback
		while True:

			# Handle and remove all events from the pygame queue from the last tick
			for event in pygame.event.get():

				# Redraw the board
				self.draw_board(surface)

				pressed = pygame.key.get_pressed()
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or (pressed[pygame.K_LALT] or pressed[pygame.K_RALT]) and event.key == pygame.K_F4):

					# Gracefully exit when the system sends SIGINT
					pygame.quit()
					sys.exit()

				elif event.type == pygame.MOUSEMOTION:

					# Check if the mouse is within any button rectangle for button hover effect
					pygame.draw.circle(surface, self.p1 if p1turn else self.p2, (event.pos[0], int(self.tile_size / 2)), self.radius)

				elif event.type == pygame.MOUSEBUTTONDOWN:

					# Check if the mouse clicked within any button rectangle for callback execution
					# TODO - handle events here
					pass

			# Render the whole screen
			pygame.display.flip()
			clock.tick(200)
