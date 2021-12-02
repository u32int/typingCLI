from curses import wrapper
import menu

def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Launch into menu
    menu.init_menu(stdscr)


wrapper(main)
