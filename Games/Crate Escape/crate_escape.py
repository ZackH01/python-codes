"""
Resolution: 1280x720

Controls:
Left Arrow Key:  Move left
Right Arrow Key: Move right
Up Arrow Key:    Jump
ESC:             Pause/Unpause
Ctrl+ESC:        Boss key
Ctrl+K:          Kills the player
Ctrl+I:          Toggle invincibility cheat
Ctrl+J:          Toggle infite jump cheat
Ctrl+F:          Toggle freeze cheat

Image Sources:
player_front.png: Created in paint
player_left.png:  Created in paint
player_right.png: Created in paint
crate.png:        Created in paint
coin.png:         Created in paint
goal.png:         Created in paint
boss_key.png:     Screenshot from Google Sheets
"""

#Imports
from tkinter import Tk, Button, Entry, Canvas, PhotoImage, NW
import os
import random as rand


def start_game(level=1, score=0):
	global game_canvas
	global game_width
	global game_height
	global key_pressed
	global direction
	global curr_level
	global curr_score
	global score_text
	global player
	global player_size
	global y_velocity
	global can_jump
	global crates
	global falling_crates
	global crate_size
	global goal
	global coins
	global coin_size
	global num_of_coins
	global time
	global max_time
	global time_text
	global time_between_crates
	global game_paused
	global cheats
	global cheats_used
	global cheats_text
	global is_game_over
	global do_countdown
	global countdown_text
	
	#Hide previous menus/initialise game variables
	main_menu_canvas.pack_forget()
	how_to_play_canvas.pack_forget()
	sl_canvas.pack_forget()
	curr_level = int(level)
	curr_score = int(score)
	
	if curr_level > 1:
		level_cleared_canvas.pack_forget()
		sl_canvas.pack_forget()
		game_canvas.pack_forget()
		if "do_countdown" not in globals():
			do_countdown = False
	else:
		cheats = [] #List of currently active cheats
		cheats_used = False
		do_countdown = True
	
	#Dimensions of the game screen
	if height <= width:
		game_width = height
		game_height = height
	else:
		game_width = width
		game_height = width
	game_canvas = Canvas(root, bg="#CCCCCC", width=game_width, height=game_height)
	
	#Binding keys
	key_pressed = ""
	direction = "" #Direction the player is moving
	game_canvas.bind("<"+left_key_bind+">", left_key)
	game_canvas.bind("<"+right_key_bind+">", right_key)
	game_canvas.bind("<KeyRelease-"+left_key_bind+">", direction_key_released)
	game_canvas.bind("<KeyRelease-"+right_key_bind+">", direction_key_released)
	game_canvas.bind("<"+jump_key_bind+">", up_key)
	game_canvas.bind("<Escape>", esc_key)
	game_canvas.bind("<Control-Escape>", ctrl_esc_key)
	game_canvas.bind("<Control-k>", kill_code)
	game_canvas.bind("<Control-i>", invincibility_code)
	game_canvas.bind("<Control-j>", infinite_jump_code)
	game_canvas.bind("<Control-f>", freeze_code)
	game_canvas.focus_set()
	
	#Initialize game objects
	player_size = int(game_width/24)
	player = game_canvas.create_rectangle(game_width-player_size, game_height-player_size,
					      game_width, game_height, fill="black")
	y_velocity = 0
	can_jump = True
	crates = []
	falling_crates = []
	crate_size = int(game_width/8)
	goal = game_canvas.create_rectangle(0, game_height, game_width, game_height+(crate_size/3),
					    fill="light blue")
	coins = []
	coin_size = int(game_width/24)
	time = 0 #Time measured in frames
	time_between_crates = 186-(curr_level*(6+int(curr_level/5)))
		
	if time_between_crates < 20:
		time_between_crates = 20 #Minimum is 1 crate every 20 frames
	
	game_paused = False
	is_game_over = False
	
	#Move player to centre of the screen
	player_pos = game_canvas.coords(player)
	player_pos[0] -= (game_width/2 - player_size/2)
	player_pos[2] -= (game_width/2 - player_size/2)
	game_canvas.coords(player, player_pos[0], player_pos[1], player_pos[2], player_pos[3])
	
	#Move goal bar to desired location for the level and add desired number of bonuses
	goal_pos = game_canvas.coords(goal)
	if curr_level < 5:
		#Goal is 5 crates above ground and there is 1 coin and max time is 60s
		goal_pos[1] -= crate_size*5
		goal_pos[3] -= crate_size*5
		num_of_coins = 1
		max_time = 60*60
	elif curr_level >= 5 and curr_level < 10:
		#Goal is 6 crates above ground and there are 2 coins and max time is 50s
		goal_pos[1] -= crate_size*6
		goal_pos[3] -= crate_size*6
		num_of_coins = 2
		max_time = 50*60
	elif curr_level >=10 and curr_level < 15:
		#Goal is 7 crates above ground and there are 3 coins and max time is 40s
		goal_pos[1] -= crate_size*7
		goal_pos[3] -= crate_size*7
		num_of_coins = 3
		max_time = 40*60
	else:
		#Goal is 7 crates above ground and there are 3 coins and max time is 30s
		goal_pos[1] -= crate_size*7
		goal_pos[3] -= crate_size*7
		num_of_coins = 3
		max_time = 30*60
	game_canvas.coords(goal, goal_pos[0], goal_pos[1], goal_pos[2], goal_pos[3])
	
	#Create and move coins randomly such that they are below the goal and atleast 3 crates above ground
	for i in range(num_of_coins):
		coins.append(game_canvas.create_rectangle(game_width-coin_size, game_height-coin_size,
			     game_width, game_height, fill="yellow"))
		coin_pos = game_canvas.coords(coins[i])
		x_change = rand.randint(0, game_width-coin_size)
		y_change = rand.randint(int(goal_pos[3]+coin_size),
		                        game_height-crate_size*4)+crate_size*(num_of_coins-1)
		coin_pos[0] -= x_change
		coin_pos[2] -= x_change
		coin_pos[1] -= y_change
		coin_pos[3] -= y_change
		game_canvas.coords(coins[i], coin_pos[0], coin_pos[1], coin_pos[2], coin_pos[3])
	
	#Text displayed on the screen
	score_text = game_canvas.create_text(game_width/8, game_height/12, fill="#333333",
	                                     font="Times 20 bold", text="Score: " + str(curr_score))	
	level_text = game_canvas.create_text(game_width/2, game_height/12, fill="#333333",
					     font="Times 24 bold", text="Level: " + str(curr_level))
	time_text = game_canvas.create_text(game_width-game_width/8, game_height/12, fill="#333333",
					    font="Times 20 bold", text="Time: " + str(int((max_time-time)/60)))
	cheats_text = game_canvas.create_text(game_width/2, game_height/24, fill="#333333",
					      font="Times 16 bold", text="")
	countdown_text = game_canvas.create_text(game_width/2, game_height/2, fill="#333333",
						 font="Times 20 bold", text="")
	
	#Create image overlays for game objects and start the game
	create_images()
	if using_images:
		move_images()
	game_canvas.pack()
	update_game()


