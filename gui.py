#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import c4utils
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

    # TODO - Remove this callback when development is done
    c4gui.sfx.play("invalid")


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
        ("Start Game", screen_game, (c4gui.game.GameType.SINGLE,)),
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
        ("Start Game", screen_game, (c4gui.game.GameType.DOUBLE,)),
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
        ("Start Game", screen_game, (c4gui.game.GameType.SPECTATE,)),
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


def player_event(from_game: c4gui.game, p1turn: bool, column: int) -> bool:
    """
    Callback to handle a player's move

    from_menu -- The menu used to trigger the callback
    p1turn -- True if it's player 1's turn; False if it's player 2's turn
    column -- The attempted player column

    Returns a boolean of the move's legality
    """

    # Grab the board details
    board = from_game.get_boards()[-1]
    maximum: c4gui.Coordinates = c4utils.get_board_maximums(board)

    # Verify move legality
    if column not in range(maximum.x) or c4utils.check_if_column_full(board, column):
        return False

    # Update the board
    for i in range(maximum.y-1, -1, -1):
        if board[i][column] == " ":
            board[i][column] = "X" if p1turn else "O"
            break
    from_game.update_board(board)

    # Check for an end condition
    if c4utils.check_win(board):
        from_game.set_winner(c4gui.game.Winner.P1 if p1turn else c4gui.game.Winner.P2)

    if c4utils.check_if_board_full(board):
        from_game.set_winner(c4gui.game.Winner.TIE)

    return True


def screen_game(from_menu: c4gui.menu, game_type: int) -> None:
    """
    Callback to run a game screen

    from_menu -- The menu used to trigger the callback
    """

    # Establish player parameters
    # TODO - Figure out where the user can input these
    players: c4gui.Players = c4gui.Players(p1_name="Player 1",
                                        p1_color=c4gui.styles.COLOR_RED,
                                        p2_name="Player 2",
                                        p2_color=c4gui.styles.COLOR_YELLOW)

    # Play the start sound and render a new game board
    c4gui.sfx.play("start")
    game: c4gui.Game = c4gui.game.Game(game_type, from_menu.theme, WIDTH, HEIGHT, players)
    game.render(DISPLAY, CLOCK, True, player_event, screen_mainmenu)


# Entrypoint straight into the main menu
screen_mainmenu()
