import curses
import game

def init_postgamescreen(stdscr, stats):
    stdscr.clear()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    
    game.displayCenterTxt(stdscr, f"mistakes: {stats['mistakes']} time: {stats['time']}s ", 1)
    stdscr.getch()
    stdscr.clear()
