
Connect 4
======
[**Connect 4**](https://en.wikipedia.org/wiki/Connect_Four) is a two-player connection board game, in which the players choose a color and then take turns dropping colored discs ("tokens") into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.

This project is developed in Python, utilizing PyGame3, specifically for CSE550: Software Engineering.

#### Screenshots

##### Main Menu

Each of the menu options leads to game settings menus, and a game is created when "Start Game" is pressed.

![1](https://imgur.com/yxuyN4F.png "Main Menu")

##### Game Screen

Human moves are accomplished with the mouse movements. A token is dropped after a mouse click. Computer opponents automatically move. The game ends in a "win" when four of a players tokens line up vertically, horizontally, or diagonally, and the game ends in a "tie" when there are no valid moves left on the grid.

![2](https://imgur.com/XLp0hgE.png "Game Screen")

##### Game Review Screen

After finishing the game, each turn may be reviewed by clicking on the navigation icons at the bottom. Alternatively, the game can be closed by clicking "Exit" in the top right to return to the main menu.

![3](https://imgur.com/2bckPot.png "Review Screen")

## Features
* Create 0-player game with "0" or "random" CPU difficulty
	* Show users every turn on a realistic, full-screen GUI
	* Alert users of illegal/invalid moves
	* Announce when a player wins or ties
	* Can "record" or "step-through" each state or move of the game and "review" a match's entire move sequence
* Create 1-player game (human v. CPU)
* Create local 2-player game (human v. human)
* Create remote 2-player game through remote network LAN play
* Quit the game entirely with Esc or Alt+F4
* Hear sound effects with button events
* Switch between light mode and dark mode

## To-Do

## Download
* [Latest release (v1.0)](https://github.com/Ap3x/connect4/archive/master.zip) (Stable)
* [Latest dev build (v1.0.1)](https://github.com/Ap3x/connect4/archive/develop.zip) (Experimental)

## Setup

### Windows
Install Python3 (any version >= 3.4):
https://www.python.org/downloads/

Install PyGame:
https://www.pygame.org/wiki/GettingStarted

In order to ensure that you have all the required packages, please install the packages as listed below:

```shell
$ py -m pip install -r requirements.txt
```

### Linux
In order to ensure that you have all the required packages, please install the packages as listed below:

```shell
$ pip install -r requirements.txt
$ sudo apt install python3-pygame
```

## Usage
Once in the source directory, run the following command to execute the program:

```
$ python ./connect4.py
```

## License
[MIT](https://github.com/Ap3x/connect4/blob/master/LICENSE.md)
