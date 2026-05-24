#!/usr/bin/python3

import curses
import sys

from data import Program
from menu import menu

prog = Program()

def main(stdscr):
  # Setting curses
  curses.start_color()
  curses.use_default_colors()  
  curses.curs_set(0)
  stdscr.keypad(True)
  # Defining colors
  curses.init_pair(1, curses.COLOR_WHITE, -1)
  curses.init_pair(2, curses.COLOR_RED,   -1)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
  stdscr.clear()
  # Launching the loop
  while True: menu(stdscr,prog)

if __name__ == "__main__":
  try: curses.wrapper(main)
  except KeyboardInterrupt: sys.exit(0)
