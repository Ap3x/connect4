#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import pygame
import pygame_gui
from typing import Tuple, Callable


class SubMenu:
	MAIN = 1
	LOCAL = 2
	SINGLE = 3
	DOUBLE = 4
	SPECTATE = 5
	NETWORK = 6
	HOST = 7
	JOIN = 8


def callback_do_nothing() -> None:
	"""
	Callback to not trigger anything

	from_menu -- The menu used to trigger the callback
	"""

	# TODO - Remove this callback when development is done
	c4gui.sfx.play("invalid")


class Menu:
	"""Handles menu creation, animation, and alteration."""

	def __init__(self, theme: c4gui.Theme, display_width: int, display_height: int, submenu: int, game_callback: Callable) -> None:
		"""
		Set up menu elements
		
		theme -- A c4gui styling theme
		display_width -- The screen display width
		display_height -- The screen display height
		"""
		
		# Instantiate passed variables
		self.theme = theme
		self.display_width = display_width
		self.display_height = display_height
		self.submenu = submenu
		self.manager = None
		self.reload_manager()
		self.game_callback = game_callback
		self.element_values = {}

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

		# Clear the surface
		self.manager.clear_and_reset()

		# Switch cases for all possible menus
		if self.submenu == SubMenu.MAIN:

			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset), (button_width, button_height)),
												   text="Local Game",
												   object_id="call_menu_local")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + button_height + padding), (button_width, button_height)),
												   text="Network Game",
												   object_id="call_menu_network")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												   text="Quit",
												   object_id="quit")

		elif self.submenu == SubMenu.LOCAL:

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

			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (200 + padding) + h_offset), v_offset - 2 * (button_height + padding)), (200, button_height)),
												 text="Sound Effects")
			pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(manager=self.manager,
																 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - 2 * (button_height + padding) + 20), (200, 40)),
																 options_list=["Enabled", "Disabled"],
																 starting_option=("Enabled" if c4gui.config.get("Global", "sfx_enabled", bool) else "Disabled"),
																 object_id="set_sfx")
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
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Start",
												   object_id="call_game_single")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 4 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_local")

		elif self.submenu == SubMenu.DOUBLE:

			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (200 + padding) + h_offset), v_offset), (200, button_height)),
												 text="Sound Effects")
			pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(manager=self.manager,
																 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset + 20), (200, 40)),
																 options_list=["Enabled", "Disabled"],
																 starting_option=("Enabled" if c4gui.config.get("Global", "sfx_enabled", bool) else "Disabled"),
																 object_id="set_sfx")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 2 * (button_height + padding)), (button_width, button_height)),
												   text="Start",
												   object_id="call_game_double")
			pygame_gui.elements.ui_button.UIButton(manager=self.manager,
												   relative_rect=pygame.Rect((horizontal_middle, v_offset + 3 * (button_height + padding)), (button_width, button_height)),
												   text="Back",
												   object_id="call_menu_local")

		elif self.submenu == SubMenu.SPECTATE:

			pygame_gui.elements.ui_label.UILabel(manager=self.manager,
												 relative_rect=pygame.Rect((int(self.display_width / 2 - (200 + padding) + h_offset), v_offset - 2 * (button_height + padding)), (200, button_height)),
												 text="Sound Effects")
			pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(manager=self.manager,
																 relative_rect=pygame.Rect((int(self.display_width / 2 + padding + h_offset), v_offset - 2 * (button_height + padding) + 20), (200, 40)),
																 options_list=["Enabled", "Disabled"],
																 starting_option=("Enabled" if c4gui.config.get("Global", "sfx_enabled", bool) else "Disabled"),
																 object_id="set_sfx")
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
			callback_do_nothing()
		elif self.submenu == SubMenu.HOST:
			callback_do_nothing()
		elif self.submenu == SubMenu.JOIN:
			callback_do_nothing()
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

		# Loop until a user triggers callback
		while True:

			time_delta = clock.tick(60) / 1000.0
			
			# Handle and remove all events from the pygame queue from the last tick
			# https://github.com/pygame/pygame/blob/e40d00db1f8015e8f37624f83a0bd334547cd8dc/docs/reST/ref/event.rst
			for event in pygame.event.get():

				# check for SIGINT
				c4gui.check_sigint(event)

				# Handle custom fields
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == c4gui.Mouse.LEFT:

					# Check if the mouse clicked the theme button
					if theme_button.collidepoint(event.pos[0], event.pos[1]):
						c4gui.sfx.play("toggle")
						self.toggle_theme()

				# Handle menu elements
				elif event.type == pygame.USEREVENT:

					if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:

						if "set_cpu0" in event.ui_element.object_ids:
							self.element_values["cpu0"].set_text(str(event.value))
						elif "set_cpu1" in event.ui_element.object_ids:
							self.element_values["cpu1"].set_text(str(event.value))
						elif "set_cpu2" in event.ui_element.object_ids:
							self.element_values["cpu2"].set_text(str(event.value))

					elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:

						if "set_sfx" in event.ui_element.object_ids:
							c4gui.config.set("Global", "sfx_enabled", (event.text == "Enabled"))

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
							self.submenu = SubMenu.HOST
						elif "call_menu_join" in event.ui_element.object_ids:
							self.submenu = SubMenu.JOIN

						# Game action
						elif "call_game_single" in event.ui_element.object_ids:
							self.game_callback(self, c4gui.game.GameType.SINGLE)
						elif "call_game_double" in event.ui_element.object_ids:
							self.game_callback(self, c4gui.game.GameType.DOUBLE)
						elif "call_game_spectate" in event.ui_element.object_ids:
							self.game_callback(self, c4gui.game.GameType.SPECTATE)
						elif "call_game_host" in event.ui_element.object_ids:
							self.game_callback(self, c4gui.game.GameType.HOST)
						elif "call_game_join" in event.ui_element.object_ids:
							self.game_callback(self, c4gui.game.GameType.JOIN)

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
			
			# Render the drawing
			self.manager.draw_ui(surface)
			pygame.display.update()
			clock.tick(c4gui.TICKSPEED)