def left_key(event):
	global key_pressed
	global direction
	
	if not game_paused:
		key_pressed = "left"
	direction = "left"


def right_key(event):
	global key_pressed
	global direction
	
	if not game_paused:
		key_pressed = "right"
	direction = "right"


def direction_key_released(event):
	global key_pressed
	global direction
	
	direction = ""
	

def up_key(event):
	global key_pressed
	
	key_pressed = "up"
	
	
def esc_key(event):
	global key_pressed
	
	#Escape key is used to pause the game
	if key_pressed == "esc"  and not do_countdown or key_pressed == "ctrl+escape" and not do_countdown:
		pause_game("u")
	else:
		key_pressed = "esc"


def ctrl_esc_key(event):
	global key_pressed
	
	#Ctrl+escape is used to access the boss key
	if key_pressed == "esc"  and not do_countdown or key_pressed == "ctrl+escape" and not do_countdown:
		pause_game("u")
	else:
		key_pressed = "ctrl+esc"
	
	
def kill_code(event):
	global key_pressed
	
	#The player can kill themselves by pressing ctrl+k
	key_pressed = "ctrl+k"
	game_over()
	
	
def invincibility_code(event):
	global key_pressed
	global cheats_used
	
	#Pressing ctrl+i toggles invincibility
	key_pressed = "ctrl+i"
	if "invincibility" not in cheats:
		cheats.append("invincibility")
		cheats_used = True
	else:
		cheats.remove("invincibility")
		
	
def infinite_jump_code(event):
	global key_pressed
	global cheats_used
	
	#Pressing ctrl+j toggles infinite jumping
	key_pressed = "ctrl+j"
	if "infinite jump" not in cheats:
		cheats.append("infinite jump")
		cheats_used = True
	else:
		cheats.remove("infinite jump")
		

def freeze_code(event):
	global key_pressed
	global cheats_used
	
	#Pressing ctrl+f toggles wether crates can fall or not
	key_pressed = "ctrl+j"
	if "freeze" not in cheats:
		cheats.append("freeze")
		cheats_used = True
	else:
		cheats.remove("freeze")


def check_resize(event):
	global width
	global height
	
	#Checks for and changes the width and height used if the window size changes
	wind_width = root.winfo_width()
	wind_height = root.winfo_height()
	
	if wind_height != height or wind_width != width:
		height = wind_height
		width = wind_width


def pause_game(mode = "p"):
	global pause_canvas
	global game_canvas
	global game_paused
	global boss_key_render
	global key_pressed
	global do_countdown
	
	#Pauses the game
	#If mode = p, the normal pause menu opens
	#If mode = b, the boss key is used when pausing
	#If mode = u, the game is unpaused
	if mode != "u":
		game_paused = True
		pause_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
		
		if mode == "p":
			#Paused
			pause_text = pause_canvas.create_text(width/2, height/3, fill="#333333",
							      font="Times 60 bold", text="Paused")
			unpause_button = Button(pause_canvas, width=int(width*0.015), height=int(height*0.004),
			                        text="Continue", command=lambda: pause_game("u"))
			unpause_button.place(x=width*0.425, y=height/2)
		
		elif mode == "b":
			#Boss key
			key_pressed = "esc"
			if using_images and boss_key_img:
				boss_key_render = pause_canvas.create_image(width/2, height/2,
				                                            image=boss_key_img)
			
		game_canvas.pack_forget()
		#Key bindings - to allow button presses on the pause screen, i.e ESC to unpause
		pause_canvas.bind("<Escape>", esc_key)
		#Preserve direction key inputs while paused
		pause_canvas.bind("<Left>", left_key)
		pause_canvas.bind("<Right>", right_key)
		pause_canvas.bind("<KeyRelease-Left>", direction_key_released)
		pause_canvas.bind("<KeyRelease-Right>", direction_key_released)
		pause_canvas.focus_set()
		pause_canvas.pack()
	
	else:
		#Unpause
		pause_canvas.pack_forget()
		game_canvas.focus_set()
		game_canvas.pack()
		key_pressed = ""
		game_paused = False
		do_countdown = True
		update_game()		
	
	
def back(canvas):
	#Stop showing given canvas and display the main menu
	if canvas == "controls":
		controls_canvas.pack_forget()
		main_menu_canvas.pack()
	elif canvas == "leaderboard":
		leaderboard_canvas.pack_forget()
		main_menu_canvas.pack()
	elif canvas == "game_over":
		game_over_canvas.pack_forget()
		game_canvas.pack_forget()
		main_menu_canvas.pack()
	elif canvas == "load":
		sl_canvas.pack_forget()
		main_menu_canvas.pack()


def submit_score(name):
	#Validate player name
	name = name.replace(",", "")
	if name.replace(" ", "") == "":
		#Set default name to "Player" if no input is given
		name = "Player"
	
	if len(name) > 20:
		#Shorten long names
		name = name[0:20]
		
	#Write score to the Leaderboard.txt file
	#Scores written in the form (name, score, level)
	entry = name+","+str(curr_score)+","+str(curr_level)+"\n"
	with open("Leaderboard.txt", "a") as f:
		f.write(entry)
		
	#Switch to leaderboard
	game_over_canvas.pack_forget()
	leaderboard()

	
