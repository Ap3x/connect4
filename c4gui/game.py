#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import copy
import math
import pygame

from typing import Dict, Tuple, Callable


class Winner:
	NONE = 1
	P1 = 2
	P2 = 3
	TIE = 4


class GameType:
	SPECTATE = 1
	SINGLE = 2
	DOUBLE = 3
	NETWORK = 4


class Game:
	"""Handles game board rendering and animation."""

	def __init__(self, game_type: int, theme: c4gui.Theme, display_width: int, display_height: int, players: c4gui.Players = c4gui.Players(p1_name="Player 1", p1_color=c4gui.styles.COLOR_RED, p2_name="Player 2", p2_color=c4gui.styles.COLOR_YELLOW)) -> None:
		"""
		Set up board elements

		theme -- A c4gui styling theme
		display_width -- The screen display width
		display_height -- The screen display height
		players -- The Players object containing names and colors of each user
		"""

		# Instantiate an array of boards (rows and columns) with a single blank board
		self.boards = [[[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "],
			[" ", " ", " ", " ", " ", " ", " "]]]

		# Instantiate passed variables
		self.states: list = []
		self.game_type: int = game_type
		self.theme: c4gui.Theme = theme
		self.players: c4gui.Players = players
		self.display_width: int = display_width
		self.display_height: int = display_height
		self.winner: int = Winner.NONE

		# Calculate dimensions
		self.rows: int = len(self.boards[-1])
		self.cols: int = len(self.boards[-1][0]) if self.rows > 0 else 0
		self.top: int = self.display_height * c4gui.styles.PADDING_TOP
		self.tile_size: int = 0

		# Scale everything by the smaller dimension
		self.scale: float = 1
		if display_height - self.top < display_width:
			self.scale = (self.display_height - self.top) / c4gui.styles.BOARD_HEIGHT
		else:
			self.scale = self.display_width / c4gui.styles.BOARD_WIDTH

		# The radius is for any circular token and the tile is rectangle of the surrounding padding
		self.radius: int = int(c4gui.styles.TOKEN_RADIUS * self.scale)
		self.tile_size: int = int((c4gui.styles.GRID_END_X - c4gui.styles.GRID_START_X) * self.scale / self.cols)

		# The board is the entire image
		self.board_width: int = int(c4gui.styles.BOARD_WIDTH * self.scale)
		self.board_height: int = int(c4gui.styles.BOARD_HEIGHT * self.scale)
		self.board_start_x: int = int(self.display_width/2 - self.board_width/2)
		self.board_start_y: int = int((self.display_height + self.top)/2 - self.board_height/2)

		# The grid is the inside part of the image, just for tiles
		self.grid_start_x: int = self.board_start_x + c4gui.styles.GRID_START_X*self.scale
		self.grid_start_y: int = self.board_start_y + c4gui.styles.GRID_START_Y*self.scale
		self.inner_padding: int = int((self.tile_size - self.radius) / 2)

	def set_winner(self, winner: Winner) -> None:
		"""
		Trigger a game end

		winner -- A Winner object
		"""
		self.winner = winner

	def update_board(self, board: [[]]) -> None:
		"""
		Update the board stored in the game object

		board -- the new 2D board array with token positions
		"""

		self.boards.append(board)

	def set_colors(self, p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> None:
		"""
		Set the token colors for each player

		p1 -- The token color for player 1
		p2 -- The token color for player 2
		"""

		self.players.p1_color = p1
		self.players.p2_color = p2

	def get_boards(self) -> [[]]:
		"""Get the 3D board array stored in the game object"""

		return copy.deepcopy(self.boards)

	def get_icon_dimension(self) -> int:
		"""Calculate square icon dimensions based on the window scale"""

		return int(140 * self.scale)

	def draw_turn(self, surface: pygame.Surface, p1turn: bool) -> None:
		"""
		Draw the text description of whose turn it is

		surface -- The pygame surface to draw on
		p1turn -- True if it's player 1's turn; False if it's player 2's turn
		"""
		name = self.players.p1_name if p1turn else self.players.p2_name
		color = self.players.p1_color if p1turn else self.players.p2_color
		surface.blit(c4gui.styles.FONT.render("%s'%s turn" % (name, "" if name[-1] == "s" else "s"), True, color), (10, 10))

	def draw_board(self, surface: pygame.Surface, board: int = -1) -> None:
		"""
		Draw the board onto a surface

		surface -- The pygame surface to draw on
		board -- The board index to display (defaults to the most recent)
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
				if self.boards[board][r][c] == " ":

					# Blank spots get rendered as images through rectangles
					surface.blit(pygame.transform.scale(self.theme.empty, ((self.radius - 1) * 2, (self.radius - 1) * 2)), (int(x + c4gui.styles.SPRITE_SCALE * self.scale), int(y + c4gui.styles.SPRITE_SCALE * self.scale)))

				else:

					# Filled spots get rendered as circles, which require an offset
					pygame.draw.circle(surface, self.players.p1_color if self.boards[board][r][c] == "X" else self.players.p2_color, (int(x + self.tile_size / 2), int(y + self.tile_size / 2)), self.radius)

	def draw_hovering_token(self, surface: pygame.Surface, x_pos: int, color: Tuple[int, int, int]) -> None:
		"""
		Draw the token above the game board onto a surface

		surface -- The pygame surface to draw on
		x_pos -- The horizontal component where the user's mouse is
		color -- The RGB value for the token
		"""
		pygame.draw.circle(surface, color, (x_pos, int(self.tile_size / 2)), self.radius)

	def draw_review_text(self, surface: pygame.Surface, turn: int):
		"""
		Draw the token above the game board onto a surface

		surface -- The pygame surface to draw on
		turn -- The turn number for the reviewed board
		"""

		surface.blit(c4gui.styles.FONT.render("Turn #%d:" % turn, True, self.theme.hover), (10, 10))

	def draw_review_buttons(self, surface: pygame.Surface, buttons: Tuple[str, ...]) -> Dict[str, c4gui.Coordinates]:
		"""
		Draw the review buttons onto a surface

		surface -- The pygame surface to draw on
		buttons -- A list of loadable icons

		Returns a dictionary of button coordinates
		"""

		# Calculate constants and initial horizontal offset
		result = {}
		button_dimension = self.get_icon_dimension()
		offset = self.display_width / 2 - (button_dimension * (len(buttons) * 2 - 1)) / 2

		# Iterate and render items from the list
		for button in buttons:
			result[button] = c4gui.Coordinates(x=offset, y=int(self.display_height - button_dimension))
			surface.blit(pygame.transform.scale(getattr(self.theme.icons, button), (button_dimension, button_dimension)), (result[button].x, result[button].y))
			offset += 2 * button_dimension

		return result

	def draw_highlight_button(self, surface: pygame.Surface, dimension: int, button: str, coordinates: c4gui.Coordinates) -> None:
		"""
		Draw over a button (icon) to highlight it

		surface -- The pygame surface to draw on
		dimension -- The the length of a side of the icon's square
		button -- The sprite to overlay
		coordinates -- The x and y positions of the button start
		"""

		try:
			icon: pygame.image = getattr(self.theme.icons_hover, button)
			if icon is not None:
				surface.blit(pygame.transform.scale(icon, (dimension, dimension)), (coordinates.x, coordinates.y))
		except AttributeError:
			pass

	def draw_exit_button(self, surface: pygame.Surface, hover: bool = False) -> pygame.rect:
		"""
		Draw over a button (icon) to highlight it

		surface -- The pygame surface to draw on
		dimension -- The the length of a side of the icon's square
		button -- The sprite to overlay
		coordinates -- The x and y positions of the button start
		"""

		button_width = 200 * self.scale
		rect = pygame.Rect(self.display_width - button_width - 10, 10, button_width, 80)
		pygame.draw.rect(surface, self.theme.hover if hover else self.theme.button, rect)
		text = c4gui.styles.FONT.render("Exit", True, self.theme.text)
		surface.blit(text, text.get_rect(center=(rect.x + rect.width / 2, rect.y + rect.height / 2)))

		return rect

	def draw_win_status(self, surface: pygame.Surface, winner: int):
		"""
		Draw over a button (icon) to highlight it

		surface -- The pygame surface to draw on
		p1turn -- True if it's player 1's turn; False if it's player 2's turn
		"""

		if winner == Winner.P1:
			color: str = self.players.p1_color
			text = "%s wins!" % self.players.p1_name
		elif winner == Winner.P2:
			color: str = self.players.p2_color
			text = "%s wins!" % self.players.p2_name
		else:
			color: str = c4gui.styles.COLOR_GRAY
			text = "It's a tie!"

		text = c4gui.styles.FONT.render(text, True, color)
		surface.blit(text, (self.display_width / 2 - text.get_width() / 2, 10))

	def render(self, surface: pygame.Surface, clock: pygame.time.Clock, p1turn: bool, move_callback: Callable, end_callback: Callable) -> None:
		"""
		Render all board elements and loop until user interaction

		surface -- The pygame surface to draw on
		clock -- The pygame clock to iteratively refresh
		p1turn -- True if it's player 1's turn; False if it's player 2's turn
		"""

		# Verify parameters
		if not move_callback or not isinstance(move_callback, Callable):
			raise TypeError("invalid move callback")

		if not end_callback or not isinstance(end_callback, Callable):
			raise TypeError("invalid game end callback")

		# Draw the first blank
		self.draw_board(surface)
		self.draw_turn(surface, p1turn)
		pygame.display.flip()

		# Loop until a user triggers callback or the game ends
		while self.winner == Winner.NONE:

			# Handle and remove all events from the pygame queue from the last tick
			for event in pygame.event.get():

				# Redraw the board
				self.draw_board(surface)
				self.draw_turn(surface, p1turn)

				# check for SIGINT
				c4gui.helpers.check_sigint(event)

				if event.type == pygame.MOUSEMOTION:

					# Draw the x position of the mouse for a token hover effect
					self.draw_hovering_token(surface, event.pos[0], self.players.p1_color if p1turn else self.players.p2_color)

				elif event.type == pygame.MOUSEBUTTONDOWN:

					# Check if the mouse clicked within a tile relative to the valid list of columns
					column: int = math.floor((event.pos[0] - self.grid_start_x) / self.tile_size)
					if column in range(self.cols) and move_callback(self, p1turn, column):

						# The move was legal; switch turns and continue
						c4gui.sfx.play("token_drop")
						p1turn = not p1turn

					else:

						# The move was illegal; render as normal
						c4gui.sfx.play("invalid")
						self.draw_hovering_token(surface, event.pos[0], self.players.p1_color if p1turn else self.players.p2_color)

			# Render the whole screen
			pygame.display.flip()
			clock.tick(20)

		# Set up the game over / review state
		max_board_num = len(self.boards) - 1
		current_board_num = max_board_num
		nav_buttons = (("nav_first", -2),
						("nav_prev", -1),
						("nav_nonce", 0),
						("nav_next", 1),
						("nav_last", 2))
		button_dimension = self.get_icon_dimension()

		play_sound: bool = True
		exit_game: bool = False
		while not exit_game:

			# Handle and remove all events from the pygame queue from the last tick
			for event in pygame.event.get():

				# Redraw the board
				self.draw_board(surface, current_board_num)

				# Redraw review features
				self.draw_review_text(surface, current_board_num)
				self.draw_win_status(surface, self.winner)
				nav_buttons_pos = self.draw_review_buttons(surface, tuple([x[0] for x in nav_buttons]))
				exit_button = self.draw_exit_button(surface)

				if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:

					# Handle navigation buttons
					for button in nav_buttons_pos.keys():
						if pygame.Rect(nav_buttons_pos[button].x, nav_buttons_pos[button].y, button_dimension, button_dimension).collidepoint(event.pos):

							# Highlight if hovered over
							self.draw_highlight_button(surface, button_dimension, button, nav_buttons_pos[button])

							if event.type == pygame.MOUSEBUTTONDOWN:

								# Change the board number if clicked
								direction = int(dict(nav_buttons)[button])
								if direction == 0:
									continue
								if direction == -2:
									current_board_num = 0
									c4gui.sfx.play("special")
								elif direction == -1:
									current_board_num = 0 if current_board_num < 1 else current_board_num - 1
									c4gui.sfx.play("down")
								elif direction == 1:
									current_board_num = max_board_num if current_board_num > max_board_num - 1 else current_board_num + 1
									c4gui.sfx.play("up")
								elif direction == 2:
									current_board_num = max_board_num
									c4gui.sfx.play("special")

					# Check exit button events
					if exit_button.collidepoint(event.pos[0], event.pos[1]):
						if event.type == pygame.MOUSEMOTION:
							self.draw_exit_button(surface, True)
						elif event.type == pygame.MOUSEBUTTONDOWN:
							end_callback()
							exit_game = True
							break

				# Render the whole screen
				pygame.display.flip()
				clock.tick(20)

				# Play a game end sound after the first render
				if play_sound:
					if self.winner == Winner.P1 or self.winner == Winner.P2:
						c4gui.sfx.play("win")
					elif self.winner == Winner.TIE:
						c4gui.sfx.play("tie")
					pygame.time.delay(2500)
					play_sound = False
