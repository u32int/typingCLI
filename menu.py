import curses
import os
from curses import wrapper
import game


class Button:
    def __init__(self, y: int, x: int, text: str, stdscr) -> None:
        self.y, self.x = y, x
        self.text = text
        self.stdscr = stdscr
        self.hovering = False

    def place(self):
        self.stdscr.addstr(self.y, self.x - int(len(self.text) / 2), self.text, curses.color_pair(int(self.hovering) + 1))

    def toggle_hover(self):
        self.hovering = not self.hovering
        self.place()


class OptionButton(Button):
    def config(self, options):
        self.options = options
        self.curr_option = 0

    def cycle_options(self, direction):
        if direction == "left" and self.curr_option != 0:
            self.curr_option -= 1
        if direction == "right" and self.curr_option != len(self.options) - 1:
            self.curr_option += 1

        self.place()

    def place(self):
        self.text = self.options[self.curr_option]

        if self.curr_option != 0:
            self.text = "< " + self.text
        if self.curr_option != len(self.options) + 1:
            self.text = self.text + " >"

        # clear what is left of the other button
        self.stdscr.addstr(self.y, self.x - int((len(max(self.options)) + 8) / 2), " " * (len(max(self.options)) + 8), curses.color_pair(1))

        # place the button
        self.stdscr.addstr(self.y, self.x - int(len(self.text) / 2), self.text, curses.color_pair(int(self.hovering) + 1))


            


def init_menu(stdscr):
    curses.curs_set(0)
    # -- init button colors --
    # normal (not hovering)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # hovering
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # init buttons 
    # normal buttons
    startGameButton = Button(int(os.get_terminal_size()[1] / 2) - 2, int(os.get_terminal_size()[0] / 2), "Start Game", stdscr)
    exitGameButton = Button(int(os.get_terminal_size()[1] / 2) + 2, int(os.get_terminal_size()[0] / 2), "Exit", stdscr)
    # option buttons
    wordlistButton = OptionButton(int(os.get_terminal_size()[1] / 2), int(os.get_terminal_size()[0] / 2), "", stdscr)
    wordlistButton.config(["english1k.txt", "english100.txt", "polish100.txt"])


    # buttons are ordered by their actuall screen position - exitGameButton is the lowest on screen for example
    button_array = [exitGameButton, wordlistButton,startGameButton]
    curr_hovering = len(button_array) - 1
    button_array[curr_hovering].toggle_hover()

    # place buttons
    startGameButton.place()
    wordlistButton.place()
    exitGameButton.place()

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

        if key == "KEY_LEFT":
            if button_array[curr_hovering] == wordlistButton:
                wordlistButton.cycle_options("left")

        if key == "KEY_RIGHT":
            if button_array[curr_hovering] == wordlistButton:
                wordlistButton.cycle_options("right")

        if key == "\n":
            if button_array[curr_hovering].text == "Start Game":
                curses.curs_set(1)
                game.start_game(stdscr, "wordlists/" + wordlistButton.options[wordlistButton.curr_option], 3)
                init_menu(stdscr)
            if button_array[curr_hovering].text == "Exit":
                exit()

            
wrapper(init_menu)
