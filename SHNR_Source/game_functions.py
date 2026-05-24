#!/usr/bin/python3

import curses

def pop_bullet(i,o_y,o_x,prog):
  prog.breaks_y.append(prog.bullet_y[i]-o_y)
  prog.breaks_x.append(prog.bullet_x[i]-o_x)
  prog.breaks_c.append(2)
  prog.bullet_y.pop(i)
  prog.bullet_x.pop(i)
  prog.bullet_h.pop(i)
  prog.bullet_v.pop(i)

def pop_redguy(i,prog):
  prog.breaks_y.append(prog.redguy_y[i])
  prog.breaks_x.append(prog.redguy_x[i])
  prog.breaks_c.append(2)
  prog.redguy_y.pop(i)
  prog.redguy_x.pop(i)
  prog.redguy_l.pop(i)
  prog.redguy_s.pop(i)

def pop_obstcl(i,prog):
  prog.breaks_y.append(prog.obstcl_y[i])
  prog.breaks_x.append(prog.obstcl_x[i])
  prog.breaks_c.append(1)
  prog.obstcl_y.pop(i)
  prog.obstcl_x.pop(i)
  prog.obstcl_t.pop(i)

def disp_level(stdscr,prog,y_offs,x_offs):
  stdscr.addstr(prog.player_y+y_offs,prog.player_x+x_offs,"@" if prog.player_l > 0 else "X",curses.color_pair(2 if prog.player_h == True and prog.player_l > 0 else 1)) # Player
  for i in range(0,len(prog.breaks_y)):       stdscr.addstr(prog.breaks_y[i]+y_offs,prog.breaks_x[i]+x_offs,"X",curses.color_pair(prog.breaks_c[i] if prog.player_h == False and prog.msg_done == True else 2)) # Shatter particles
  for i in range(0,len(prog.redguy_y)):                                                                                                                           # Enemies
    if  (prog.redguy_l[i] == -1):             stdscr.addstr(prog.redguy_y[i]+y_offs,prog.redguy_x[i]+x_offs,"M",curses.color_pair(2))
    elif(prog.redguy_l[i] >= prog.gun_load):  stdscr.addstr(prog.redguy_y[i]+y_offs,prog.redguy_x[i]+x_offs,"@",curses.color_pair(2))
    else:                                     stdscr.addstr(prog.redguy_y[i]+y_offs,prog.redguy_x[i]+x_offs,"O",curses.color_pair(2))
  for i in range(0,len(prog.obstcl_y)):                                                                                                                           # Walls
    if   prog.obstcl_t[i] == 0:               stdscr.addstr(prog.obstcl_y[i]+y_offs,prog.obstcl_x[i]+x_offs,"█",curses.color_pair(1 if prog.player_h == False and prog.msg_done == True else 2))
    elif prog.obstcl_t[i] == 1:               stdscr.addstr(prog.obstcl_y[i]+y_offs,prog.obstcl_x[i]+x_offs,"░",curses.color_pair(1 if prog.player_h == False and prog.msg_done == True else 2))
    else:                                     stdscr.addstr(prog.obstcl_y[i]+y_offs,prog.obstcl_x[i]+x_offs,"#",curses.color_pair(1 if prog.player_h == False and prog.msg_done == True else 2))
#    for i in range(0,h_win):  # Causes black screen flashes on weak hardware
#      for j in range(0,w_win):
#        if not(i in range(y_offs,y_offs+prog.border_h) and j in range(x_offs,x_offs+prog.border_w)):
#          stdscr.addstr(i,j,"░",curses.color_pair(1 if prog.player_h == False else 2))
  stdscr.addstr(y_offs-1,x_offs+int(prog.border_w*0.8),f"Lifes: {prog.player_l}",curses.color_pair(1 if (prog.player_h == False and prog.player_l > 1) else 2))   # Player lifes
  stdscr.addstr(y_offs-1,x_offs+int(prog.border_w*0.2)-len(prog.map_name),prog.map_name,curses.color_pair(1 if prog.player_h == False else 2))                    # Map name
  for i in range(0,len(prog.bullet_y)):                                                                                                                           # Bullets
    if   prog.bullet_h[i] == -1:              stdscr.addstr(prog.bullet_y[i]+y_offs,prog.bullet_x[i]+x_offs,"<",curses.color_pair(2))
    elif prog.bullet_h[i] == 1:               stdscr.addstr(prog.bullet_y[i]+y_offs,prog.bullet_x[i]+x_offs,">",curses.color_pair(2))
    elif prog.bullet_v[i] == -1:              stdscr.addstr(prog.bullet_y[i]+y_offs,prog.bullet_x[i]+x_offs,"A",curses.color_pair(2))
    elif prog.bullet_v[i] == 1:               stdscr.addstr(prog.bullet_y[i]+y_offs,prog.bullet_x[i]+x_offs,"V",curses.color_pair(2))
    #stdscr.addstr(prog.bullet_y[i],prog.bullet_x[i],str(i)) # [For debugging] Shows bullets as their index numbers
