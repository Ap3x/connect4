#!/usr/bin/python3
# -*- coding: utf8 -*-

import c4gui
import c4utils

def test_should_return_true_if_column_is_full() -> None:
    board = [["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", "O", "O", " ", " ", " "],
	["X", "X", "X", "X", "O", " ", " "]]
    col = 0
    assert True == c4utils.check_if_column_full(board, col)


def test_should_return_false_if_column_is_not_full() -> None:
    board = [[" ", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", "O", "O", " ", " ", " "],
	["X", "X", "X", "X", "O", " ", " "]]
    col = 0
    assert False == c4utils.check_if_column_full(board, col)


def test_should_return_true_if_board_is_full() -> None:
    board = [["X" for i in range(c4gui.MAX_COLS)] for i in range(c4gui.MAX_ROWS)]
    assert True == c4utils.check_if_board_full(board)


def test_should_return_false_if_board_is_not_full() -> None:
    board = [[" " for i in range(c4gui.MAX_COLS)] for i in range (c4gui.MAX_ROWS)]
    assert False == c4utils.check_if_board_full(board)


def test_should_win_for_horizontal() -> None:
    board = [[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", "O", "O", " ", " ", " "],
	["X", "X", "X", "X", "O", " ", " "]]
    assert True == c4utils.check_win(board)


def test_should_win_for_vertical() -> None:
    board = [[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", " ", " ", " ", " ", " "],
	["X", " ", "O", "O", "O", " ", " "]]
    assert True == c4utils.check_win(board)


def test_should_win_for_diagonal() -> None:
    board = [[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", "O", " ", " ", " ", " ", " "],
	[" ", "O", "O", " ", " ", " ", " "],
	[" ", "X", "O", "O", " ", " ", " "],
	[" ", "X", "X", "X", "O", "X", "X"]]
    assert True == c4utils.check_win(board)


def test_should_not_win_for_no_4_in_a_row() -> None:
    board = [[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", " ", " ", " ", " ", " "],
	[" ", " ", "O", "O", " ", " ", " "],
	[" ", "X", "X", "X", "O", " ", " "]]
    assert False == c4utils.check_win(board)


if __name__ == "__main__":
    test_should_return_true_if_column_is_full()
    test_should_return_false_if_column_is_not_full()
    test_should_return_true_if_board_is_full()
    test_should_return_false_if_board_is_not_full()
    test_should_win_for_horizontal()
    test_should_win_for_vertical()
    test_should_win_for_diagonal()
    test_should_not_win_for_no_4_in_a_row()
    print("PASS, 0 failures")
