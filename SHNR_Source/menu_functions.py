#!/usr/bin/python3

import curses
import json
import os
from pathlib import Path
from game    import game

def play_level(f,stdscr,prog, node):
    level = json.load(open(f,"r",encoding="utf-8"))
    # All those variables have default values that are used if value is not specified in map file
    prog.obstcl_y = level.get("obstcl_y", [])
    prog.obstcl_x = level.get("obstcl_x", [])
    prog.obstcl_t = level.get("obstcl_t", [])

    prog.border_h = level.get("border_h", 15)
    prog.border_w = level.get("border_w", 30)
    prog.welc_msg = level.get("welc_msg", "")

    prog.redguy_y = level.get("redguy_y", [])
    prog.redguy_x = level.get("redguy_x", [])
    prog.redguy_l = level.get("redguy_l", [])
    prog.redguy_s = level.get("redguy_s", [])

    prog.player_y = level.get("player_y", 2)
    prog.player_x = level.get("player_x", 2)

    prog.gun_load = level.get("gun_load", 5)
    # The next two variable groups are auto-generated, but you can still set them
    prog.bullet_y = level.get("bullet_y", [])
    prog.bullet_x = level.get("bullet_x", [])
    prog.bullet_h = level.get("bullet_h", [])
    prog.bullet_v = level.get("bullet_v", [])
    # No idea why anyone would need this, but I want maps fully customizable
    prog.breaks_y = level.get("breaks_y", [])
    prog.breaks_x = level.get("breaks_x", [])
    prog.breaks_c = level.get("breaks_c", [])
    # For nodes, map files can specify whether set full lifes when map starts (never happens in Endless)
    if (level.get("reset_hp", False) == True and node == 1) or node == 0: prog.player_l = level.get("player_l", 1)
    # Unsettable in the file
    prog.player_h = False
    prog.roomdone = 0
    prog.msg_done = False
    prog.map_name = Path(f).stem
    # Making walls from borders
    for i in range(0,prog.border_h):
      prog.obstcl_y.append(i)
      prog.obstcl_x.append(0)
      prog.obstcl_t.append(0)
      prog.obstcl_y.append(i)
      prog.obstcl_x.append(prog.border_w-1)
      prog.obstcl_t.append(0)
    for i in range(0,prog.border_w):
      #if not (0 in prog.obstcl_y and prog.border_w-1 in prog.obstcl_y and i in prog.obstcl_x):
      prog.obstcl_y.append(0)
      prog.obstcl_x.append(i)
      prog.obstcl_t.append(0)
      prog.obstcl_y.append(prog.border_h-1)
      prog.obstcl_x.append(i)
      prog.obstcl_t.append(0)
    # Run the level from created variables
    while prog.roomdone == 0: game(stdscr,prog)

def play_node(file,start,stdscr,prog):
  last_f = json.load(open(Path(__file__).parent / "other" / "last_file.json","r",encoding="utf-8"))
  levels = json.load(open(file,"r",encoding="utf-8")).get("run", [])
  dosave = json.load(open(file,"r",encoding="utf-8")).get("dosave", False)
  if not dosave: start = 0
  i = start
  last_f["node"] = Path(file).stem
  while i < len(levels):
    if dosave: start = i
    last_f["level"] = i
    json.dump(last_f,open(Path(__file__).parent / "other" / "last_file.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
    play_level(Path(__file__).parent / "levels" / f"{levels[i]}.json",stdscr,prog,0 if i==start else 1)
    i+=1
    if prog.roomdone == 1: i = start

def draw_menu(stdscr,h_win, y, x, height, width,text):
  TL,TR,BL,BR,H,V = "┌","┐","└","┘","─","│"
  try:
    stdscr.addstr(y, x, TL + H * (width - 2) + TR)
    for i in range(1, height - 1): stdscr.addstr(y + i, x, V + " " * (width - 2) + V)
    stdscr.addstr(y + height - 1, x, BL + H * (width - 2) + BR)
    stdscr.addstr(y+2,x+1,"─"*36)
    stdscr.addstr(y+9,x+1,"─"*36)
    for i in range(3,9): stdscr.addstr(y+i,x+28,"│")
    stdscr.addstr(y+1,x+1,text)
    stdscr.addstr(h_win-2,1,"SHNR v0.11 (22. May 2026)")
  except curses.error: pass

def list_files(stdscr,y_offs,x_offs,h_win,directory,select):
  directory = Path(__file__).parent / directory
  files = sorted([f for f in os.listdir(directory) if f.endswith('.json')])
  if not files: return
  if select: files.append("Start run_____")
  selected_idx = 0
  scroll_offset = 0
  chosen = []

  while True:
    stdscr.erase()
    draw_menu(stdscr,h_win, y_offs, x_offs, 12, 38, f" NAME{22*' '}| SIZE")

    for i in range(6):
      file_idx = scroll_offset + i
      if file_idx < len(files):
        if select and not files[file_idx] == "Start run_____": stdscr.addstr(y_offs+3+i,x_offs+1,f"[{'*' if files[file_idx] in chosen else ' '}] {files[file_idx][:-5]}{' '*(28-len(files[file_idx]))}",curses.color_pair(3 if file_idx == selected_idx else 1))
        else:      stdscr.addstr(y_offs+3+i,x_offs+1,f"{files[file_idx][:-5]}{' '*(32-len(files[file_idx]))}",curses.color_pair(3 if file_idx == selected_idx else 1))
        stdscr.addstr(y_offs+3+i,x_offs+29,f"{os.path.getsize(os.path.join(directory, files[file_idx])) if not files[file_idx] == 'Start run_____' else 4} B")
    if not files[selected_idx] == "Start run_____": stdscr.addstr(y_offs+10,x_offs+1,f"Author: {json.load(open(directory / files[selected_idx], "r", encoding="utf-8")).get("author", "<unknown>")}")
    key = stdscr.getch()
    if key == ord('q'): return
    elif key in (curses.KEY_UP,ord('w')):
      if selected_idx > 0:
        selected_idx -= 1
        if selected_idx < scroll_offset: scroll_offset = selected_idx
    elif key in (curses.KEY_DOWN,ord('s')):
      if selected_idx < len(files) - 1:
        selected_idx += 1
        if selected_idx >= scroll_offset + 10: scroll_offset = selected_idx - 10 + 1
    elif key in (curses.KEY_ENTER,10,13,ord(" ")):
      if not select:                                return os.path.join(directory, files[selected_idx])
      elif files[selected_idx] == "Start run_____": return chosen
      elif files[selected_idx] in chosen:           chosen.remove(files[selected_idx])
      else:                                         chosen.append(files[selected_idx])
    stdscr.noutrefresh()
    curses.doupdate()
