import pygame, sys, random, time

class obstlacles:
	def __init__(self):
		self.arr = []

	def add(self,n):
		self.arr.clear()
		while n:
			x = [random.choice(range(10, screen_width - 10)) , random.choice(range(screen_height))]
			self.arr.append(x)
			n -= 1;

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		pygame.mixer.Sound.play(plob_sound)
		ball_speed_y *= -1
		
	# Player Score
	if ball.left <= 0: 
		if ball.top <= goal_top or ball.bottom >= goal_bottom:
			pygame.mixer.Sound.play(plob_sound)
			ball_speed_x *= -1
		else:	
			pygame.mixer.Sound.play(score_sound)
			score_time = pygame.time.get_ticks()
			player_score += 1
		
	# Opponent Score
	if ball.right >= screen_width:
		if ball.top <= goal_top or ball.bottom >= goal_bottom:
			pygame.mixer.Sound.play(plob_sound)
			ball_speed_x *= -1
		else:
			pygame.mixer.Sound.play(score_sound)
			score_time = pygame.time.get_ticks()
			opponent_score += 1
		
	if ball.colliderect(player) and ball_speed_x > 0:
		pygame.mixer.Sound.play(plob_sound)
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	if ball.colliderect(opponent) and ball_speed_x < 0:
		pygame.mixer.Sound.play(plob_sound)
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1
		

def player_animation():
	player.y += player_speed

	if player.top <= goal_top:
		player.top = goal_top
	if player.bottom >= goal_bottom:
		player.bottom = goal_bottom

def opponent_ai():
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= goal_top:
		opponent.top = goal_top
	if opponent.bottom >= goal_bottom:
		opponent.bottom = goal_bottom

def ball_start():
	global ball_speed_x, ball_speed_y, ball_moving, score_time

	ball.center = (screen_width/2, screen_height/2)
	current_time = pygame.time.get_ticks()

	if current_time - score_time < 700:
		number_three = basic_font.render("3",False,light_grey)
		screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))
	if 700 < current_time - score_time < 1400:
		number_two = basic_font.render("2",False,light_grey)
		screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))
	if 1400 < current_time - score_time < 2100:
		number_one = basic_font.render("1",False,light_grey)
		screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_y, ball_speed_x = 0,0
	else:
		ball_speed_x = 5 * random.choice((1,-1))
		ball_speed_y = 5 * random.choice((1,-1))
		score_time = None

# General setup
pygame.mixer.pre_init(44100,-16,1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1067
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 20, 20)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 40, 10,80)
opponent = pygame.Rect(10, screen_height / 2 - 40, 10,80)
goal1 = pygame.Rect(screen_height/2 - 120, 30, 10 , 240)
goal2 = pygame.Rect(screen_height/2 - 120, screen_width - 350, 10 , 240)
obs = []

# Game Variables
ball_speed_x = 5 * random.choice((1,-1))
ball_speed_y = 5 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7
ball_moving = False
score_time = True
goal_top = screen_height/2 - 120;
goal_bottom = screen_height/2 + 120;
obb = obstlacles()
obb.add(10)

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# sound 
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

prev_time = time.perf_counter()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player_speed -= 6
			if event.key == pygame.K_DOWN:
				player_speed += 6
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player_speed += 6
			if event.key == pygame.K_DOWN:
				player_speed -= 6
	
	# tm = random.choice((2,3))
	new_time = time.perf_counter()
	if new_time - prev_time > 5.0:
		prev_time = new_time
		obb.arr.clear()
		obb.add(5)
		obs.clear()
		for ele in obb.arr:
			x = pygame.Rect(ele[0], ele[1], 10,10)
			obs.append(x)

	#Game Logic
	ball_animation()
	player_animation()
	opponent_ai()

	# Visuals 
	screen.fill(bg_color)
	for ele in obs:
		pygame.draw.rect(screen, light_grey, ele)
	pygame.draw.rect(screen, light_grey, player)
	pygame.draw.rect(screen, light_grey, opponent)
	pygame.draw.ellipse(screen, light_grey, ball)
	pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
	pygame.draw.rect(screen, light_grey, goal2)
	pygame.draw.rect(screen, light_grey, goal1)


	if score_time:
		ball_start()

	player_text = basic_font.render(f'{player_score}',False,light_grey)
	screen.blit(player_text,(screen_width/2 + 15,0))

	opponent_text = basic_font.render(f'{opponent_score}',False,light_grey)
	screen.blit(opponent_text,(screen_width/2 - 30,0))

	pygame.display.flip()
	clock.tick(120)

