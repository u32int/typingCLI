import curses
import time
import random
import os
import postgamescreen


def displayCenterTxt(stdscr, text, color):
    stdscr.addstr(int(os.get_terminal_size()[1]/2), int(os.get_terminal_size()[0]/2) - int(len(text) / 2),
    text, curses.color_pair(color))
    stdscr.refresh()


def get_text_line(wordlist, length):
    return ' '.join([random.choice(wordlist) for _ in range(0, length)])


def start_game(stdscr, wordlist):
    stdscr.clear()
    stdscr.refresh()
    # display word loading message

    # -- color pairs --
    # 1 - incorrect letter/loading message
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    # 2 - correct letter
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    load_text = "Loading words.."
    displayCenterTxt(stdscr, load_text, 1)
    word_list = [word.strip() for word in open("english1k.txt") if len(word) > 1]
       
    
    stats = {
        "mistakes": 0,
        "time": time.time(),
    }


    def game_loop():
        stdscr.clear()

        # generate random "sentence"
        sentence = get_text_line(word_list, 5)

        stdscr.addstr(int(os.get_terminal_size()[1]/2 + 1), int((os.get_terminal_size()[0] - len(sentence))/2), sentence)
        stdscr.move(int(os.get_terminal_size()[1]/2), int((os.get_terminal_size()[0] - len(sentence))/2))
        curr_user_sentence = ""
        while(True):
            key = stdscr.getkey()
            try:
                if len(key) > 1:
                    if key == "KEY_BACKSPACE":
                        if len(curr_user_sentence) > 0 and sentence[len(curr_user_sentence) - 1] != " ":
                            y, x = stdscr.getyx()
                            stdscr.addstr(y, x-1, " ")
                            stdscr.move(y, x-1)
                            curr_user_sentence = curr_user_sentence[:-1:]

                else:
                    if key == "\n":
                        continue

                    if sentence[len(curr_user_sentence)] == " " and key != " ":
                        continue

                    curr_user_sentence += key
                    if curr_user_sentence[len(curr_user_sentence) - 1] == sentence[len(curr_user_sentence) - 1]:
                        stdscr.addstr(f"{key}", curses.color_pair(2))
                    else:
                        stdscr.addstr(f"{key}", curses.color_pair(1))
                        stats["mistakes"] += 1
                    if curr_user_sentence == sentence or len(curr_user_sentence) == len(sentence):
                        break;

            except:
                continue

    rounds = 3
    for _ in range(0, rounds):
        game_loop()

    stats["time"] = round(time.time() - stats["time"], 2)
    postgamescreen.init_postgamescreen(stdscr, stats)
