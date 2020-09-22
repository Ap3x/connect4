#!/usr/bin/env python3

import pygame
import os

class State_Information_t:
	"""
	@brief Contains information necessary between all states
	"""

	def __init__(self, menu_option):
		"""
		@brief Initialize
		@param menu_option Integer: The currently selected menu option
		"""

		self.menu_option = menu_option

def State_Game(state_information_instance):
	"""
	@brief Game state
	@param state_information_instance State_Information_t: Instance containing state information
	"""

	while (state_information_instance.menu_option != "0"):
		os.system('cls' if os.name == 'nt' else 'clear')
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
		if (state_information_instance.menu_option == "1"):
			print("##TODO##")
		elif (state_information_instance.menu_option == "2"):
			print("##TODO##")
		elif (state_information_instance.menu_option == "3"):
			print("##TODO##")
	state_information_instance.menu_option = -1

def State_GameSetup(state_information_instance, sub_menu_string, player_count):
	"""
	@brief Game-setup state
	@param state_information_instance State_Information_t: Instance containing state information
	@param sub_menu_string String: Either "local" or "network" indicating which submenu text to display in menu
	@param player_count Integer: Represents number of players/number of CPU
	"""

	while (state_information_instance.menu_option != "0"):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		if (sub_menu_string == "local"):
			print("|       Local-play      |")
		elif (sub_menu_string == "network"):
			print("|     Network-play      |")
		print("+-----------------------+")
		print("|       Game Setup      |")
		print("+-----------------------+")
		print("| 1. SFX: ON / [OFF]    |")
		if (player_count > 0):
			print("| 2. CPU #1 Difficulty: |")
			if(player_count > 1):
				print("| 3. CPU #2 Difficulty: |")
		print("| 9. Start game         |")
		print("| 0. Back               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if (state_information_instance.menu_option == "1"):
			print("##TODO##")
		elif (state_information_instance.menu_option == "2"):
			print("##TODO##")
		elif (state_information_instance.menu_option == "3"):
			print("##TODO##")
		elif (state_information_instance.menu_option == "9"):
			State_Game(state_information_instance)
	state_information_instance.menu_option = -1

def State_LocalPlay(state_information_instance):
	"""
	@brief Local-play state
	@param state_information_instance State_Information_t: Instance containing state information
	"""

	while (state_information_instance.menu_option != "0"):
		os.system('cls' if os.name == 'nt' else 'clear')
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
		if (state_information_instance.menu_option == "1"):
			State_GameSetup(state_information_instance, "local", 1)
		elif (state_information_instance.menu_option == "2"):
			State_GameSetup(state_information_instance, "local", 2)
		elif (state_information_instance.menu_option == "3"):
			State_GameSetup(state_information_instance, "local", 0)
	state_information_instance.menu_option = -1


def State_NetworkPlay(state_information_instance):
	"""
	@brief Network-play state
	@param state_information_instance State_Information_t: Instance containing state information
	"""

	while (state_information_instance.menu_option != "0"):
		os.system('cls' if os.name == 'nt' else 'clear')
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
		if (state_information_instance.menu_option == "1"):
			print("##TODO##")
		elif (state_information_instance.menu_option == "2"):
			print("##TODO##")		
	state_information_instance.menu_option = -1
	
			
def State_Options(state_information_instance):
	"""
	@brief Options state
	@param state_information_instance State_Information_t: Instance containing state information
	"""

	while (state_information_instance.menu_option != "0"):
		os.system('cls' if os.name == 'nt' else 'clear')
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
		if (state_information_instance.menu_option == "1"):
			print("##TODO##")
		elif (state_information_instance.menu_option == "2"):
			print("##TODO##")
	state_information_instance.menu_option = -1


def State_MainMenu(state_information_instance):
	"""
	@brief Main Menu state
	@param state_information_instance State_Information_t: Instance containing state information
	"""

	while (state_information_instance.menu_option != "0"):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("+-----------------------+")
		print("|       Connect 4       |")
		print("+-----------------------+")
		print("| 1. Local-play         |")
		print("| 2. Network-play       |")
		print("| 3. Options            |")
		print("| 0. Quit               |")
		print("+-----------------------+")
		state_information_instance.menu_option = input("| > Select menu option: ")
		if (state_information_instance.menu_option == "1"):
			State_LocalPlay(state_information_instance)
		elif (state_information_instance.menu_option == "2"):
			State_NetworkPlay(state_information_instance)
		elif (state_information_instance.menu_option == "3"):
			State_Options(state_information_instance)
	state_information_instance.menu_option = -1


def main():
	"""
	@brief Main
	"""
	state_information_instance = State_Information_t(-1)

	State_MainMenu(state_information_instance)

main()
