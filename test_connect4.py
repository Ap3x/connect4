#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import pygame
import connect4

WIDTH = connect4.WIDTH
HEIGHT = connect4.HEIGHT

def test_should_quit_game() -> None:
    menu = c4gui.menu.Menu(c4gui.styles.THEME_LIGHT, WIDTH, HEIGHT)
    assert pygame.event.post(pygame.event.Event(pygame.QUIT, {})) == connect4.callback_quit_game(menu)


def test_should_do_nothing() -> None:
    menu = c4gui.menu.Menu(c4gui.styles.THEME_LIGHT, WIDTH, HEIGHT)
    assert c4gui.sfx.play("invalid") == connect4.callback_do_nothing(menu)


def test_should_set_winner_to_p1_on_move_end_event() -> None:
    game: c4gui.Game = c4gui.game.Game(0, c4gui.styles.THEME_LIGHT, WIDTH, HEIGHT, 0)
    board = [["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", "O", "O", " ", " ", " "],
	["X", "X", "X", "X", "O", " ", " "]]
    p1turn = True
    assert game.set_winner(c4gui.game.Winner.P1) == connect4.move_end_event(game, board, p1turn)


def test_should_set_winner_to_p2_on_move_end_event() -> None:
    game: c4gui.Game = c4gui.game.Game(0, c4gui.styles.THEME_LIGHT, WIDTH, HEIGHT, 0)
    board = [["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", "O", "O", " ", " ", " "],
	["X", "X", "X", "X", "O", " ", " "]]
    p1turn = False
    assert game.set_winner(c4gui.game.Winner.P2) == connect4.move_end_event(game, board, p1turn)


def test_should_set_winner_to_tie_on_move_end_event() -> None:
    game: c4gui.Game = c4gui.game.Game(0, c4gui.styles.THEME_LIGHT, WIDTH, HEIGHT, 0)
    board = [["X", "X", "O", "X", "O", "O", "O"],
	["O", "O", "X", "O", "O", "X", "X"],
	["X", "X", "O", "O", "X", "O", "X"],
	["O", "X", "X", "X", "O", "X", "O"],
	["X", "O", "O", "X", "X", "X", "O"],
	["X", "O", "X", "O", "O", "O", "X"]]
    p1turn = True
    assert game.set_winner(c4gui.game.Winner.TIE) == connect4.move_end_event(game, board, p1turn)


def test_should_handle_players_move_if_column_is_not_full() -> None:
    game: c4gui.Game = c4gui.game.Game(0, c4gui.styles.THEME_LIGHT, WIDTH, HEIGHT, 0)
    game.update_board([[" ", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", "O", "O", " ", " ", " "],
	["X", "X", "X", "X", "O", " ", " "]])
    p1turn = True
    column = 0
    assert True == connect4.player_event(game, p1turn, column)


def test_should_not_handle_players_move_if_column_is_full() -> None:
    game: c4gui.Game = c4gui.game.Game(0, c4gui.styles.THEME_LIGHT, WIDTH, HEIGHT, 0)
    game.update_board([["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", "O", "O", " ", " ", " "],
	["X", "X", "X", "X", "O", " ", " "]])
    p1turn = True
    column = 0
    assert False == connect4.player_event(game, p1turn, column)


if __name__ == "__main__":
    test_should_quit_game()
    test_should_do_nothing()
    test_should_set_winner_to_p1_on_move_end_event()
    test_should_set_winner_to_p2_on_move_end_event()
    test_should_set_winner_to_tie_on_move_end_event()
    test_should_handle_players_move_if_column_is_not_full()
    test_should_not_handle_players_move_if_column_is_full()
    print("PASS, 0 failures")
