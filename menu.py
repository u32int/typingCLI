import curses
import os
from curses import wrapper
import game


class Button:
    def __init__(self, y: int, x: int, text: str, hovering: bool, stdscr) -> None:
        self.y, self.x = y, x
        self.text = text
        self.hovering = hovering
        self.stdscr = stdscr

    def toggle_hover(self):
        self.hovering = not self.hovering
        if self.hovering:
            self.stdscr.addstr(self.y, self.x - int(len(self.text) / 2), self.text, curses.color_pair(2))
        else:
            self.stdscr.addstr(self.y, self.x - int(len(self.text) / 2), self.text, curses.color_pair(1))




def init_menu(stdscr):
    curses.curs_set(0)
    # -- init button colors --
    # normal (not hovering)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # hovering
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # init buttons 
    startGameButton = Button(int(os.get_terminal_size()[1] / 2) - 2, int(os.get_terminal_size()[0] / 2), "Start Game", True, stdscr)
    exitGameButton = Button(int(os.get_terminal_size()[1] / 2) + 1, int(os.get_terminal_size()[0] / 2), "Exit", False, stdscr)

    # buttons are ordered by their actuall screen position - exitGameButton is the lowest on screen for example
    button_array = [exitGameButton, startGameButton]
    curr_hovering = 1
    # place buttons
    stdscr.addstr(startGameButton.y, startGameButton.x - int(len(startGameButton.text) / 2), startGameButton.text, curses.color_pair(2))
    stdscr.addstr(exitGameButton.y, exitGameButton.x - int(len(exitGameButton.text) / 2), exitGameButton.text, curses.color_pair(1))

    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        if key == "KEY_UP":
            if len(button_array) - 1 != curr_hovering:
                button_array[curr_hovering].toggle_hover()
                button_array[curr_hovering + 1].toggle_hover()
                curr_hovering += 1
                pass
            else:
                button_array[curr_hovering].toggle_hover()
                button_array[0].toggle_hover()
                curr_hovering = 0
        if key == "KEY_DOWN":
            if curr_hovering != 0:
                button_array[curr_hovering].toggle_hover()
                button_array[curr_hovering - 1].toggle_hover()
                curr_hovering -= 1
            else:
                button_array[0].toggle_hover()
                button_array[len(button_array) - 1].toggle_hover()
                curr_hovering = len(button_array) - 1
        if key == "\n":
            if button_array[curr_hovering].text == "Start Game":
                curses.curs_set(1)
                game.start_game(stdscr, "english1k")
                init_menu(stdscr)
            if button_array[curr_hovering].text == "Exit":
                exit()

            
wrapper(init_menu)
