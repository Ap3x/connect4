#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import os
import pygame
import random

sound_path = os.path.join(c4gui.GAMEPATH, "sfx")

SFX: dict = {
	"click": os.path.join(sound_path, "click.wav"),
	"toggle": os.path.join(sound_path, "toggle.wav"),
	"token_drop": os.path.join(sound_path, "token_drop"),
	"invalid": os.path.join(sound_path, "invalid.wav"),
	"up": os.path.join(sound_path, "up.wav"),
	"down": os.path.join(sound_path, "down.wav"),
	"special": os.path.join(sound_path, "special.wav"),
}


def init() -> None:
	"""
	Verify all sounds can be loaded
	"""
	global SFX

	# Check each listed sound effect exists
	for sound in SFX.values():
		if not os.path.exists(sound):
			raise OSError("sound effect source missing: %s" % sound)


def play(sound: str, loops: int = 0) -> None:
	"""
	Play a loaded sound file

	sound -- The name of the sound
	loops -- The number of times to loop the sound; defaults to 0
	"""
	global SFX

	# Check if the sound is loadable
	if sound in SFX.keys():

		# If the source is a directory, pick a random file from the directory
		if os.path.isdir(SFX[sound]):
			source = os.path.join(SFX[sound], random.choice(os.listdir(SFX[sound])))
		else:
			source = SFX[sound]

		# Pass the sound to pygame to play
		if os.path.isfile(source):
			pygame.mixer.music.load(source)
			pygame.mixer.music.play(loops)
			return

	# If anything failed, raise an exception
	raise KeyError("sound effect not loaded: %s" % sound)


init()