def game_over():
	global game_over_canvas
	global score_text
	global is_game_over

	if not is_game_over:
		is_game_over = True
		
		#Create game over screen
		game_over_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
		game_over_text = game_over_canvas.create_text(width/2, height/8, fill="#333333",
							      font="Times 60 bold", text="Game Over!")
		game_over_score_text = game_over_canvas.create_text(width/2, height*0.32+32,
		                                                    fill="#333333", font="Times 24 bold",
		                                                    text="Score: " + str(curr_score))
		game_over_level_text = game_over_canvas.create_text(width/2, height*0.32, fill="#333333", 
								   font="Times 24 bold", 
								   text="Level: " + str(curr_level))
		
		#If cheats are used or score=0, don't show the option to save the score
		if cheats_used:
			back_button = Button(game_over_canvas, width=int(width*0.015),
			                     height=int(height*0.004), text="Main Menu",
			                     command=lambda: back("game_over"))
			back_button.place(x=width*0.425, y=height*0.7)
			game_over_canvas.create_text(width/2, height/2, fill="#333333",
			                             font="Times 20 bold", text="Scores obtained using cheats"
			                             + " can't be recorded on the leaderboard")

		elif curr_score <= 0:
			back_button = Button(game_over_canvas, width=int(width*0.015),
			                     height=int(height*0.004), text="Main Menu",
			                     command=lambda: back("game_over"))
			back_button.place(x=width*0.425, y=height*0.7)
		
		else:
			name_entry = Entry(game_over_canvas)
			submit_button = Button(game_over_canvas, width=int(width*0.015), 
					       height=int(height*0.004), text="Submit",
					       command=lambda: submit_score(name_entry.get()))
			game_over_canvas.create_text(width*0.43, height*0.516, fill="#333333",
						     font="Times 16 bold", text="Enter your name:")
			game_over_canvas.create_text(width/2, height*0.55, fill="#333333",
			                             font="Times 12 bold", text="(Maximum name length is 20"
			                             + " characters)")
			name_entry.place(x=width/2, y=height/2)	
			submit_button.place(x=width*0.425, y=height*0.7)
		
		#Change to game over screen
		game_canvas.pack_forget()
		game_over_canvas.pack()
		
	
def check_player_death(crate):
	#Player dies if a crate falls on top of them (Overlap with crate's co-ords)
	player_pos = game_canvas.coords(player)
	crate_pos = game_canvas.coords(crate)
	px1, px2 = player_pos[0], player_pos[2]
	py1, py2 = player_pos[1], player_pos[3]
	cx1, cx2 = crate_pos[0], crate_pos[2]
	cy1, cy2 = crate_pos[1], crate_pos[3]
	
	is_player_dead = False
	
	#Check for overlap (player is in middle of the crate)
	if cx1 < px1 and cx2 > px2 and py1 <= cy2 and py1 > cy1:
		is_player_dead = True
	#Player touches left corner
	elif cx1 >= px1 and cx1 < px2 and py1 <= cy2 and py1 > cy1:
		is_player_dead = True
	#Player touches right corner
	elif cx2 > px1 and cx2 <= px2 and py1 <= cy2 and py1 > cy1:
		is_player_dead = True

	#Player dies unless invincibility cheat is enabled
	if is_player_dead and "invincibility" not in cheats:
		game_over()
	elif is_player_dead and "invincibility" in cheats:
		#Crate is destroyed if the player is invincible
		if using_images and crate_img:
			for i in range(len(crates)):
				if crate_renders[i][0] == crate:
					game_canvas.delete(crate_renders[i][1])
					del crate_renders[i]
					break
		falling_crates.remove(crate)
		crates.remove(crate)
		game_canvas.delete(crate)
			

def level_cleared(level):
	global level_cleared_canvas
	global is_game_over
	global curr_score
	
	is_game_over = True
	
	#Calculate score (Coin bonus is added in check_coin_collision())
	#Level clear bonus: +500, extra +500 per 5 levels beaten (max of +2000)
	#Coin bonus: +100 per coin collected
	#Time bonus: +10 per second left above 30 seconds
	if level < 5:
		level_clear_bonus = 500
	elif level >= 5 and level < 10:
		level_clear_bonus = 1000
	elif level >= 10 and level < 15:
		level_clear_bonus = 1500
	else:
		level_clear_bonus = 2000
	coin_bonus = (num_of_coins-len(coins))*100
	time_bonus = int((1800+60-time)/60)*10
	#Ensures you can't be deducted points because of time
	if time_bonus <= 0:
		time_bonus = 0
	
	curr_score += level_clear_bonus
	curr_score += time_bonus
	
	#Create level cleared screen
	level_cleared_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	level_cleared_text = level_cleared_canvas.create_text(width/2, height/8, fill="#333333",
							      font="Times 60 bold", text="Level "
							      + str(level) + " Cleared!")
	bonus_text = level_cleared_canvas.create_text(width/2, height*0.45, fill="#333333",
						      font="Times 24 bold", text="Clear Bonus:  +" 
						      + str(level_clear_bonus) + "\nCoin Bonus:   +" 
						      + str(coin_bonus) + "\nTime bonus:   +" 
						      + str(time_bonus) 
						      + "\n_____________________\nScore:              " 
						      + str(curr_score))
	next_level_button = Button(level_cleared_canvas, width=int(width*0.015), height=int(height*0.004),
				   text="Next Level", command=lambda: start_game(level+1, curr_score))
	save_button = Button(level_cleared_canvas, width=int(width*0.015), height=int(height*0.004),
			     text="Save & Quit", command=lambda: save_load_game("s"))
	
	next_level_button.place(x=width*0.425, y=height*0.7)
	save_button.place(x=width*0.425, y=height*0.76)
	
	#Change to level cleared screen
	game_canvas.pack_forget()
	level_cleared_canvas.pack()


