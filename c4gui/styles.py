#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import os
import pygame


# Colors
COLORS = {
	"PINK": (233, 30, 99),
	"RED": (244, 67, 54),
	"ORANGE": (255, 152, 0),
	"AMBER": (255, 193, 7),
	"YELLOW": (255, 235, 59),
	"LIME": (205, 220, 57),
	"LIGHT_GREEN": (139, 195, 74),
	"GREEN": (76, 175, 80),
	"TEAL": (0, 150, 136),
	"CYAN": (0, 188, 212),
	"LIGHT_BLUE": (3, 169, 244),
	"BLUE": (33, 150, 243),
	"INDIGO": (63, 81, 181),
	"PURPLE": (156, 39, 176),
	"BROWN": (121, 85, 72),
	"GRAY": (150, 150, 150),
	"DARK_GRAY": (47, 49, 54),
	"WHITE": (255, 255, 255),
	"OFF_WHITE": (200, 200, 200),
	"BLACK": (0, 0, 0),
	"OFF_BLACK": (10, 10, 10),
}


def get_color_name(x):
	return x.replace("_", " ").title()


def get_color_from_name(x):
	key = x.replace(" ", "_").upper()
	if key not in COLORS:
		raise IndexError("invalid color value")
	return COLORS[key]


def get_color_from_tuple(x):
	for color in COLORS.keys():
		if x == COLORS[color]:
			return color
	raise IndexError("unlisted color configuration")


def get_color_name_from_tuple(x):
	return get_color_name(get_color_from_tuple(x))


def get_all_color_names():
	return [get_color_name(x) for x in COLORS.keys()]


# Fonts
FONT = pygame.font.SysFont("Open Sans", 72)
FONT_SMALL = pygame.font.SysFont("Open Sans", 100)
FONT_LARGE = pygame.font.SysFont("Open Sans", 40)


# Icon sets
ICONS_LIGHT = c4gui.Icons(theme=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "theme.png")),
						  sound_on=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "sound_on.png")),
						  sound_off=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "sound_off.png")),
						  nav_first=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_first.png")),
						  nav_prev=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_prev.png")),
						  nav_nonce=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_nonce.png")),
						  nav_next=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_next.png")),
						  nav_last=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_last.png")))

ICONS_DARK = c4gui.Icons(theme=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "theme.png")),
						 sound_on=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "sound_on.png")),
						 sound_off=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "sound_off.png")),
						 nav_first=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_first.png")),
						 nav_prev=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_prev.png")),
						 nav_nonce=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_nonce.png")),
						 nav_next=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_next.png")),
						 nav_last=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_last.png")))

ICONS_LIGHT_HOVER = c4gui.Icons(theme=None,
								sound_on=None,
								sound_off=None,
								nav_first=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light_hover", "nav_first.png")),
								nav_prev=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light_hover", "nav_prev.png")),
								nav_nonce=None,
								nav_next=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light_hover", "nav_next.png")),
								nav_last=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light_hover", "nav_last.png")))

ICONS_DARK_HOVER = c4gui.Icons(theme=None,
							   sound_on=None,
							   sound_off=None,
							   nav_first=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark_hover", "nav_first.png")),
							   nav_prev=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark_hover", "nav_prev.png")),
							   nav_nonce=None,
							   nav_next=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark_hover", "nav_next.png")),
							   nav_last=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark_hover", "nav_last.png")))


# Themes
THEME_LIGHT = c4gui.Theme(text=COLORS["BLACK"],
						  background=COLORS["WHITE"],
						  button=COLORS["GRAY"],
						  hover=COLORS["DARK_GRAY"],
						  logo=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "logo_light.png")),
						  icons=ICONS_LIGHT,
						  icons_hover=ICONS_LIGHT_HOVER,
						  board=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "boards", "blue_light.png")),
						  empty=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "boards", "empty", "blue_light.png")),
						  shadow=COLORS["OFF_WHITE"],
						  gui_ext=os.path.join(c4gui.ASSET_PATH, "themes", "light.json"))

THEME_DARK = c4gui.Theme(text=COLORS["WHITE"],
						 background=COLORS["BLACK"],
						 button=COLORS["DARK_GRAY"],
						 hover=COLORS["GRAY"],
						 logo=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "logo_dark.png")),
						 icons=ICONS_DARK,
						 icons_hover=ICONS_DARK_HOVER,
						 board=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "boards", "blue_dark.png")),
						 empty=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "boards", "empty", "blue_dark.png")),
						 shadow=COLORS["OFF_BLACK"],
						 gui_ext=os.path.join(c4gui.ASSET_PATH, "themes", "dark.json"))


# Theme mappings for configuration storage
THEMES = {
	"THEME_LIGHT": THEME_LIGHT,
	"THEME_DARK": THEME_DARK
}


# Board dimensions
BOARD_WIDTH = 1920
BOARD_HEIGHT = 1608
BOARD_OFFSET_X = 343
BOARD_OFFSET_Y = 286
GRID_START_X = 159
GRID_START_Y = 62
GRID_END_X = 1757
GRID_END_Y = 1451
X_STRETCH = 1.5
Y_STRETCH = 2.6
PADDING_TOP = 0.1
TOKEN_RADIUS = 96
SPRITE_SCALE = 20
