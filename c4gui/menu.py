#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import network
import pygame
import pygame_gui
import server
import socket
from typing import Callable


class SubMenu:
	MAIN = 1
	LOCAL = 2
	SINGLE = 3
	DOUBLE = 4
	SPECTATE = 5
	NETWORK = 6
	HOST = 7
	JOIN = 8
	HOST_LOBBY = 9
	JOIN_LOBBY = 10


def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]


class Menu:
	"""Handles menu creation, animation, and alteration."""

	def __init__(self, display_width: int, display_height: int, submenu: int, game_callback: Callable) -> None:
		"""
		Set up menu elements
		
		display_width -- The screen display width
		display_height -- The screen display height
		submenu -- The specific menu to render on initialization
		game_callback -- The callable for a game start event
		"""

		# Instantiate passed variables
		self.theme = c4gui.config.get("Global", "theme", c4gui.Theme)
		self.sound = c4gui.config.get("Global", "sfx_enabled", bool)
		self.display_width = display_width
		self.display_height = display_height
		self.submenu = submenu
		self.manager = None
		self.reload_manager()
		self.game_callback = game_callback
		self.element_values = {}
		self.network = None
		self.network_data = None
		self.server_started = False

	def reload_manager(self):
		self.manager = pygame_gui.UIManager((self.display_width, self.display_height), self.theme.gui_ext)
		self.generate()

	def generate(self) -> None:
		"""
		Generate the button elements for the menu
		
		menu_type - The sub-menu to display
		"""

		# Declare constants
		button_width: int = int(self.display_width / 3)
		button_height: int = 80
		v_offset: int = int(self.display_height / 2)
		h_offset: int = -200
		padding: int = 20
		horizontal_middle: int = int(self.display_width / 2 - button_width / 2)
		color_list = [x for x in c4gui.styles.get_all_color_names() if x not in ["Black", "White", "Dark Gray"]]

		# Clear the surface
		self.manager.clear_and_reset()

		# Switch cases for all possible menus
		if self.submenu == SubMenu.MAIN:

			"""
			Main Menu
			
			[Button] Local Game
			[Button] Network Game
			[Button] Quit
			"""
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset), (button_width, button_height)),
												   text="Local Game",
												   object_id="call_menu_local")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + button_height + padding), (button_width, button_height)),
												   text="Network Game",
												   object_id="call_menu_network")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Quit",
												   object_id="quit")

		elif self.submenu == SubMenu.LOCAL:

			"""
			Local Game Menu

			[Button] 1 Player
			[Button] 2 Player
			[Button] Spectate
			[Button] Back
			"""
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset), (button_width, button_height)),
												   text="1-Player",
												   object_id="call_menu_single")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + button_height + padding), (button_width, button_height)),
												   text="2-Player",
												   object_id="call_menu_double")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												   text="Spectate",
												   object_id="call_menu_spectate")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_main")

		elif self.submenu == SubMenu.SINGLE:

			"""
			1 Player Menu

			[Option] P1 Name & Color
			[Option] CPU0 Difficulty
			[Button] Start Game
			[Button] Back
			"""

			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - 2 * (button_height + padding)), (200, button_height)),
												 text="Player")
			pygame_gui.elements.ui_text_entry_line.UITextEntryLine(manager=self.manager,
																   relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - 2 * (button_height + padding) + 18), (200, 40)),
																   object_id="set_player1_name").set_text(c4gui.config.get("Player1", "name", str))
			pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(manager=self.manager,
																 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset + 300), v_offset - 2 * (button_height + padding) + 25), (200, 40)),
																 options_list=color_list,
																 starting_option=c4gui.styles.get_color_name_from_tuple(c4gui.config.get("Player1", "color", tuple)),
																 object_id="set_player1_color")
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (180 + padding) + h_offset), v_offset - (button_height + padding)), (200, button_height)),
												 text="AI Difficulty")
			start_value = c4gui.config.get("Computer0", "difficulty", int)
			pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(manager=self.manager,
																		relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - button_height), (500, 50)),
																		start_value=start_value,
																		value_range=(1, 10),
																		object_id="set_cpu0")
			self.element_values["cpu0"] = pygame_gui.elements.ui_label.UILabel(manager=self.manager,
																			   relative_rect=pygame.Rect((int(self.display_width / 2 + 500 + padding + h_offset), v_offset - button_height), (200, 50)),
																			   text=str(start_value))
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												   text="Start",
												   object_id="call_game_single")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_local")

		elif self.submenu == SubMenu.DOUBLE:

			"""
			2 Player Menu

			[Option] P1 Name & Color
			[Option] P2 Name & Color
			[Button] Start Game
			[Button] Back
			"""
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - 2 * (button_height + padding)), (200, button_height)),
												 text="Player 1")
			pygame_gui.elements.ui_text_entry_line.UITextEntryLine(manager=self.manager,
																   relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - 2 * (button_height + padding) + 18), (200, 40)),
																   object_id="set_player1_name").set_text(c4gui.config.get("Player1", "name", str))
			pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(manager=self.manager,
																 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset + 300), v_offset - 2 * (button_height + padding) + 25), (200, 40)),
																 options_list=color_list,
																 starting_option=c4gui.styles.get_color_name_from_tuple(c4gui.config.get("Player1", "color", tuple)),
																 object_id="set_player1_color")
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - (button_height + padding)), (200, button_height)),
												 text="Player 2")
			pygame_gui.elements.ui_text_entry_line.UITextEntryLine(manager=self.manager,
																   relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - (button_height + padding) + 18), (200, 40)),
																   object_id="set_player2_name").set_text(c4gui.config.get("Player2", "name", str))
			pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(manager=self.manager,
																 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset + 300), v_offset - (button_height + padding) + 25), (200, 40)),
																 options_list=color_list,
																 starting_option=c4gui.styles.get_color_name_from_tuple(c4gui.config.get("Player2", "color", tuple)),
																 object_id="set_player2_color")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												   text="Start",
												   object_id="call_game_double")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_local")

		elif self.submenu == SubMenu.SPECTATE:

			"""
			Spectate Menu

			[Option] CPU1 Difficulty
			[Option] CPU2 Difficulty
			[Button] Start Game
			[Button] Back
			"""
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (200 + padding) + h_offset), v_offset - (button_height + padding)), (220, button_height)),
												 text="CPU 1 Difficulty")
			start_value = c4gui.config.get("Computer1", "difficulty", int)
			pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(manager=self.manager,
																		relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - (button_height + padding) + 12), (500, 50)),
																		start_value=start_value,
																		value_range=(1, 10),
																		object_id="set_cpu1")
			self.element_values["cpu1"] = pygame_gui.elements.ui_label.UILabel(manager=self.manager,
																			   relative_rect=pygame.Rect((int(self.display_width / 2 + 500 + padding + h_offset), v_offset - (button_height + padding)), (200, 50)),
																			   text=str(start_value))
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (200 + padding) + h_offset), v_offset), (220, button_height)),
												 text="CPU 2 Difficulty")
			start_value = c4gui.config.get("Computer2", "difficulty", int)
			pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(manager=self.manager,
																		relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset + 12), (500, 50)),
																		start_value=start_value,
																		value_range=(1, 10),
																		object_id="set_cpu2")
			self.element_values["cpu2"] = pygame_gui.elements.ui_label.UILabel(manager=self.manager,
																			   relative_rect=pygame.Rect((int(self.display_width / 2 + 500 + padding + h_offset), v_offset), (200, 50)),
																			   text=str(start_value))
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												   text="Start",
												   object_id="call_game_spectate")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_local")

		elif self.submenu == SubMenu.NETWORK:

			"""
			Network Menu

			[Button] Host Game
			[Button] Join Game
			[Button] Back
			"""
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset), (button_width, button_height)),
												   text="Host Game",
												   object_id="call_menu_host")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + button_height + padding), (button_width, button_height)),
												   text="Join Game",
												   object_id="call_menu_join")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_main")

		elif self.submenu == SubMenu.HOST:

			"""
			Host Menu
	
			[Option] IP
			[Option] Port
			[Button] Back
			"""
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - (button_height + padding)), (200, button_height)),
												 text="Interface")
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - (button_height + padding) + 18), (200, 42)),
												 text=get_ip_address())
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset), (200, button_height)),
												 text="Port")
			pygame_gui.elements.ui_text_entry_line.UITextEntryLine(manager=self.manager,
																   relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset + 18), (200, 40)),
																   object_id="set_host_port").set_text(c4gui.config.get("Network", "host_port", str))
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												   text="Begin Listening",
												   object_id="call_lobby_host")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_network")

		elif self.submenu == SubMenu.JOIN:

			"""
			Join Menu

			[Option] Connection
			[Button] Back
			"""
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - (button_height + padding)), (200, button_height)),
												 text="Host Address")
			pygame_gui.elements.ui_text_entry_line.UITextEntryLine(manager=self.manager,
																   relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset + 50), v_offset - (button_height + padding) + 18), (450, 40)),
																   object_id="set_connection").set_text(c4gui.config.get("Network", "last_connection", str))
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												   text="Join",
												   object_id="call_lobby_join")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_network")

		elif self.submenu == SubMenu.HOST_LOBBY:

			"""
			Network Lobby Menu (Post-Connect)

			[Option] P1 Name & Color
			[Text] P2 Name & Color
			[Button] Start Game
			[Button] Back
			"""
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - 2 * (button_height + padding)), (200, button_height)),
												 text="You")
			pygame_gui.elements.ui_text_entry_line.UITextEntryLine(manager=self.manager,
																   relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - 2 * (button_height + padding) + 18), (200, 40)),
																   object_id="set_player1_name").set_text(c4gui.config.get("Player1", "name", str))
			pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(manager=self.manager,
																 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset + 300), v_offset - 2 * (button_height + padding) + 25), (200, 40)),
																 options_list=color_list,
																 starting_option=c4gui.styles.get_color_name_from_tuple(c4gui.config.get("Player1", "color", tuple)),
																 object_id="set_player1_color")
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((0, v_offset - (button_height + padding)), (int(self.display_width), button_height)),
												 text="Waiting for player..." if self.network_data is None else ("[" + self.network_data[1] + "] " + self.network_data[0]))
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - (button_height + padding)), (200, button_height)),
												 text="Opponent")
			if self.network_data is not None:
				pygame_gui.elements.ui_button.UIButton(manager=self.manager,
													   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
													   text="Start Game",
													   object_id="call_game_host")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_host")

		elif self.submenu == SubMenu.JOIN_LOBBY:

			"""
			Network Lobby Menu (Post-Connect)

			[Option] P2 Name & Color
			[Text] P1 Name & Color
			[Button] Start Game
			[Button] Back
			"""
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - 2 * (button_height + padding)), (200, button_height)),
												 text="You")
			pygame_gui.elements.ui_text_entry_line.UITextEntryLine(manager=self.manager,
																   relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - 2 * (button_height + padding) + 18), (200, 40)),
																   object_id="set_player1_name").set_text(c4gui.config.get("Player1", "name", str))
			pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(manager=self.manager,
																 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset + 300), v_offset - 2 * (button_height + padding) + 25), (200, 40)),
																 options_list=color_list,
																 starting_option=c4gui.styles.get_color_name_from_tuple(c4gui.config.get("Player1", "color", tuple)),
																 object_id="set_player1_color")
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((0, v_offset - (button_height + padding)), (int(self.display_width), button_height)),
												 text="Waiting for player..." if self.network_data is None else ("[" + self.network_data[1] + "] " + self.network_data[0]))
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (150 + padding) + h_offset), v_offset - (button_height + padding)), (200, button_height)),
												 text="Opponent")
			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												 text="Waiting for host to start the game...")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Cancel",
												   object_id="call_menu_join")

		else:
			raise IndexError("undefined submenu called")

	def get_font(self, data: str) -> pygame.font:
		"""
		Return a font object according to the menu theme
		
		data - The plain text to be formatted
		"""

		return c4gui.styles.FONT.render(data, True, self.theme.text)

	def set_theme(self, theme: c4gui.Theme) -> None:
		"""
		Set the menu theme

		theme -- A c4gui styling theme
		"""

		self.theme = theme

	def set_sound(self, enabled: bool) -> None:
		"""
		Set the menu theme

		enabled -- True if sound is enabled; False if sound is disabled
		"""

		self.sound = enabled

	def toggle_theme(self) -> None:
		"""Toggle between LIGHT and DARK themes"""

		# Toggle the theme
		if self.theme == c4gui.styles.THEME_LIGHT:
			self.set_theme(c4gui.styles.THEME_DARK)
			c4gui.config.set("Global", "theme", "THEME_DARK")
		else:
			self.set_theme(c4gui.styles.THEME_LIGHT)
			c4gui.config.set("Global", "theme", "THEME_LIGHT")
		self.reload_manager()

	def toggle_sound(self) -> None:
		"""Toggle between enabled and disabled sound"""

		# Toggle the sound setting
		if self.sound:
			self.set_sound(False)
			c4gui.config.set("Global", "sfx_enabled", False)
		else:
			self.set_sound(True)
			c4gui.config.set("Global", "sfx_enabled", True)

	def send_network_data(self, command: str = "") -> None:
		"""Send player name and color over the network"""

		if self.network is not None:
			if command == "":
				self.network.send((c4gui.config.get("Player1", "name", str), c4gui.styles.get_color_name_from_tuple(c4gui.config.get("Player1", "color", tuple))))
			else:
				self.network.send(command)

	def render(self, surface: pygame.Surface, clock: pygame.time.Clock) -> None:
		"""
		Render all menu elements and loop until user interaction
		
		surface -- The pygame surface to draw on
		clock -- The pygame clock to iteratively refresh
		"""

		# Center the logo horizontally and pad from the top
		logo_x = self.display_width / 2 - self.theme.logo.get_size()[0] / 2
		logo_y = 100

		# Set special button boundaries
		theme_button = pygame.Rect(self.display_width - 60, 10, 50, 50)
		sound_button = pygame.Rect(self.display_width - 60, 60, 50, 50)

		# Loop until a user triggers callback
		while True:

			time_delta = clock.tick(60) / 1000.0

			# Handle network events
			if self.network is not None:

				# Check network queue
				network_data = self.network.receive()
				if network_data is not None:

					# Send player info for the first time
					if self.network_data is None:
						self.send_network_data()

					# Handle special network cases
					if network_data == "DISCONNECT":
						self.network_data = None
					elif network_data == "START":
						self.send_network_data()
						self.game_callback(self, c4gui.game.GameType.JOIN,self.network)
					else:
						self.network_data = network_data

					self.generate()

			# Handle and remove all events from the pygame queue from the last tick
			# https://github.com/pygame/pygame/blob/e40d00db1f8015e8f37624f83a0bd334547cd8dc/docs/reST/ref/event.rst
			for event in pygame.event.get():

				# check for SIGINT
				c4gui.check_sigint(event)

				# Handle custom fields
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == c4gui.Mouse.LEFT:

					# Check if the mouse clicked the theme button
					if theme_button.collidepoint(event.pos[0], event.pos[1]):
						self.toggle_theme()
						c4gui.sfx.play("toggle")

					# Check if the mouse clicked the sound button
					if sound_button.collidepoint(event.pos[0], event.pos[1]):
						self.toggle_sound()
						c4gui.sfx.play("toggle")

				# Handle menu elements
				elif event.type == pygame.USEREVENT:

					if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:

						if "set_cpu0" in event.ui_element.object_ids:
							if self.element_values["cpu0"].text != str(event.value):
								self.element_values["cpu0"].set_text(str(event.value))
								c4gui.config.set("Computer0", "difficulty", int(event.value))
								c4gui.sfx.play("tick")
						elif "set_cpu1" in event.ui_element.object_ids:
							if self.element_values["cpu1"].text != str(event.value):
								self.element_values["cpu1"].set_text(str(event.value))
								c4gui.config.set("Computer1", "difficulty", int(event.value))
								c4gui.sfx.play("tick")
						elif "set_cpu2" in event.ui_element.object_ids:
							if self.element_values["cpu2"].text != str(event.value):
								self.element_values["cpu2"].set_text(str(event.value))
								c4gui.config.set("Computer2", "difficulty", int(event.value))
								c4gui.sfx.play("tick")

					elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:

						if "set_player1_name" in event.ui_element.object_ids:
							c4gui.config.set("Player1", "name", event.text)
							self.send_network_data()
						elif "set_player2_name" in event.ui_element.object_ids:
							c4gui.config.set("Player2", "name", event.text)
						elif "set_host_port" in event.ui_element.object_ids:
							c4gui.config.set("Network", "host_port", event.text)
						elif "set_connection" in event.ui_element.object_ids:
							c4gui.config.set("Network", "last_connection", event.text)

					elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:

						if "set_player1_color" in event.ui_element.object_ids:
							c4gui.config.set("Player1", "color", c4gui.styles.get_color_from_name(event.text))
							self.send_network_data()
						elif "set_player2_color" in event.ui_element.object_ids:
							c4gui.config.set("Player2", "color", c4gui.styles.get_color_from_name(event.text))

					elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:

						c4gui.sfx.play("click")
						regenerate: bool = True

						# Quit case
						if "quit" in event.ui_element.object_ids:
							pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

						# Menu action
						elif "call_menu_main" in event.ui_element.object_ids:
							self.submenu = SubMenu.MAIN
						elif "call_menu_local" in event.ui_element.object_ids:
							self.submenu = SubMenu.LOCAL
						elif "call_menu_network" in event.ui_element.object_ids:
							self.submenu = SubMenu.NETWORK
						elif "call_menu_single" in event.ui_element.object_ids:
							self.submenu = SubMenu.SINGLE
						elif "call_menu_double" in event.ui_element.object_ids:
							self.submenu = SubMenu.DOUBLE
						elif "call_menu_spectate" in event.ui_element.object_ids:
							self.submenu = SubMenu.SPECTATE
						elif "call_menu_host" in event.ui_element.object_ids:
							if self.server_started:
								server.stop_server()
							self.submenu = SubMenu.HOST
						elif "call_menu_join" in event.ui_element.object_ids:
							if self.network is not None:
								self.send_network_data("DISCONNECT")
								self.network = None
							self.submenu = SubMenu.JOIN

						# Lobby action
						elif "call_lobby_host" in event.ui_element.object_ids:
							server.start_server_thread("0.0.0.0", c4gui.config.get("Network", "host_port", int))
							self.server_started = True
							self.network = network.Network(server_ip="127.0.0.1", port=c4gui.config.get("Network", "host_port", int))
							self.network.connect()
							self.submenu = SubMenu.HOST_LOBBY
						elif "call_lobby_join" in event.ui_element.object_ids:
							network_parts = c4gui.config.get("Network", "last_connection", str).split(":", 1)
							self.network = network.Network(server_ip=network_parts[0], port=int(network_parts[1]))
							if self.network.connect():
								self.send_network_data()
								self.submenu = SubMenu.JOIN_LOBBY
							else:
								# TODO throw join error message
								self.submenu = SubMenu.JOIN

						# Game action
						elif "call_game_single" in event.ui_element.object_ids:
							self.game_callback(self, c4gui.game.GameType.SINGLE)
						elif "call_game_double" in event.ui_element.object_ids:
							self.game_callback(self, c4gui.game.GameType.DOUBLE)
						elif "call_game_spectate" in event.ui_element.object_ids:
							self.game_callback(self, c4gui.game.GameType.SPECTATE)
						elif "call_game_host" in event.ui_element.object_ids:
							self.send_network_data("START")
							self.send_network_data()
							self.game_callback(self, c4gui.game.GameType.HOST,self.network)

						# Invalid ID
						else:
							regenerate = False

						# Regenerate the menu elements
						if regenerate:
							self.generate()

				self.manager.process_events(event)

			self.manager.update(time_delta)

			# Draw the background, logo, and theme button
			surface.fill(self.theme.background)
			surface.blit(self.theme.logo, (logo_x, logo_y))
			surface.blit(pygame.transform.scale(self.theme.icons.theme, (theme_button.width, theme_button.height)), (theme_button.x, theme_button.y))
			surface.blit(pygame.transform.scale(self.theme.icons.sound_on if self.sound else self.theme.icons.sound_off, (sound_button.width, sound_button.height)), (sound_button.x, sound_button.y))

			# Render the drawing
			self.manager.draw_ui(surface)
			pygame.display.update()
			clock.tick(c4gui.TICKSPEED)