def check_level_clear():
	#Level is cleared when the player touches the goal
	player_pos = game_canvas.coords(player)
	goal_pos = game_canvas.coords(goal)
	
	if player_pos[1] < goal_pos[3]:
		level_cleared(curr_level)
		
	
def check_coin_collection():
	global curr_score

	#Check if the player is overlapping with a coin to collect it
	player_pos = game_canvas.coords(player)
	px1, px2 = player_pos[0], player_pos[2]
	py1, py2 = player_pos[1], player_pos[3]
	
	for coin in coins:
		coin_pos = game_canvas.coords(coin)
		collect_coin = False
		#Check collision on all 4 vertices of the coin
		cx1, cx2 = coin_pos[0], coin_pos[2]
		cy1, cy2 = coin_pos[1], coin_pos[3]
	
		if cx1 >= px1 and cy1 > py1 and cx1 < px2 and cy1 < py2:
			collect_coin = True
		elif cx2 >= px1 and cy1 > py1 and cx2 < px2 and cy1 < py2:
			collect_coin = True
		elif cx1 >= px1 and cy2 > py1 and cx1 < px2 and cy2 < py2:
			collect_coin = True
		elif cx2 >= px1 and cy2 > py1 and cx2 < px2 and cy2 < py2:
			collect_coin = True
		
		#If collected, remove coin from the game and add 100 points
		if collect_coin:
			coins.remove(coin)
			#Check if using images
			if using_images and coin_img:
				for i in range(len(coin_renders)):
					if coin_renders[i][0] == coin:
						game_canvas.delete(coin_renders[i][1])
						del coin_renders[i]
						break
			game_canvas.delete(coin)
			curr_score += 100
			game_canvas.itemconfigure(score_text, text="Score: " + str(curr_score))


def move_crates():
	#Moves any crate that can fall downwards
	for crate in falling_crates:
		crate_pos = game_canvas.coords(crate)
		x1, x2 = crate_pos[0], crate_pos[2]
		y1, y2 = crate_pos[1], crate_pos[3]
		
		y1 += game_height/100
		y2 += game_height/100
		
		#Check collision with border
		if y2 > game_height:
			y1 = game_height-crate_size
			y2 = game_height
			falling_crates.remove(crate)
		
		#Check collision with other crates
		check_collision_1 = check_crate_collision(x1+1, y2)
		check_collision_2 = check_crate_collision(x2-1, y2)
		if check_collision_1 != False:
			y1 = check_collision_1[1] - crate_size
			y2 = check_collision_1[1]
			falling_crates.remove(crate)
		elif check_collision_2 != False:
			y1 = check_collision_2[1] - crate_size
			y2 = check_collision_2[1]
			falling_crates.remove(crate)
		
		#Move crate
		game_canvas.coords(crate, x1, y1, x2, y2)
		
		#Check if the player dies due to this crate's move
		check_player_death(crate)
		
		
def create_crate(tries = 0):
	#Find a random position for the crate at the top of the screen
	x = (crate_size/3) * rand.randint(0, int((game_width/(crate_size/3)-3)))
	y = -crate_size
	
	#Check if there is a crate at the top already (crates have stacked to the top of the screen)
	check_collision_1 = check_crate_collision(x+1, y+1)
	check_collision_2 = check_crate_collision(x+crate_size-1, y+crate_size-1)
	if check_collision_1 == False and check_collision_2 == False:
		#Create crate
		crate = game_canvas.create_rectangle(game_width-crate_size, game_height-crate_size, 
						     game_width, game_height, fill="orange")
		crates.append(crate)
		falling_crates.append(crate)
		game_canvas.coords(crates[len(crates)-1], x, y, x+crate_size, y+crate_size)
		#Check if images should be used
		if using_images and crate_img:
			crate_renders.append([crate, game_canvas.create_image(0, 0, anchor=NW,
			                     image=crate_img)])
	else:
		#Try placing crate again up to 10 times (to avoid reaching recursion limit)
		if tries < 10:
			create_crate(tries+1)
	

def check_crate_collision(x, y):
	#Returns coords of the crate an object collides with
	for crate in crates:
		crate_pos = game_canvas.coords(crate)
		cx1, cx2 = crate_pos[0], crate_pos[2]
		cy1, cy2 = crate_pos[1], crate_pos[3]
		
		if x > cx1 and y > cy1 and x < cx2 and y < cy2:
			return crate_pos
	return False


def calc_vertical_pos(velocity):
	result = [0, 0] #[displacement, final velocity]
	gravity = game_height/720
	
	#Displacement given as s = ut + 0.5gt^2 where here t=1, g>0
	result[0] = velocity + 0.5*gravity
	
	#Final velocity given as v = u + gt where here t=1, g>0
	result[1] = velocity + gravity
	
	return result


