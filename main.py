#!/usr/bin/env python3

import pygame
import os


class TypeStateInformation:
	"""Contains information necessary between all states """

	def __init__(self, menu_option: str, player_count: int) -> None:
		"""
		Initializes a typeStateInformation object

		menu_option -- The currently selected menu option

		player_count -- Selected number of human players
		"""

		self.menu_option: str = menu_option
		self.player_count: int = player_count


def state_game(state_information_instance: TypeStateInformation) -> None:
	"""
	Game state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("  1   2   3   4   5   6   7  ")
		print("                             ")
		print("|   |   |   |   |   |   |   |")
		print("+---------------------------+")
		print("|   |   |   |   |   |   |   |")
		print("+---------------------------+")
		print("|   |   |   |   |   |   |   |")
		print("+---------------------------+")
		print("|   |   |   |   |   |   |   |")
		print("+---------------------------+")
		print("|   |   |   |   |   |   |   |")
		print("+---------------------------+")
		print("|   |   |   |   |   |   |   |")
		print("+---------------------------+")
		print("|   |   |   |   |   |   |   |")
		print("+---------------------------+")
		state_information_instance.menu_option = input("| > Select column: ")
		if state_information_instance.menu_option == "1":
			print("##TODO##")
		elif state_information_instance.menu_option == "2":
			print("##TODO##")
		elif state_information_instance.menu_option == "3":
			print("##TODO##")
	state_information_instance.menu_option = "-1"


def state_gamesetup(state_information_instance: TypeStateInformation, sub_menu_string: str) -> None:
	"""
	Game-setup state

	state_information_instance -- Instance containing state information
	sub_menu_string -- Indicates which submenu text to display in menu ("local"/"network")
	player_count -- Represents number of players/number of CPU
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		if sub_menu_string == "local":
			print("|       Local-play      |")
		elif sub_menu_string == "network":
			print("|     Network-play      |")
		print("+-----------------------+")
		print("|       Game Setup      |")
		print("+-----------------------+")
		print("| 1. SFX: ON / [OFF]    |")
		if state_information_instance.player_count < 2:
			print("| 2. CPU #1 Difficulty: |")
			if state_information_instance.player_count < 1:
				print("| 3. CPU #2 Difficulty: |")
		print("| 9. Start game         |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			print("##TODO##")
		elif state_information_instance.menu_option == "2":
			print("##TODO##")
		elif state_information_instance.menu_option == "3":
			print("##TODO##")
		elif state_information_instance.menu_option == "9":
			state_game(state_information_instance)
	state_information_instance.menu_option = "-1"


def state_localplay(state_information_instance):
	"""
	Local-play state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("|       Local-play      |")
		print("+-----------------------+")
		print("| 1. 1-player           |")
		print("| 2. 2-player           |")
		print("| 3. Spectate           |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			state_information.instance.player_count = 1;
			state_gamesetup(state_information_instance, "local", 1)
		elif state_information_instance.menu_option == "2":
			state_information.instance.player_count = 2;
			state_gamesetup(state_information_instance, "local", 2)
		elif state_information_instance.menu_option == "3":
			state_information.instance.player_count = 0
			state_gamesetup(state_information_instance, "local", 0)
	state_information_instance.menu_option = "-1"


def state_networkplay(state_information_instance):
	"""
	Network-play state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("|      Network-play     |")
		print("+-----------------------+")
		print("| 1. Host game          |")
		print("| 2. Join game          |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			print("##TODO##")
		elif state_information_instance.menu_option == "2":
			print("##TODO##")
	state_information_instance.menu_option = "-1"


def state_options(state_information_instance):
	"""
	Options state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("|        Options        |")
		print("+-----------------------+")
		print("| 1. Resolution         |")
		print("| 2. Display Name       |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			print("##TODO##")
		elif state_information_instance.menu_option == "2":
			print("##TODO##")
	state_information_instance.menu_option = "-1"


def state_mainmenu(state_information_instance):
	"""
	Main Menu state

	state_information_instance -- Instance containing state information
	"""

	while state_information_instance.menu_option != "0":
		os.system("cls" if os.name == "nt" else "clear")
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("| 1. Local-play         |")
		print("| 2. Network-play       |")
		print("| 3. Options            |")
		print("| 0. Quit               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if state_information_instance.menu_option == "1":
			state_localplay(state_information_instance)
		elif state_information_instance.menu_option == "2":
			state_networkplay(state_information_instance)
		elif state_information_instance.menu_option == "3":
			state_options(state_information_instance)
	state_information_instance.menu_option = "-1"


def main():
	state_information_instance: TypeStateInformation = TypeStateInformation("-1")
	state_mainmenu(state_information_instance)


if __name__ == "__main__":
	main()
