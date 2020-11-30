#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import c4utils
import pygame
import network

# Establish the entire screen as the primary surface and prepare the clock
screen: pygame.display = pygame.display.Info()
HEIGHT: int = int(screen.current_h / c4gui.SCALE_MODIFIER)
WIDTH: int = int(screen.current_w / c4gui.SCALE_MODIFIER)
DISPLAY: pygame.display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
CLOCK: pygame.time.Clock = pygame.time.Clock()


def screen_menu(start_at: int = c4gui.menu.SubMenu.MAIN) -> None:
    """
    Self-runnable or callback to run the menu loops

    start_at -- The optional submenu to start at
    """

    # Make a new Menu and render all objects
    menu = c4gui.menu.Menu(WIDTH, HEIGHT, start_at, screen_game)
    menu.render(DISPLAY, CLOCK)


def move_end_event(from_game: c4gui.game.Game, board: [[]], p1turn: bool) -> None:
    """
    Callback event for the end of each player's turn
    from_menu -- The menu used to trigger the callback
    board -- The board state
    p1turn -- True if it's player 1's turn; False if it's player 2's turn
    """

    if c4utils.check_win(board):
        from_game.set_winner(c4gui.game.Winner.P1 if p1turn else c4gui.game.Winner.P2)

    if c4utils.check_if_board_full(board):
        from_game.set_winner(c4gui.game.Winner.TIE)

    pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"user_type": "GAME_END"}))


def player_event(from_game: c4gui.game.Game, p1turn: bool, column: int) -> bool:
    """
    Callback to handle a player's move

    from_menu -- The menu used to trigger the callback
    p1turn -- True if it's player 1's turn; False if it's player 2's turn
    column -- The attempted player column

    Returns a boolean of the move's legality
    """

    # Grab the board details
    board = from_game.get_boards()[-1]

    # Verify move legality
    if column not in range(c4gui.MAX_COLS) or c4utils.check_if_column_full(board, column):
        return False

    # Update the board
    for i in range(c4gui.MAX_ROWS-1, -1, -1):
        if board[i][column] == " ":
            board[i][column] = "X" if p1turn else "O"
            break
    from_game.update_board(board)

    # Check for an end condition
    move_end_event(from_game, board, p1turn)

    return True


def computer_event(from_game: c4gui.game.Game, p1turn: bool) -> None:
    """
    Callback to handle a computer's move

    from_menu -- The menu used to trigger the callback
    p1turn -- True if it's player 1's turn; False if it's player 2's turn
    """

    board = from_game.get_boards()[-1]
    if from_game.game_type == c4gui.game.GameType.SINGLE:
        section = "Computer0"
    elif from_game.game_type == c4gui.game.GameType.SPECTATE:
        section = "Computer1" if p1turn else "Computer2"
    else:
        raise ValueError("computer event is invalid for game type")

    difficulty: int = c4gui.config.get(section, "difficulty", int)
    turn_num: int = len(from_game.boards)

    if difficulty < 3:
        c4utils.cpu_algorithm_easy(board, "X" if p1turn else "O")
    elif difficulty < 6:
        c4utils.cpu_algorithm_hard(board, "X" if p1turn else "O", 2)
    elif difficulty < 9 or turn_num < 18:
        c4utils.cpu_algorithm_hard(board, "X" if p1turn else "O", 4)
    else:
        c4utils.cpu_algorithm_hard(board, "X" if p1turn else "O", 6)
    from_game.update_board(board)
    move_end_event(from_game, board, p1turn)


def screen_game(from_menu: c4gui.menu, game_type: int, net: network.Network = None) -> None:
    """
    Callback to run a game screen

    from_menu -- The menu used to trigger the callback
    """

    # Play the start sound and render a new game board
    c4gui.sfx.play("start")
    game: c4gui.Game = c4gui.game.Game(game_type, from_menu.theme, WIDTH, HEIGHT, net)
    game.render(DISPLAY, CLOCK, True, c4gui.MoveCallbacks(human=player_event, computer=computer_event), screen_menu)


# Entrypoint straight into the main menu
if __name__ == "__main__":
    screen_menu()