def move_player():
	global key_pressed
	global y_velocity
	global can_jump
	global player_img

	player_pos = game_canvas.coords(player)
	x1, x2 = player_pos[0], player_pos[2]
	y1, y2 = player_pos[1], player_pos[3]
	
	#Move player horizontally
	if direction == "left":
		x1 -= game_width/144
		x2 -= game_width/144
		
		#Check if image should be changed
		if using_images and player_img:
			player_img = PhotoImage(file="images/player_left.png")
			game_canvas.itemconfig(player_render, image=player_img)
		
		#Check collision with border
		if  x1 < 0:
			x1 = 0
			x2 = player_size
		
		#Check collision with crates
		check_collision_1 = check_crate_collision(x1, y1)
		check_collision_2 = check_crate_collision(x1, y2)
		
		if check_collision_1 != False:
			x1 = check_collision_1[2]
			x2 = check_collision_1[2]+player_size
		
		elif check_collision_2 != False:
			x1 = check_collision_2[2]
			x2 = check_collision_2[2]+player_size
	
	elif direction == "right":
		x1 += game_width/144
		x2 += game_width/144
		
		#Check if image should be changed
		if using_images and player_img:
			player_img = PhotoImage(file="images/player_right.png")
			game_canvas.itemconfig(player_render, image=player_img)
		
		#Check collision with border
		if x2 > game_width:
			x1 = game_width-player_size
			x2 = game_width
		
		#Check collision with crates
		check_collision_1 = check_crate_collision(x2, y1)
		check_collision_2 = check_crate_collision(x2, y2)
		
		if check_collision_1 != False:
			x1 = check_collision_1[0]-player_size
			x2 = check_collision_1[0]
		
		elif check_collision_2 != False:
			x1 = check_collision_2[0]-player_size
			x2 = check_collision_2[0]
		
	else:
		#Resest image to front facing
		if using_images and player_img:
			player_img = PhotoImage(file="images/player_front.png")
			game_canvas.itemconfig(player_render, image=player_img)
		
	#Move player vertically and handle jumping
	if key_pressed == "up":
		key_pressed = ""
		
		if "infinite jump" not in cheats:
			if can_jump == True and y_velocity == 0:
				y_velocity = -game_height/36 #Initial jump speed
				can_jump = False
		else:
			y_velocity = -game_height/36 #Initial jump speed
		
	vertical_calc = calc_vertical_pos(y_velocity)
	y1 += vertical_calc[0]
	y2 += vertical_calc[0]
	y_velocity = vertical_calc[1]
	
	#Check collision with border
	if y2 > game_height:
		y1 = game_height-player_size
		y2 = game_height
		#Since on the floor
		y_velocity = 0
		can_jump = True
		
	#Check collision with crates
	#All collisions with crates must check two pairs of co-ords (to account for corners)
	if y_velocity < 0: 
		#Moving up so check ceilings
		check_collision_1 = check_crate_collision(x1, y1)
		check_collision_2 = check_crate_collision(x2, y1)
		
		if check_collision_1 != False:
			y1 = check_collision_1[3]
			y2 = check_collision_1[3]+player_size
			#Collided with ceiling so set y-velocity to 0
			y_velocity = 0
		
		elif check_collision_2 != False:
			y1 = check_collision_2[3]
			y2 = check_collision_2[3] + player_size
			#Collided with ceiling so set y-velocity to 0
			y_velocity = 0
	else: 
		#Moving downwards so check floors
		check_collision_1 = check_crate_collision(x1, y2)
		check_collision_2 = check_crate_collision(x2, y2)
		
		if check_collision_1 != False:
			y1 = check_collision_1[1]-player_size
			y2 = check_collision_1[1]
			#Since on the floor
			y_velocity = 0
			can_jump = True
		
		elif check_collision_2 != False:
			y1 = check_collision_2[1]-player_size
			y2 = check_collision_2[1]
			#Since on the floor
			y_velocity = 0
			can_jump = True
	
	#Update player with new position
	game_canvas.coords(player, x1, y1, x2, y2)
	
	#Check if the player will collect any coins
	check_coin_collection()
	
	#Check if the player clears the level
	check_level_clear()


def create_images():
	global using_images
	global player_render
	global player_img
	global crate_renders
	global crate_img
	global coin_renders
	global coin_img
	global goal_render
	global goal_img
	global boss_key_img
	
	#Check if each image should be used and create them if so
	#See the docstring at the top of the code for image sources
	if os.path.exists("images/") and width >= 1280 and height >= 720:
		using_images = True
		
		#Check if images for the player exist
		front_img = os.path.isfile("images/player_front.png")
		left_img = os.path.isfile("images/player_left.png")
		right_img = os.path.isfile("images/player_right.png")
		
		if front_img and left_img and right_img:
			player_img = PhotoImage(file="images/player_front.png")
			player_render = game_canvas.create_image(0, 0, anchor=NW, image=player_img)
		else:
			player_img = False
			
		if os.path.isfile("images/coin.png"):
			coin_img = PhotoImage(file="images/coin.png")
			coin_renders = [] #List of [coin_id, coin_render]
			
			for i, coin in enumerate(coins):
				coin_renders.append([coin, game_canvas.create_image(0, 0, anchor=NW,
						    image=coin_img)])
				coin_pos = game_canvas.coords(coins[i])
				game_canvas.coords(coin_renders[i][1], coin_pos[0], coin_pos[1])
		else:
			coin_img = False
			
		if os.path.isfile("images/player_front.png"):
			crate_img = PhotoImage(file="images/crate.png")
			crate_renders = [] #List of [crate_id, crate_render]
		else:
			crate_img = False
			
		if os.path.isfile("images/goal.png"):
			goal_img = PhotoImage(file="images/goal.png")
			goal_render = game_canvas.create_image(0, 0, anchor=NW, image=goal_img)
			goal_pos = game_canvas.coords(goal)
			game_canvas.coords(goal_render, goal_pos[0], goal_pos[1])
		else:
			goal_img = False
			
		if os.path.isfile("images/boss_key.png"):
			boss_key_img = PhotoImage(file="images/boss_key.png")
		else:
			boss_key_img = False
	else:
		using_images = False


def move_images():
	#Moves images over the top of the rectangels that define the position for the game objects
	if player_img:
		player_pos = game_canvas.coords(player)
		game_canvas.coords(player_render, player_pos[0], player_pos[1])

	if crate_img:
		for crate in crates:
			crate_pos = game_canvas.coords(crate)
			for i in range(len(crate_renders)):
				if crate_renders[i][0] == crate:
					game_canvas.coords(crate_renders[i][1], crate_pos[0], crate_pos[1])

	
def update_game():
	global key_pressed
	global time
	global do_countdown
	global countdown
	global countdown_text
	
	#Handle pausing of the game
	if key_pressed == "esc" and not game_paused and not do_countdown:
		pause_game()
	elif key_pressed == "ctrl+esc" and not game_paused and not do_countdown:
		pause_game("b")
	
	#Run a countdown after unpausing/loading a game/starting a new game
	if do_countdown:
		if "countdown" not in globals():
			countdown = 4
		
		countdown -= 1
		game_canvas.itemconfigure(countdown_text, text="Starting in: " + str(countdown))
		
		if countdown <= 1:
			do_countdown = False
			countdown = 4
		
		game_canvas.pack()
		root.after(1000, update_game)
	
	#Move objects and refresh the screen
	elif not is_game_over and not game_paused:
		#Calculate movement
		if "freeze" not in cheats:
			move_crates()
		
		move_player()
		
		#Makes a crate at regular intervals based on level
		if time % time_between_crates == 0 and "freeze" not in cheats:
			create_crate()
		
		#Update timer and check for timer death
		time += 1 #Time measured in frames
		game_canvas.itemconfigure(time_text, text="Time: " + str(int((max_time+60-time)/60)))
		if time >= max_time:
			game_over()
		
		#Update screen
		if using_images:
			move_images()
		
		if cheats_used:
			game_canvas.itemconfigure(cheats_text, text="Cheats: "+", ".join(cheats))
		
		game_canvas.itemconfigure(countdown_text, text="")

		game_canvas.pack()
		root.after(16, update_game) #Updates every frame at 60fps
		
	else:
		game_canvas.pack_forget()
		
		
