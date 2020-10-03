#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import pygame
from typing import Callable, Tuple

# Establish the entire screen as the primary surface and prepare the clock
screen: pygame.display = pygame.display.Info()
HEIGHT: int = int(screen.current_h / c4gui.SCALE_MODIFIER)
WIDTH: int = int(screen.current_w / c4gui.SCALE_MODIFIER)
DISPLAY: pygame.display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
CLOCK: pygame.time.Clock = pygame.time.Clock()


def quit_game(from_menu: c4gui.menu.Menu) -> None:
	"""
	Callback to trigger a QUIT event

	from_menu -- The menu used to trigger the callback
	"""

	pygame.event.post(pygame.event.Event(pygame.QUIT, {}))


def main_menu(from_menu: c4gui.menu.Menu = None) -> None:
	"""
	Self-runnable or callback to run the main main loop

	from_menu -- The menu used to trigger the callback
	"""

	# Set up buttons
	buttons = (
		("Local Game", local_menu),
		("Network Game", quit_game),
		("Quit", quit_game)
	)

	# Make a new Menu and (re-)render all objects
	menu = c4gui.menu.Menu(c4gui.styles.THEME_LIGHT if from_menu is None else from_menu.theme, WIDTH, HEIGHT)
	menu.generate(buttons, WIDTH/3, 80, 20)
	menu.render(DISPLAY, CLOCK)


def local_menu(from_menu: c4gui.menu) -> None:
	"""
	Callback to run the "Local Game" menu

	from_menu -- The menu used to trigger the callback
	"""

	# Set up buttons
	buttons: Tuple[Tuple[str, Callable], ...] = (
		("1-Player", quit_game),
		("2-Player", quit_game),
		("Spectate", quit_game),
		("Back", main_menu)
	)

	# Make a new Menu and (re-)render all objects
	menu: c4gui.Menu = c4gui.menu.Menu(from_menu.theme, WIDTH, HEIGHT)
	menu.generate(buttons, WIDTH/3, 80, 20)
	menu.render(DISPLAY, CLOCK)


# Entrypoint straight into the main menu
main_menu()
