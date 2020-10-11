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
COLOR_WHITE = (255, 255, 255)
COLOR_OFFWHITE = (200, 200, 200)
COLOR_BLACK = (0, 0, 0)
COLOR_OFFBLACK = (10, 10, 10)
COLOR_DISCORD = (47, 49, 54)


# Fonts
FONT = pygame.font.SysFont("Open Sans", 72)
FONT_SMALL = pygame.font.SysFont("Open Sans", 100)
FONT_LARGE = pygame.font.SysFont("Open Sans", 40)


# Themes
THEME_LIGHT = c4gui.Theme(text=COLOR_WHITE,
					background=COLOR_WHITE,
					button=COLOR_GRAY,
					hover=COLOR_DISCORD,
					logo=pygame.image.load(os.path.join(c4gui.GAMEPATH, "logo_light.png")),
					meta=pygame.image.load(os.path.join(c4gui.GAMEPATH, "icons", "darkmode.png")),
					board=pygame.image.load(os.path.join(c4gui.GAMEPATH, "boards", "blue_light.png")),
					empty=pygame.image.load(os.path.join(c4gui.GAMEPATH, "boards", "empty", "blue_light.png")),
					shadow=COLOR_OFFWHITE)

THEME_DARK = c4gui.Theme(text=COLOR_WHITE,
					background=COLOR_BLACK,
					button=COLOR_DISCORD,
					hover=COLOR_GRAY,
					logo=pygame.image.load(os.path.join(c4gui.GAMEPATH, "logo_dark.png")),
					meta=pygame.image.load(os.path.join(c4gui.GAMEPATH, "icons", "lightmode.png")),
					board=pygame.image.load(os.path.join(c4gui.GAMEPATH, "boards", "blue_dark.png")),
					empty=pygame.image.load(os.path.join(c4gui.GAMEPATH, "boards", "empty", "blue_dark.png")),
					shadow=COLOR_OFFBLACK)

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
