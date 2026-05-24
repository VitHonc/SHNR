#!/usr/bin/python3

import curses
import random
import json
import math
import time

from pathlib import Path
from game_functions import pop_bullet, pop_redguy, pop_obstcl, disp_level

def game(stdscr,prog):
  try:
  # Setting clear screen and getting dimensions
    stdscr.erase()
    h_win, w_win = stdscr.getmaxyx()
    y_offs,x_offs = int(h_win/2)-int(prog.border_h/2),int(w_win/2)-int(prog.border_w/2)
    if prog.redguy_y == []:
      prog.welc_msg = "SUPER HOT SUPER HOT"
      prog.msg_done = False
  # Small window warning message
    if h_win < prog.border_h+2 or w_win < prog.border_w:
      stdscr.addstr(0,0,"Too\nsmall\nwindow!")
      stdscr.refresh()
      stdscr.getch()
  # Showing the "welcome" message
    if prog.msg_done == False and not prog.welc_msg == "":
      words = prog.welc_msg.split()
      w_y_offs = y_offs + int((prog.border_h/2) - 2.5)
      big_font = json.load(open(Path(__file__).parent / "font" / "big-font.json", "r", encoding="utf-8"))
      for i in range(0,len(words)):
        stdscr.erase()
        w_x_offs = x_offs + int((prog.border_w/2) - (len(words[i])*4.5))
        disp_level(stdscr,prog,y_offs,x_offs)
        for j in range(0,len(words[i])):
          for k in range(0,5): stdscr.addstr(w_y_offs+k,w_x_offs+(j*9),big_font[words[i][j]][k])
        stdscr.noutrefresh()
        curses.doupdate()
        time.sleep(0.35)
      stdscr.erase()
        
    prog.msg_done = True
  # Display the level
    disp_level(stdscr,prog,y_offs,x_offs)
    stdscr.noutrefresh()
    curses.doupdate()
  except curses.error: pass
  if prog.player_l == 0:
    prog.roomdone = 1
    time.sleep(0.5)
    return
  if prog.redguy_y == []:
    prog.roomdone = 2
    return
  # -----------------------------------------------------------
  # SETTING UP NEXT FRAME (Movement, collisions, breaking, ...)
  # -----------------------------------------------------------
  key = stdscr.getch()
  # Clear One-Frame effects
  prog.breaks_y,prog.breaks_x,prog.breaks_c = [],[],[]
  # Player movement and enemy destroying
  # >----------------------------------------------------------
  prog.player_y_todo,prog.player_x_todo = 0,0
  nomove = 0 # 0 do move everything; 1 don't move player only; 2 move nothing
  if   (key == ord('w') or key == curses.KEY_UP)    and prog.player_y > 0:         prog.player_y_todo = -1
  elif (key == ord('s') or key == curses.KEY_DOWN)  and prog.player_y < (h_win-1): prog.player_y_todo =  1
  elif (key == ord('a') or key == curses.KEY_LEFT)  and prog.player_x > 0:         prog.player_x_todo = -1
  elif (key == ord('d') or key == curses.KEY_RIGHT) and prog.player_x < (w_win-1): prog.player_x_todo =  1
  else: nomove = 2
  for i in range(len(prog.redguy_y)-1,-1,-1):
    if prog.player_y + prog.player_y_todo == prog.redguy_y[i] and prog.player_x + prog.player_x_todo == prog.redguy_x[i]:
      pop_redguy(i,prog)
      nomove = 1
  for i in range(len(prog.obstcl_y)-1,-1,-1):
    if prog.player_y + prog.player_y_todo == prog.obstcl_y[i] and prog.player_x + prog.player_x_todo == prog.obstcl_x[i]:
      if prog.obstcl_t[i] == 2:
        pop_obstcl(i,prog)
        nomove = 1
      else: nomove = 2
  if nomove == 0:
    prog.player_y += prog.player_y_todo
    prog.player_x += prog.player_x_todo
  elif nomove == 2: return
  # BULLETS
  # >----------------------------------------------------------
  # Bullet movement
  for i in range(len(prog.bullet_y)-1,-1,-1):
    prog.bullet_x[i] += prog.bullet_h[i]*2
    prog.bullet_y[i] += prog.bullet_v[i]*2
  # Bullet collision
  bull_to_rem,bull_to_rem_oy,bull_to_rem_ox,enem_to_remove,wall_to_remove = [],[],[],[],[]
  prog.player_h = False
  for i in range(0,len(prog.bullet_y)):
    for o in range(3,-1,-1):
      # Enemies
      for j in range(0,len(prog.redguy_y)):
        if i not in bull_to_rem and o <= 2 and j not in enem_to_remove and prog.bullet_y[i]-(prog.bullet_v[i]*o) == prog.redguy_y[j] and prog.bullet_x[i]-(prog.bullet_h[i]*o) == prog.redguy_x[j]:
          bull_to_rem.append(i)
          bull_to_rem_oy.append(prog.bullet_v[i]*(o+1))
          bull_to_rem_ox.append(prog.bullet_h[i]*(o+1))
          enem_to_remove.append(j)
      # Player
      if i not in bull_to_rem and o <= 2 and prog.bullet_y[i]-(prog.bullet_v[i]*o) == prog.player_y and prog.bullet_x[i]-(prog.bullet_h[i]*o) == prog.player_x:
        prog.player_h = True
        bull_to_rem.append(i)
        bull_to_rem_oy.append(prog.bullet_v[i]*(o+1))
        bull_to_rem_ox.append(prog.bullet_h[i]*(o+1))
      # Walls
      for j in range(0,len(prog.obstcl_y)):
        if i not in bull_to_rem and o <= 1 and j not in wall_to_remove and (not prog.obstcl_t[j] == 1) and prog.bullet_y[i]-(prog.bullet_v[i]*o) == prog.obstcl_y[j] and prog.bullet_x[i]-(prog.bullet_h[i]*o) == prog.obstcl_x[j]:
          bull_to_rem.append(i)
          bull_to_rem_oy.append(prog.bullet_v[i]*(o+1))
          bull_to_rem_ox.append(prog.bullet_h[i]*(o+1))
          if prog.obstcl_t[j] == 2: wall_to_remove.append(j)
      # Bullets
      for j in range(0,len(prog.bullet_y)):
        if i not in bull_to_rem and not i == j and prog.bullet_y[i]-(prog.bullet_v[i]*o) == prog.bullet_y[j] and prog.bullet_x[i]-(prog.bullet_h[i]*o) == prog.bullet_x[j]:
          bull_to_rem.append(i)
          bull_to_rem_oy.append(prog.bullet_v[i]*o)
          bull_to_rem_ox.append(prog.bullet_h[i]*o)
  # Removing broken bullets, walls, enemies
  for i in range(len(bull_to_rem)-1,   -1,-1): pop_bullet(bull_to_rem[i],bull_to_rem_oy[i],bull_to_rem_ox[i],prog)
  for i in range(len(enem_to_remove)-1,-1,-1): pop_redguy(enem_to_remove[i],prog)
  for i in range(len(wall_to_remove)-1,-1,-1): pop_obstcl(wall_to_remove[i],prog)
  # ENEMIES
  # >----------------------------------------------------------
  # Choosing enemy to shoot (the closest one on each side)
  best_y_redguy,best_x_redguy = [-1,-1],[-1,-1] # L,R, U,D
  for i in range(0,len(prog.redguy_y)):
    if prog.redguy_l[i] >= prog.gun_load:
      if   prog.redguy_y[i] == prog.player_y and prog.redguy_x[i] < prog.player_x and (best_y_redguy[0] == -1 or (best_y_redguy[0] >= 0 and prog.redguy_x[i] > prog.redguy_x[best_y_redguy[0]])):
        wall = False
        for j in range(0,len(prog.obstcl_y)):
          if prog.redguy_y[i] == prog.obstcl_y[j] and prog.obstcl_t[j] == 0 and prog.redguy_x[i] < prog.obstcl_x[i] < prog.player_x: wall = True
        if wall == False: best_y_redguy[0] = i
      elif prog.redguy_y[i] == prog.player_y and prog.redguy_x[i] > prog.player_x and (best_y_redguy[1] == -1 or (best_y_redguy[1] >= 0 and prog.redguy_x[i] < prog.redguy_x[best_y_redguy[1]])):
        wall = False
        for j in range(0,len(prog.obstcl_y)):
          if prog.redguy_y[i] == prog.obstcl_y[j] and prog.obstcl_t[j] == 0 and prog.redguy_x[i] > prog.obstcl_x[i] > prog.player_x: wall = True
        if wall == False: best_y_redguy[1] = i
      elif prog.redguy_x[i] == prog.player_x and prog.redguy_y[i] < prog.player_y and (best_x_redguy[0] == -1 or (best_x_redguy[0] >= 0 and prog.redguy_y[i] > prog.redguy_y[best_x_redguy[0]])):
        wall = False
        for j in range(0,len(prog.obstcl_y)):
          if prog.redguy_x[i] == prog.obstcl_x[j] and prog.obstcl_t[j] == 0 and prog.redguy_y[i] < prog.obstcl_y[i] < prog.player_y: wall = True
        if wall == False: best_x_redguy[0] = i
      elif prog.redguy_x[i] == prog.player_x and prog.redguy_y[i] > prog.player_y and (best_x_redguy[1] == -1 or (best_x_redguy[1] >= 0 and prog.redguy_y[i] < prog.redguy_y[best_x_redguy[1]])):
        wall = False
        for j in range(0,len(prog.obstcl_y)):
          if prog.redguy_x[i] == prog.obstcl_x[j] and prog.obstcl_t[j] == 0 and prog.redguy_y[i] > prog.obstcl_y[i] > prog.player_y: wall = True
        if wall == False: best_x_redguy[1] = i
  # Enemies shooting
  for d in range(0,2):
    if not best_y_redguy[d] == -1:
      if abs(prog.player_x - prog.redguy_x[best_y_redguy[d]]) > 1:
        prog.redguy_l[best_y_redguy[d]] = 0;
        prog.bullet_v.append(0)
        prog.bullet_h.append(1 if d == 0 else -1)
        prog.bullet_y.append(prog.redguy_y[best_y_redguy[d]])
        prog.bullet_x.append(prog.redguy_x[best_y_redguy[d]]+prog.bullet_h[-1])
      else: prog.player_h = True
    if not best_x_redguy[d] == -1:
      if abs(prog.player_y - prog.redguy_y[best_x_redguy[d]]) > 1:
        prog.redguy_l[best_x_redguy[d]] = 0;
        prog.bullet_v.append(1 if d == 0 else -1)
        prog.bullet_h.append(0)
        prog.bullet_y.append(prog.redguy_y[best_x_redguy[d]]+prog.bullet_v[-1])
        prog.bullet_x.append(prog.redguy_x[best_x_redguy[d]])
      else: prog.player_h = True
  # Enemy movement
  for i in range(0,len(prog.redguy_y)):
    # Enemies can be "static" so they don't move
    if prog.redguy_s[i] == 0:
      # Melee use the shortest path but also do a bit of random moves
      if prog.redguy_l[i] == -1:
        du = math.sqrt(pow(prog.redguy_y[i]-1-prog.player_y,2)+pow(prog.redguy_x[i]  -prog.player_x,2))
        dd = math.sqrt(pow(prog.redguy_y[i]+1-prog.player_y,2)+pow(prog.redguy_x[i]  -prog.player_x,2))
        dl = math.sqrt(pow(prog.redguy_y[i]  -prog.player_y,2)+pow(prog.redguy_x[i]-1-prog.player_x,2))
        dr = math.sqrt(pow(prog.redguy_y[i]  -prog.player_y,2)+pow(prog.redguy_x[i]+1-prog.player_x,2))
        dists = {"du": du, "dd": dd, "dl": dl, "dr": dr}
        # So they don't go into walls...
        for j in range(0,len(prog.obstcl_y)):
          if   prog.redguy_y[i]-1 == prog.obstcl_y[j] and prog.redguy_x[i]   == prog.obstcl_x[j]: del dists["du"]
          elif prog.redguy_y[i]+1 == prog.obstcl_y[j] and prog.redguy_x[i]   == prog.obstcl_x[j]: del dists["dd"]
          elif prog.redguy_y[i]   == prog.obstcl_y[j] and prog.redguy_x[i]-1 == prog.obstcl_x[j]: del dists["dl"]
          elif prog.redguy_y[i]   == prog.obstcl_y[j] and prog.redguy_x[i]+1 == prog.obstcl_x[j]: del dists["dr"]
        #  or other enemies
        for j in range(0,len(prog.redguy_y)):
          if   prog.redguy_y[i]-1 == prog.redguy_y[j] and prog.redguy_x[i]   == prog.redguy_x[j] and "du" in dists: del dists["du"]
          elif prog.redguy_y[i]+1 == prog.redguy_y[j] and prog.redguy_x[i]   == prog.redguy_x[j] and "dd" in dists: del dists["dd"]
          elif prog.redguy_y[i]   == prog.redguy_y[j] and prog.redguy_x[i]-1 == prog.redguy_x[j] and "dl" in dists: del dists["dl"]
          elif prog.redguy_y[i]   == prog.redguy_y[j] and prog.redguy_x[i]+1 == prog.redguy_x[j] and "dr" in dists: del dists["dr"]
        if not dists == {}:
          ds = sorted(dists.items(), key=lambda x: x[1])
          if ds[0][1] < 0.1:                 prog.player_h = True
          else:
            if len(ds) >= 2 and abs(ds[0][1]-ds[1][1]) < 1.5: shortest = ds[random.randint(0,1)][0]
            else:                                             shortest = ds[0][0]
            match(shortest):
              case "du": prog.redguy_y[i] -=1
              case "dd": prog.redguy_y[i] +=1
              case "dl": prog.redguy_x[i] -=1
              case "dr": prog.redguy_x[i] +=1
      # Ranged try to align in-line with player and then approach straight, but they don't come too close
      elif prog.redguy_l[i] > 0:
        du = abs(prog.redguy_y[i]-1-prog.player_y)
        dd = abs(prog.redguy_y[i]+1-prog.player_y)
        dl = abs(prog.redguy_x[i]-1-prog.player_x)
        dr = abs(prog.redguy_x[i]+1-prog.player_x)
        dists = {"du": du, "dd": dd, "dl": dl, "dr": dr}
        for j in range(0,len(prog.obstcl_y)):
          if "du" in dists and (prog.redguy_y[i] == prog.player_y or (prog.redguy_y[i]-1 == prog.obstcl_y[j] and prog.redguy_x[i]   == prog.obstcl_x[j])): del dists["du"]
          if "dd" in dists and (prog.redguy_y[i] == prog.player_y or (prog.redguy_y[i]+1 == prog.obstcl_y[j] and prog.redguy_x[i]   == prog.obstcl_x[j])): del dists["dd"]
          if "dl" in dists and (prog.redguy_x[i] == prog.player_x or (prog.redguy_y[i]   == prog.obstcl_y[j] and prog.redguy_x[i]-1 == prog.obstcl_x[j])): del dists["dl"]
          if "dr" in dists and (prog.redguy_x[i] == prog.player_x or (prog.redguy_y[i]   == prog.obstcl_y[j] and prog.redguy_x[i]+1 == prog.obstcl_x[j])): del dists["dr"]
        for j in range(0,len(prog.redguy_y)):
          if   prog.redguy_y[i]-1 == prog.redguy_y[j] and prog.redguy_x[i]   == prog.redguy_x[j] and "du" in dists: del dists["du"]
          elif prog.redguy_y[i]+1 == prog.redguy_y[j] and prog.redguy_x[i]   == prog.redguy_x[j] and "dd" in dists: del dists["dd"]
          elif prog.redguy_y[i]   == prog.redguy_y[j] and prog.redguy_x[i]-1 == prog.redguy_x[j] and "dl" in dists: del dists["dl"]
          elif prog.redguy_y[i]   == prog.redguy_y[j] and prog.redguy_x[i]+1 == prog.redguy_x[j] and "dr" in dists: del dists["dr"]
        if not dists == {}:
          ds = sorted(dists.items(), key=lambda x: x[1])
          if pow(prog.redguy_y[i]-1-prog.player_y,2)+pow(prog.redguy_x[i]-prog.player_x,2) > 9:
            match(ds[0][0]):
              case "du": prog.redguy_y[i] -= 1
              case "dd": prog.redguy_y[i] += 1
              case "dl": prog.redguy_x[i] -= 1
              case "dr": prog.redguy_x[i] += 1
  # OTHER
  # >----------------------------------------------------------
  # Decreasing player lifes if hit by anything previously
  if prog.player_h == True: prog.player_l -= 1
  # Enemies loading guns (if not melee)
  for i in range(0,len(prog.redguy_y)):
    if prog.redguy_l[i] < prog.gun_load and prog.redguy_l[i] > -1: prog.redguy_l[i] += 1
