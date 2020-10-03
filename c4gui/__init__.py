#!/usr/bin/python3
# -*- coding: utf8 -*-
import os
import pkgutil
import sys

# Set up any environment variables
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
os.environ["SDL_VIDEO_CENTERED"] = "1"
SCALE_MODIFIER = 1
GAMEPATH = os.path.join(os.path.dirname(__file__), "../assets")

# Initialize pygame
import pygame
pygame.init()
pygame.display.set_icon(pygame.image.load(os.path.join(GAMEPATH, "favicon.png")))
pygame.display.set_caption("Connect4")

# Declare named tuples
from collections import namedtuple
Theme = namedtuple("Theme", "text background button hover logo meta")

# Inject all existing submodules
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
