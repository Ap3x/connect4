#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import configparser
import os

from ast import literal_eval

config = configparser.ConfigParser()
config_path = os.path.join(c4gui.ORIGIN_PATH, 'settings.ini')
config.read(config_path)


def section_exists(section: str) -> bool:
	"""
	Determine if a section exists in the configuration

	section -- the INI section header
	"""

	return section in config


def setting_exists(setting: str, section: any = None) -> bool:
	"""
	Determine if a specific setting exists in the configuration

	setting -- the INI option
	section -- the INI section header; defaults to any section
	"""

	if section is not None:
		return section in config and setting in config[section]
	for section in config:
		if setting in config[section]:
			return True
	return False


def get(section: str, setting: str, expect: type = str) -> any:
	"""
	Get a configuration value

	section -- the INI section header
	setting -- the INI option
	expect -- an optional type cast
	"""

	if section_exists(section) and setting_exists(setting, section):
		try:
			if expect == bool:
				return config.getboolean(section, setting)
			if expect == str:
				return config.get(section, setting)
			if expect == int:
				return config.getint(section, setting)
			if expect == float:
				return config.getfloat(section, setting)
			if expect == tuple:
				return literal_eval(config[section][setting])
			if expect == c4gui.Theme:
				return c4gui.styles.THEMES[config.get(section, setting)]
			return config[section][setting]
		except ValueError as e:
			raise ValueError("invalid configuration type: %s/%s: %s" % (section, setting, e)) from None
	else:
		raise IndexError("no such section/setting exists: %s/%s" % (section, setting))


def set(section: str, setting: str, value: any, do_commit: bool = True) -> None:
	"""
	Set a configuration value

	section -- the INI section header
	setting -- the INI option
	value -- the persistent data to be stored
	do_commit -- write changes to the settings file; defaults to true
	"""

	if not config.has_section(section):
		config.add_section(section)
	config.set(section, setting, str(value))

	if do_commit:
		commit()


def commit() -> None:
	"""
	Save the configuration in the file system
	"""

	with open(config_path, 'w') as fp:
		config.write(fp)


def init() -> None:
	"""
	Initialize default settings if no settings file exists
	"""

	if not os.path.exists(config_path):

		# Define defaults here
		defaults = {
			"Global": {
				"theme": "THEME_LIGHT",
				"sfx_enabled": True
			},
			"Player": {
				"name": "Player",
				"color": c4gui.styles.COLOR_RED
			},
			"Computer0": {
				"name": "CPU",
				"color": c4gui.styles.COLOR_YELLOW,
				"difficulty": 5
			},
			"Computer1": {
				"name": "CPU 1",
				"color": c4gui.styles.COLOR_RED,
				"difficulty": 5
			},
			"Computer2": {
				"name": "CPU 2",
				"color": c4gui.styles.COLOR_YELLOW,
				"difficulty": 5
			},
			"Network": {
				"host_ip": "",
				"host_port": 6334,
				"last_connection": "x.x.x.x:6334"
			}
		}

		for section in defaults:
			for setting in defaults[section]:
				set(section, setting, defaults[section][setting])
		commit()