def save(slot):
	#Get current save data and add the new save data
	with open("Saves.txt") as f:
		save_data = f.readlines()

	for i, data in enumerate(save_data):
		save_data[i] = data.replace("\n", "").split(",")

	save_data[int(slot)] = [str(curr_score), str(curr_level+1), str(cheats_used)]

	#Write save data to the file
	temp = save_data
	save_data = ""
	
	for data in temp:
		if len(data) == 1:
			save_data += "Empty"
		else:
			save_data += data[0] + "," + data[1] + "," + data[2]
		
		save_data += "\n"
	
	with open("Saves.txt", "w") as f:
		f.write(save_data)
	
	#Refresh saving menu
	sl_canvas.pack_forget()
	save_load_game("s")
	

def load(slot, slot_data):
	global cheats_used
	global cheats
	global do_countdown
	global show_how_to_play
	
	#Clear save slot when loaded
	#Get current save data
	with open("Saves.txt") as f:
		save_data = f.readlines()

	for i, data in enumerate(save_data):
		save_data[i] = data.replace("\n", "").split(",")

	save_data[slot] = ["Empty"]	
	
	#Write save data to the file
	temp = save_data
	save_data = ""
	for data in temp:
		if len(data) == 1:
			save_data += "Empty"
		else:
			save_data += data[0] + "," + data[1] + "," + data[2]
		save_data += "\n"
	
	with open("Saves.txt", "w") as f:
		f.write(save_data)
	
	#Starts the game with the saved data
	if slot_data[2] == "True":
		cheats_used = True
	else:
		cheats_used = False
	
	cheats = []
	sl_canvas.pack_forget()
	do_countdown = True
	show_how_to_play = False
	start_game(slot_data[1], slot_data[0])
	
	
def save_load_game(mode):
	global sl_canvas
	
	#If mode = s, the game's progress will be saved
	#If mode = l, a game can be loaded
	sl_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	
	with open("Saves.txt") as f:
		save_data = f.readlines()
	for i, slot in enumerate(save_data):
		save_data[i] = slot.replace("\n", "").split(",")
	
	slot_buttons = []
	#Load game
	if mode == "l":
		sl_canvas.create_text(width/2, height/8, fill="#333333", font="Times 60 bold", 
				      text="Load Game")
		sl_canvas.create_text(width/2, height-height/4, fill="#333333", font="Times 16 bold",
				      text="Note: Loading will clear the save data stored in that slot")
		main_menu_canvas.pack_forget()
		
		#Create buttons to represent save slots to load data from
		for i, data in enumerate(save_data):
			if data == ["Empty"]:
				slot_buttons.append(Button(sl_canvas, width=int(width*0.015),
				 		    height=int(height*0.015), text="Empty", 
				 		    command=start_game))
			else:
				slot_buttons.append(Button(sl_canvas, width=int(width*0.015),
							   height=int(height*0.015), text="Level: "
							   + str(data[1])+"\nScore: "
							   + str(data[0]), 
							   command=lambda s=i, d=data: load(s, d)))
				
	#Save game
	if mode == "s":
		sl_canvas.create_text(width/2, height/8, fill="#333333", font="Times 60 bold",
				      text="Save Game")
		sl_canvas.create_text(width/2, height*0.75, fill="#333333", font="Times 16 bold",
				      text="Note: Saving will overwrite any previous save data stored"
				      + " in that slot")
		level_cleared_canvas.pack_forget()
		
		#Create buttons to represent save slots to save data to
		for i, data in enumerate(save_data):
			if data == ["Empty"]:
				slot_buttons.append(Button(sl_canvas, width=int(width*0.015),
							   height=int(height*0.015), text="Empty",
							   command=lambda s=i: save(s)))
			else:
				slot_buttons.append(Button(sl_canvas, width=int(width*0.015),
							   height=int(height*0.015), text="Level: "
							   + str(data[1])+"\nScore: " + str(data[0]),
							   command=lambda s=i: save(s)))
	
	#Place save slot buttons
	for i in range(len(slot_buttons)):
		sl_canvas.create_text(width*0.295+(width*0.2*i), height*0.35, fill="#333333",
				      font="Times 20 bold", text="Slot "+str(i+1))
		slot_buttons[i].place(x=width*0.225+width*0.2*i , y=height*0.4)
				
	back_button = Button(sl_canvas, width=int(width*0.015), height=int(height*0.004),
			     text="Main Menu", command=lambda: back("load"))
	back_button.place(x=width*0.425, y=height*0.8)
	
	sl_canvas.pack()


def change_leaderboard_page(page):
	#Shows the next/previous 10 scores
	leaderboard_canvas.pack_forget()
	leaderboard(page)


