#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import os
import pygame


# Colors
COLOR_PINK = (233, 30, 99)
COLOR_RED = (244, 67, 54)
COLOR_ORANGE = (255, 152, 0)
COLOR_AMBER = (255, 193, 7)
COLOR_YELLOW = (255, 235, 59)
COLOR_LIME = (205, 220, 57)
COLOR_LIGHT_GREEN = (139, 195, 74)
COLOR_GREEN = (76, 175, 80)
COLOR_TEAL = (0, 150, 136)
COLOR_CYAN = (0, 188, 212)
COLOR_LIGHT_BLUE = (3, 169, 244)
COLOR_BLUE = (33, 150, 243)
COLOR_INDIGO = (63, 81, 181)
COLOR_PURPLE = (156, 39, 176)
COLOR_BROWN = (121, 85, 72)
COLOR_GRAY = (150, 150, 150)
COLOR_GREY = COLOR_GRAY
COLOR_DARK_GRAY = (47, 49, 54)
COLOR_DARK_GREY = COLOR_DARK_GRAY
COLOR_WHITE = (255, 255, 255)
COLOR_OFF_WHITE = (200, 200, 200)
COLOR_BLACK = (0, 0, 0)
COLOR_OFF_BLACK = (10, 10, 10)


# Fonts
FONT = pygame.font.SysFont("Open Sans", 72)
FONT_SMALL = pygame.font.SysFont("Open Sans", 100)
FONT_LARGE = pygame.font.SysFont("Open Sans", 40)


# Icon sets
ICONS_LIGHT = c4gui.Icons(theme=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "theme.png")),
						  nav_first=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_first.png")),
						  nav_prev=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_prev.png")),
						  nav_nonce=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_nonce.png")),
						  nav_next=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_next.png")),
						  nav_last=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light", "nav_last.png")))

ICONS_DARK = c4gui.Icons(theme=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "theme.png")),
						 nav_first=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_first.png")),
						 nav_prev=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_prev.png")),
						 nav_nonce=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_nonce.png")),
						 nav_next=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_next.png")),
						 nav_last=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark", "nav_last.png")))

ICONS_LIGHT_HOVER = c4gui.Icons(theme=None,
								nav_first=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light_hover", "nav_first.png")),
								nav_prev=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light_hover", "nav_prev.png")),
								nav_nonce=None,
								nav_next=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light_hover", "nav_next.png")),
								nav_last=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "light_hover", "nav_last.png")))

ICONS_DARK_HOVER = c4gui.Icons(theme=None,
							   nav_first=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark_hover", "nav_first.png")),
							   nav_prev=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark_hover", "nav_prev.png")),
							   nav_nonce=None,
							   nav_next=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark_hover", "nav_next.png")),
							   nav_last=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "icons", "dark_hover", "nav_last.png")))


# Themes
THEME_LIGHT = c4gui.Theme(text=COLOR_WHITE,
						  background=COLOR_WHITE,
						  button=COLOR_GRAY,
						  hover=COLOR_DARK_GRAY,
						  logo=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "logo_light.png")),
						  icons=ICONS_LIGHT,
						  icons_hover=ICONS_LIGHT_HOVER,
						  board=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "boards", "blue_light.png")),
						  empty=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "boards", "empty", "blue_light.png")),
						  shadow=COLOR_OFF_WHITE,
						  gui_ext=os.path.join(c4gui.ASSET_PATH, "themes", "light.json"))

THEME_DARK = c4gui.Theme(text=COLOR_WHITE,
						 background=COLOR_BLACK,
						 button=COLOR_DARK_GRAY,
						 hover=COLOR_GRAY,
						 logo=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "logo_dark.png")),
						 icons=ICONS_DARK,
						 icons_hover=ICONS_DARK_HOVER,
						 board=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "boards", "blue_dark.png")),
						 empty=pygame.image.load(os.path.join(c4gui.ASSET_PATH, "boards", "empty", "blue_dark.png")),
						 shadow=COLOR_OFF_BLACK,
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
