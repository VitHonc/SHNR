This is "levels" folder

Each level (or map if you want) is stored as single JSON file, whose name directly corresponds with in-game level name
The file consists of multiple variables that you can change freely, and all of them specify the level directly
If any variable is not set, the default value from data.py will be used instead, BUT...

Some variables are supposed to be set together. This is most important for lists/arrays, e.g. "redguy_*". If only some are set, lenghts won't match
and the game will crash when it loads the file.
When you fill those in and aligh the numbers into grid, each column is for one item (bullet, enemy, ...)

All values are represented as numbers. What do they mean is described here and in "data.py"

What do values in JSON level file mean:


   NAME   |               DESCRIPTION                   | DEFAULT
-----------------------------------------------------------------
"border_h" height of the border                             15
"border_w" width of the border                              30

 -Border is used for two things - It draws walls in rectangle shape around the map
  and also helps to center the map on the center of the screen

"player_y" starting Y (vertical) position of the player     2
"player_x" starting X (horizontal) position of the player   2
"player_l" amount of lifes player has                       1

 -Make sure you don't place the player inside walls!
 -They will be able to escape but... it's ugly

"redguy_y" Starting Y position of the enemy                 <empty>
"redguy_x" Starting X position of the enemy                 <empty>
"redguy_l" Basicly says whether it's ranged (@) or melee (M)<empty>
"redguy_s" If 1, enemy doesn't move                         <empty>

 -"redguy_l" actually says how much enemy's gun loading has progressed
  and increments by 1 each move, util it reaches "gun_load". If set
  to -1, enemy is melee
 -"redguy_s" from word "Static" can make enemies not move/chase the player.
  If the enemy is melee, they won't eve attack, while ranged still shoot

"obstcl_y" Y position of the wall                           <empty>
"obstcl_x" X position of the wall                           <empty>
"obstcl_w" whether it's weak                                <empty>

 -If "obstcl_w" is set to 1, wall is weak (#) and it can be destroyed
  by bullets or the player

"bullet_y" Starting Y position of the bullet                <empty>
"bullet_x" Starting X position of the bullet                <empty>
"bullet_v" Vertical movement speed                          <empty>
"bullet_h" Horizontal movement speed                        <empty>

 -Mostly you don't have to set this, since bullets are auto-generated
 -Vertical and horizontal speed must be -1, 0 or 1
 -Movement speeds must one be zero and the other non-zero!

"breaks_y" Y position of a shatter particle                 <empty>
"breaks_x" X position of a shatter particle                 <empty>
"breaks_c" Shatter particle color (1 is white and 2 is red) <empty>

 -Particles are one-frame effects, so they would exist only util you
  did your first move

"gun_load" How many moves it takes enemies to load guns     5