def leaderboard(page=0):
	global leaderboard_canvas
	
	if page == 0:
		main_menu_canvas.pack_forget()
	
	#Put scores from the Leaderboard.txt file into a sorted list
	with open("Leaderboard.txt") as f:
		scores_list = f.readlines()
	
	for i, score in enumerate(scores_list):
		scores_list[i] = score.replace("\n", "").split(",")
	
	scores_list = sorted(scores_list, key=lambda list: int(list[1]), reverse=True)
	
	#Create leaderboard screen
	leaderboard_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	leaderboard_canvas.create_text(width/2, height/8, fill="#333333" ,font="Times 60 bold",
				       text="Leaderboard")
	back_button = Button(leaderboard_canvas, width=int(width*0.015), height=int(height*0.004),
			     text="Main Menu", command=lambda: back("leaderboard"))
	back_button.place(x=width*0.425, y=height*0.86)
	
	table_width = width/2
	table_height = height/1.8
	leaderboard_table = Canvas(leaderboard_canvas, bg="#CCCCCC", width=table_width,
				   height=table_height*1.1)

	#Create the table
	#Header
	leaderboard_table.create_rectangle(0, 0, table_width, table_height/10, fill="#BBBBBB")
	leaderboard_table.create_text(table_width/3.5, 0.6*(table_height/10), fill="#333333",
				      font="Times 20 bold", text="Player")
	leaderboard_table.create_text(table_width-(table_width/3), 0.6*(table_height/10), fill="#333333",
				      font="Times 20 bold", text="Score")
	leaderboard_table.create_text(table_width-(table_width/10), 0.6*(table_height/10), fill="#333333",
				      font="Times 20 bold", text="Level")
	
	#Rows
	if len(scores_list) > (page+1)*10:
		last_score = (page+1)*10
	else:
		last_score = len(scores_list)
	
	for i in range(page*10, last_score):
		#Gold, Silver and Bronze colours for 1st, 2nd and 3rd
		if page == 0 and i < 3:
			if i == 0:
				leaderboard_table.create_rectangle(0, (i+1)*(table_height/10), table_width,
				 				   (i+2)*(table_height/10), fill="#FFD700")
			elif i == 1:
				leaderboard_table.create_rectangle(0, (i+1)*(table_height/10), table_width,
							           (i+2)*(table_height/10), fill="#D8D8D8")
			elif i == 2:
				leaderboard_table.create_rectangle(0, (i+1)*(table_height/10), table_width,
								   (i+2)*(table_height/10), fill="#CD7F32")
		else:
			#Alternate background colour between light and dark grey
			if i % 2 == 0:
				leaderboard_table.create_rectangle(0, (i-(page*10)+1)*(table_height/10),
							           table_width, (i-(page*10)+2)
							           * (table_height/10), fill="#CCCCCC")
			else:
				leaderboard_table.create_rectangle(0, (i-(page*10)+1)*(table_height/10),
								   table_width, (i-(page*10)+2)
								   * (table_height/10), fill="#BBBBBB")
		
		#Display scores
		leaderboard_table.create_text(table_width/30, (i-(page*10)+1.6)*(table_height/10),
					      fill="#333333", font="Times 20 bold", text=str(i+1)+".")
		leaderboard_table.create_text(table_width/3.5, (i-(page*10)+1.6)*(table_height/10),
					      fill="#333333", font="Times 20 bold", 
					      text=str(scores_list[i][0]))
		leaderboard_table.create_text(table_width-(table_width/3), (i-(page*10)+1.6)
					      * (table_height/10), fill="#333333", font="Times 20 bold",
					      text=str(scores_list[i][1]))
		leaderboard_table.create_text(table_width-(table_width/10), (i-(page*10)+1.6)
					      * (table_height/10), fill="#333333", font="Times 20 bold",
					      text=str(scores_list[i][2]))

	#Create next page/prev page buttons if needed
	if len(scores_list) > (page+1)*10:
		next_button = Button(leaderboard_canvas, width=int(width*0.004), height=int(height*0.001),
				     text="Next", command=lambda: change_leaderboard_page(page+1))
		next_button.place(x=width*0.699, y=height*(7/9))
	if page > 0:
		prev_button = Button(leaderboard_canvas, width=int(width*0.004), height=int(height*0.001),
				     text="Prev", command=lambda: change_leaderboard_page(page-1))
		prev_button.place(x=width*0.648, y=height*(7/9))
	
	leaderboard_canvas.pack()
	leaderboard_table.place(x=width/4, y=height/6)


def bind_key(event):
	global key_pressed
	global key_to_bind
	global left_key_bind
	global right_key_bind
	global jump_key_bind
	
	#Get the key that was pressed and format it as a string
	key_pressed = str(event)
	key_pressed = key_pressed.split(" ")
	key_pressed = key_pressed[2]
	key_pressed = key_pressed[7:]
	
	#Validate key
	keys = ["Left", "Right", "Up", "Down", "space"]
	if len(key_pressed) == 1 and key_pressed.isalpha() or key_pressed in keys:
		#Change key binding
		if key_to_bind == "left":
			left_key_bind = key_pressed
			bind_left_key_button.config(text=left_key_bind.title())
		
		elif key_to_bind == "right":
			right_key_bind = key_pressed
			bind_right_key_button.config(text=right_key_bind.title())
		
		elif key_to_bind == "jump":
			jump_key_bind = key_pressed
			bind_jump_key_button.config(text=jump_key_bind.title())
		
		controls_canvas.pack()
	
	key_to_bind = None
	

def set_key_to_bind(key):
	global key_to_bind

	#When the user presses a button, the key to bind is chosen
	key_to_bind = key


