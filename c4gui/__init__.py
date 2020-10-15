#!/usr/bin/python3
# -*- coding: utf8 -*-
import os
import pkgutil
import sys
from collections import namedtuple

# Set up any environment variables
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
os.environ["SDL_VIDEO_CENTERED"] = "1"
SCALE_MODIFIER: float = 1
GAMEPATH: str = os.path.join(os.path.dirname(__file__), "../assets")
TICKSPEED: int = 30
CPU_DELAY: int = 5
MAX_ROWS: int = 6
MAX_COLS: int = 7

# Initialize pygame
import pygame  # noqa: E402
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
pygame.display.set_icon(pygame.image.load(os.path.join(GAMEPATH, "favicon.png")))
pygame.display.set_caption("Connect4")

# Declare named tuples
Icons = namedtuple("Icons", "theme nav_first nav_prev nav_nonce nav_next nav_last")
Theme = namedtuple("Theme", "text background button hover logo icons icons_hover board empty shadow")
Players = namedtuple("Players", "p1_name p1_color p2_name p2_color")
MoveCallbacks = namedtuple("MoveCallbacks", "human computer network")
Coordinates = namedtuple("Coordinates", "x y")

# Inject all existing submodules
import c4gui.styles  # noqa: E402
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
	__all__.append(module_name)
	_module = loader.find_module(module_name).load_module(module_name)
	globals()[module_name] = _module

# Find the scaling factor since Windows devices can be zoomed
if sys.platform == "win32":
	import ctypes
	SCALE_MODIFIER = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
	# Ignore Windows DPI settings
	# try:
		# ctypes.windll.user32.SetProcessDPIAware()
	# except AttributeError:
		# pass


# Interrupt handler
def check_sigint(event: pygame.event) -> None:
	"""
	Check if a user sent an interrupt

	event - The published user event
	"""

	# Quit if pygame asks us or when the user presses either Esc or Alt+F4
	pressed = pygame.key.get_pressed()
	if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or (pressed[pygame.K_LALT] or pressed[pygame.K_RALT]) and event.key == pygame.K_F4):

		# Gracefully exit
		pygame.quit()
		sys.exit()
