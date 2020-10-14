#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import pygame
from typing import Tuple, Callable
from functools import partial


class Menu:
	"""Handles menu creation, animation, and alteration."""
	
	def __init__(self, theme: c4gui.Theme, display_width: int, display_height: int) -> None:
		"""
		Set up menu elements
		
		theme -- A c4gui styling theme
		display_width -- The screen display width
		display_height -- The screen display height
		"""
		
		# Instantiate passed variables
		self.buttons = []
		self.theme = theme
		self.display_width = display_width
		self.display_height = display_height

	def generate(self, buttons: Tuple[Tuple, ...], button_width: float = -1, button_height: int = 80, padding: int = 20) -> None:
		"""
		Generate the button elements for the menu
		
		buttons -- A tuple of tuples containing textual data and a callback
		button_width -- The button width
		button_height -- The button height
		padding -- The space between buttons
		"""

		# Handle default cases
		if button_width == -1:
			button_width = self.display_width / 3
		
		# Add each button, starting at the center of both dimensions
		offset: float = self.display_height / 2
		for button in buttons:

			# Verify parameters
			if len(button) < 2 or not button[1] or not isinstance(button[1], Callable):
				raise TypeError("invalid button callback")

			# Append to the list
			self.buttons.append({
				"data": button[0],
				"text": self.get_font(button[0]),
				"rect": pygame.Rect(self.display_width / 2 - button_width / 2, offset, button_width, button_height),
				"color": self.theme.button,
				"callback": button[1],
				"args": button[2] if len(button) > 2 else tuple()
			})
			offset += (button_height + padding)

	def get_font(self, data: str) -> pygame.font:
		"""
		Return a font object according to the menu theme
		
		data - The plain text to be formatted
		"""
		
		return c4gui.styles.FONT.render(data, True, self.theme.text)
	
	def set_theme(self, theme: c4gui.Theme) -> None:
		"""
		Set the menu theme
		
		theme - theme -- A c4gui styling theme
		"""
		
		self.theme = theme
	
	def toggle_theme(self) -> None:
		"""Toggle between LIGHT and DARK themes"""
		
		# Toggle the theme
		if self.theme == c4gui.styles.THEME_LIGHT:
			self.set_theme(c4gui.styles.THEME_DARK)
		else:
			self.set_theme(c4gui.styles.THEME_LIGHT)
		
		# Adjust button and font colors
		for button in self.buttons:
			button["text"] = self.get_font(button["data"])
			button["color"] = self.theme.button 

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
			
			# Handle and remove all events from the pygame queue from the last tick
			# https://github.com/pygame/pygame/blob/e40d00db1f8015e8f37624f83a0bd334547cd8dc/docs/reST/ref/event.rst
			for event in pygame.event.get():

				# check for SIGINT
				c4gui.helpers.check_sigint(event)
					
				if event.type == pygame.MOUSEMOTION:
					
					# Check if the mouse is within any button rectangle for button hover effect
					for button in self.buttons:
						if button["rect"].collidepoint(event.pos):
							button["color"] = self.theme.hover
						else:
							button["color"] = self.theme.button
					
				elif event.type == pygame.MOUSEBUTTONDOWN:
					
					# Check if the mouse clicked within any button rectangle for callback execution
					for button in self.buttons:
						if button["rect"].collidepoint(event.pos):
							c4gui.sfx.play("click")
							button["callback"](*((self,) + button["args"]))
							break
					
					# Check if the mouse clicked the theme button
					if theme_button.collidepoint(event.pos[0], event.pos[1]):
						c4gui.sfx.play("toggle")
						self.toggle_theme()
			
			# Draw the background, logo, and theme button
			surface.fill(self.theme.background)
			surface.blit(self.theme.logo, (logo_x, logo_y))
			surface.blit(pygame.transform.scale(self.theme.icons.theme, (theme_button.width, theme_button.height)), (theme_button.x, theme_button.y))
			
			# Draw all buttons
			for button in self.buttons:
				
				# Color the button
				pygame.draw.rect(surface, button["color"], button["rect"])
				
				# Center and draw the button text
				text_x = button["rect"].x + button["rect"].width / 2
				text_y = button["rect"].y + button["rect"].height / 2
				surface.blit(button["text"], button["text"].get_rect(center=(text_x, text_y)))
			
			# Render the drawing
			pygame.display.flip()
			clock.tick(20)
