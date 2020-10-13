#!/usr/bin/python3
# -*- coding: utf8 -*-

import pygame


def check_sigint(event: pygame.event) -> bool:
	"""
	Check if a user sent an interrupt

	event - The published user event
	"""

	# Quit if pygame asks us or when the user presses either Esc or Alt+F4
	pressed = pygame.key.get_pressed()
	return event.type == pygame.QUIT or event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or (pressed[pygame.K_LALT] or pressed[pygame.K_RALT]) and event.key == pygame.K_F4)
