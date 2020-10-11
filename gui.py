#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import pygame

# Establish the entire screen as the primary surface and prepare the clock
screen: pygame.display = pygame.display.Info()
HEIGHT: int = int(screen.current_h / c4gui.SCALE_MODIFIER)
WIDTH: int = int(screen.current_w / c4gui.SCALE_MODIFIER)
DISPLAY: pygame.display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
CLOCK: pygame.time.Clock = pygame.time.Clock()


def callback_quit_game(from_menu: c4gui.menu.Menu) -> None:
    """
    Callback to trigger a QUIT event

    from_menu -- The menu used to trigger the callback
    """

    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))


def callback_do_nothing(from_menu: c4gui.menu.Menu) -> None:
    """
    Callback to not trigger anything

    from_menu -- The menu used to trigger the callback
    """

    pass


def screen_mainmenu(from_menu: c4gui.menu.Menu = None) -> None:
    """
    Self-runnable or callback to run the main main loop

    from_menu -- The menu used to trigger the callback
    """

    # Make a new Menu and (re-)render all objects
    menu = c4gui.menu.Menu(c4gui.styles.THEME_LIGHT if from_menu is None else from_menu.theme, WIDTH, HEIGHT)
    menu.generate((
        ("Local Game", screen_localplay),
        ("Network Game", screen_networkplay),
        ("Quit", callback_quit_game)
    ))
    menu.render(DISPLAY, CLOCK)


def screen_localplay(from_menu: c4gui.menu) -> None:
    """
    Callback to run the "Local Game" menu

    from_menu -- The menu used to trigger the callback
    """

    # Make a new Menu and (re-)render all objects
    menu: c4gui.Menu = c4gui.menu.Menu(from_menu.theme, WIDTH, HEIGHT)
    menu.generate((
        ("1-Player", screen_gamesetup_1p),
        ("2-Player", screen_gamesetup_2p),
        ("Spectate", screen_gamesetup_0p),
        ("Back", screen_mainmenu)
    ))
    menu.render(DISPLAY, CLOCK)


def screen_gamesetup_1p(from_menu: c4gui.menu) -> None:
    """
    Callback to run the "Game Setup" menu

    from_menu -- The menu used to trigger the callback
    """

    # Make a new Menu and (re-)render all objects
    menu: c4gui.Menu = c4gui.menu.Menu(from_menu.theme, WIDTH, HEIGHT)
    menu.generate((
        ("Enable SFX", callback_do_nothing),
        ("CPU Difficulty", callback_do_nothing),
        ("Start Game", screen_game),
        ("Back", screen_localplay)
    ))
    menu.render(DISPLAY, CLOCK)


def screen_gamesetup_2p(from_menu: c4gui.menu) -> None:
    """
    Callback to run the "Game Setup" menu

    from_menu -- The menu used to trigger the callback
    """

    # Make a new Menu and (re-)render all objects
    menu: c4gui.Menu = c4gui.menu.Menu(from_menu.theme, WIDTH, HEIGHT)
    menu.generate((
        ("Enable SFX", callback_do_nothing),
        ("Start Game", screen_game),
        ("Back", screen_localplay)
    ))
    menu.render(DISPLAY, CLOCK)


def screen_gamesetup_0p(from_menu: c4gui.menu) -> None:
    """
    Callback to run the "Game Setup" menu

    from_menu -- The menu used to trigger the callback
    """

    # Make a new Menu and (re-)render all objects
    menu: c4gui.Menu = c4gui.menu.Menu(from_menu.theme, WIDTH, HEIGHT)
    menu.generate((
        ("Enable SFX", callback_do_nothing),
        ("CPU 1 Difficulty", callback_do_nothing),
        ("CPU 2 Difficulty", callback_do_nothing),
        ("Start Game", screen_game),
        ("Back", screen_localplay)
    ))
    menu.render(DISPLAY, CLOCK)


def screen_networkplay(from_menu: c4gui.menu) -> None:
    """
    Callback to run the "Network Game" menu

    from_menu -- The menu used to trigger the callback
    """

    # Make a new Menu and (re-)render all objects
    menu: c4gui.Menu = c4gui.menu.Menu(from_menu.theme, WIDTH, HEIGHT)
    menu.generate((
        ("Host Game", callback_do_nothing),
        ("Join Game", callback_do_nothing),
        ("Back", screen_mainmenu)
    ))
    menu.render(DISPLAY, CLOCK)


def screen_game(from_menu: c4gui.menu) -> None:
    """
    Callback to run a game screen

    from_menu -- The menu used to trigger the callback
    """

    # Render a new game board
    game: c4gui.Game = c4gui.game.Game(from_menu.theme, WIDTH, HEIGHT)
    game.render(DISPLAY, CLOCK, True)


# Entrypoint straight into the main menu
screen_mainmenu()
