#!/usr/bin/python3

import curses
import random
import json
import sys
import os

from pathlib        import Path
from menu_functions import play_level, play_node, draw_menu, list_files

options = [("shnr.exe","Start where you last ended"          ),
           ("Levels",  "Browse and start levels"             ),
           ("Nodes",   "Run multiple levels in succession"   ),
           ("Infinite","Ever-respawning enemies in one level"),
           ("Endless", "Run never-ending node util death"    ),
           ("exit.exe","Exit the game"                       )]

selected = 0

def menu(stdscr,prog):
  global selected
  try:
    stdscr.erase()
    h_win, w_win = stdscr.getmaxyx()
    y_offs = int(h_win/2-6)
    x_offs = int(w_win/2-19)
    draw_menu(stdscr,h_win,y_offs,x_offs,12,38,f" NAME{22*' '}| SIZE")
    for i in range(0,len(options)): stdscr.addstr(y_offs+3+i,x_offs+1,options[i][0]+" "*(27-len(options[i][0])),curses.color_pair(3 if selected == i else 1))
    stdscr.addstr(y_offs+3,x_offs+29,f"{int(sum(f.stat().st_size for f in Path(Path(__file__).parent).iterdir() if f.is_file())/100)/10} kB")
    stdscr.addstr(y_offs+4,x_offs+29,f"{len([f for f in os.listdir(Path(__file__).parent / 'levels') if os.path.isfile(os.path.join(Path(__file__).parent / 'levels',f)) and f.endswith('.json')])} files")
    stdscr.addstr(y_offs+5,x_offs+29,f"{len([f for f in os.listdir(Path(__file__).parent / 'nodes')  if os.path.isfile(os.path.join(Path(__file__).parent / 'nodes', f)) and f.endswith('.json')])} files")
    stdscr.addstr(y_offs+6,x_offs+29,f"{sum(f.stat().st_size for f in Path(Path(__file__).parent / 'levels').iterdir() if f.is_file())} B")
    stdscr.addstr(y_offs+7,x_offs+29,f"{sum(f.stat().st_size for f in Path(Path(__file__).parent / 'nodes' ).iterdir() if f.is_file())} B")
    stdscr.addstr(y_offs+8,x_offs+29,f"{os.path.getsize(Path(__file__).parent / 'main.py')} B")
    stdscr.addstr(y_offs+10,x_offs+1,options[selected][1])
    stdscr.noutrefresh()
    curses.doupdate()
  except curses.error: pass

  key = stdscr.getch()
  if   key in (curses.KEY_UP,   ord("w")): selected = (selected-1)%6
  elif key in (curses.KEY_DOWN, ord("s")): selected = (selected+1)%6
  elif key in (curses.KEY_ENTER,10,13,ord(" ")):
    match(selected):
      case 0:
        node = json.load(open(Path(__file__).parent / "other" / "last_file.json",     "r",encoding="utf-8"))
        if node["node"]: play_node(f"{Path(__file__).parent / "nodes" / node["node"]}.json",node["level"],stdscr,prog)
      case 1:
        path = list_files(stdscr,y_offs,x_offs,h_win,"levels",False)
        while path:
          play_level(path,stdscr,prog,0)
          if prog.roomdone == 2: break
      case 2:
        path = list_files(stdscr,y_offs,x_offs,h_win,"nodes",False)
        if path: play_node(path,0,stdscr,prog)
      case 3: pass
      case 4:
        path = list_files(stdscr,y_offs,x_offs,h_win,"levels",True)
        prog.player_l = 1
        prog.roomdone = 0
        while not (prog.roomdone == 1 or path == []): play_level(f"{path[random.randint(0,len(path)-1)]}",stdscr,prog,2)
      case 5: sys.exit(0)
