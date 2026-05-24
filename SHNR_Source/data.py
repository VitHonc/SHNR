#!/usr/bin/python3

class Program:
  def __init__(self):
    self.border_h = 15    # Border dimensions to make border walls and center everything
    self.border_w = 30

    self.player_y = 2
    self.player_x = 2
    self.player_l = 1     # player lifes
    self.player_h = False #*To prevent multiple damage to the player in one move

    self.roomdone = False #*Sets to True when room/level is completed
    self.gun_load = 5     # How many player moves does it take enemies to load guns
    self.welc_msg = ""    # Message displayed at he start of a level
    self.msg_done = False #*Sets to True after message is displayed
    self.map_name = ""

    self.redguy_y = []    # y position
    self.redguy_x = []    # x position
    self.redguy_l = []    # gun load state (-1 means melee enemy)
    self.redguy_s = []    # Static?

    self.obstcl_y = []    # Note that you don't have to fill border walls in
    self.obstcl_x = []    # unless you want them to be breakable or something
    self.obstcl_t = []    # Weak wall? (0 is █ and 1 is #)

    self.bullet_y = []
    self.bullet_x = []
    self.bullet_h = []    # horizontal movement
    self.bullet_v = []    # vertical movement

    self.breaks_y = []
    self.breaks_x = []
    self.breaks_c = []    # Color (1 is white and 2 is red)

# * Cannot (and shouldn't) be set in the level JSON file