def controls():
	global controls_canvas
	global key_to_bind
	global bind_left_key_button
	global bind_right_key_button
	global bind_jump_key_button
	
	key_to_bind = None
	
	#Create controls screen
	controls_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	controls_canvas.create_text(width/2, height/8, fill="#333333" ,font="Times 60 bold",
				    text="Controls")
	controls_canvas.create_text(width/2, height*0.22, fill="#333333", font="Times 24 bold", 
				    text="Movement")
	controls_canvas.create_text(width*0.44, height*0.31, fill="#333333", font="Times 20 bold", 
	                            text="  Move Left:\nMove Right:\n          Jump:")
	controls_canvas.create_text(width/2, height*0.43, fill="#333333", font="Times 24 bold", 
	                            text="Pausing")
	controls_canvas.create_text(width*0.505, height/2, fill="#333333", font="Times 20 bold",
	                            text="Pause/Unpause: Escape\nBoss Key: Ctrl+Escape")
	controls_canvas.create_text(width/2, height*0.6, fill="#333333", font="Times 24 bold", 
				    text="Cheats*")
	controls_canvas.create_text(width*0.47, height*0.71, fill="#333333" ,font="Times 20 bold",
				    text="     Kill Player: Ctrl+K\n   Invincibility: Ctrl+I"
				    + "\nInfinite Jump: Ctrl+J\nFreeze Crates: Ctrl+F")
	controls_canvas.create_text(width/2, height*0.82, fill="#333333", font="Times 16 bold", 
				    text="*Scores obtained using cheats can't be recorded on the"
				    + " Leaderboard!")
	
	back_button = Button(controls_canvas, width=int(width*0.015), height=int(height*0.004),
			     text="Main Menu", command=lambda: back("controls"))
	bind_left_key_button = Button(controls_canvas, width=int(width*0.004), height=int(height*0.0015),
			              text=left_key_bind.title(), command=lambda: set_key_to_bind("left"))
	bind_right_key_button = Button(controls_canvas, width=int(width*0.004), height=int(height*0.0015),
				       text=right_key_bind.title(), command=lambda: set_key_to_bind("right"))
	bind_jump_key_button = Button(controls_canvas, width=int(width*0.004), height=int(height*0.0015),
				      text=jump_key_bind.title(), command=lambda: set_key_to_bind("jump"))
			
	back_button.place(x=width*0.425, y=height*0.88)
	bind_left_key_button.place(x=width*0.504, y=height*0.25)
	bind_right_key_button.place(x=width*0.504, y=height*0.29)
	bind_jump_key_button.place(x=width*0.504, y=height*0.33)
	
	controls_canvas.bind("<Key>", bind_key)
	controls_canvas.focus_set()
	
	#Display canvas
	main_menu_canvas.pack_forget()
	controls_canvas.pack()


def how_to_play():
	global how_to_play_canvas
	global show_how_to_play

	if show_how_to_play:
		#Create how to play screen
		how_to_play_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
		how_to_play_canvas.create_text(width/2, height/8, fill="#333333", font="Times 60 bold",
					       text="How To Play")
		how_to_play_canvas.create_text(width/2, height*0.23, fill="#333333", 
					       font="Times 24 bold", text="Movement")
		how_to_play_canvas.create_text(width/2, height*0.31, fill="#333333",
					       font="Times 20 bold", text=" Move Left: " 
					       + left_key_bind.title() + "\nMove Right: " 
					       + right_key_bind.title() + "\n       Jump: " 
					       + jump_key_bind.title())
		how_to_play_canvas.create_text(width/2, height*0.42, fill="#333333", font="Times 24 bold",
					       text="Objective")
		how_to_play_canvas.create_text(width/2, height/2, fill="#333333", font="Times 20 bold",
		                               text="Jump on crates to reach the goal line at the top "
		                               + "to move on to the next level\n                        "
		                               + "Avoid getting crushed by the falling crates\n"
		                               + "                         Reach the goal before the timer"
		                               + " runs out")
		how_to_play_canvas.create_text(width/2, height*0.61, fill="#333333" ,font="Times 24 bold",
					       text="Scoring")
		how_to_play_canvas.create_text(width/2, height*0.69, fill="#333333" ,font="Times 20 bold",
					       text="                You gain points for every level you"
					       + " clear, harder levels earn more points\n"
					       + "                                     Collect the yellow"
					       + " coins to gain +100 points\nIf you beat a level quickly,"
					       + " you gain extra points based on how much time is left on"
					       + " the clock")
		play_button = Button(how_to_play_canvas, width=int(width*0.015), height=int(height*0.004),
				     text="Play", command=start_game)
		
		play_button.place(x=width*0.425, y=height*0.78)
		
		show_how_to_play = False
		main_menu_canvas.pack_forget()
		how_to_play_canvas.pack()
	else:
		start_game()


def main_menu():
	global main_menu_canvas
	
	#Create main menu
	main_menu_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	new_game_button = Button(main_menu_canvas, width=int(width*0.015), height=int(height*0.004),
				 text="New Game", command=how_to_play)
	load_game_button = Button(main_menu_canvas, width=int(width*0.015), height=int(height*0.004),
				  text="Load Game", command=lambda: save_load_game("l"))
	leaderboard_button = Button(main_menu_canvas, width=int(width*0.015), height=int(height*0.004),
				    text="Leaderboard", command=leaderboard)
	settings_button = Button(main_menu_canvas, width=int(width*0.015), height=int(height*0.004),
				 text="Controls", command=controls)
	title_text = main_menu_canvas.create_text(width/2, height/8, fill="#333333", font="Times 60 bold",
						  text="Crate Escape")
	
	new_game_button.place(x=width*0.425, y=height*0.5)
	load_game_button.place(x=width*0.425, y=height*0.56)
	leaderboard_button.place(x=width*0.425, y=height*0.62)
	settings_button.place(x=width*0.425, y=height*0.68)
	
	main_menu_canvas.pack()


def main():
	global root
	global width
	global height
	global controls_canvas
	global how_to_play_canvas
	global game_canvas
	global game_over_canvas
	global sl_canvas
	global level_cleared_canvas
	global left_key_bind
	global right_key_bind
	global jump_key_bind
	global show_how_to_play
	
	#Setting up the window
	width = 1280
	height = 720
	root = Tk()
	root.geometry(str(width)+"x"+str(height))
	root.title("Crate Escape")
	root.bind("<Configure>", check_resize)

	#Declare canvases that could be used
	controls_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	how_to_play_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	game_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	game_over_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	sl_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	level_cleared_canvas = Canvas(root, bg="#CCCCCC", width=width, height=height)
	
	#Default key bindings
	left_key_bind = "Left"
	right_key_bind = "Right"
	jump_key_bind = "Up"
	
	#Check for game files and create them if they don't exist
	if not os.path.isfile("Leaderboard.txt"):
		with open("Leaderboard.txt", "x"):
			pass
	
	if not os.path.isfile("Saves.txt"):
		with open("Saves.txt", "w") as f:
			f.write("Empty\nEmpty\nEmpty")
	
	#Run program
	show_how_to_play = True #Only show the how to play screen on the user's first attempt
	main_menu()
	root.mainloop()
	
	
if __name__ == "__main__":
	main()




