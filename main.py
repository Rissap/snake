import sys
import time
import numpy
import pygame
import random
import threading


pygame.init()


#DELAY = 15
DELAY = 10
SHAPE = 50
SCREEN_SIZE = [620, 670]
WINDOW = pygame.display.set_mode(SCREEN_SIZE)
FIELD = numpy.array([[0]*SHAPE]*SHAPE, dtype=int, ndmin=2)

WINDOW.fill(pygame.Color(150, 150, 150))

IMG_SHAPE = 12
SNAKE_SIZE = 3
SNAKE_SPEED = 60

FIELD[20][20] = 1
FIELD[21][20] = 2
FIELD[22][20] = 3

FIELD[10][15] = -1

COUNT = 0
SPEED = 1
SCORE = 0

x_move, y_move = 0, 0

class Snake():
	def __init__(self, x, y):
		self.size = 3
		self.body = [[x, y], [x+1, y], [x+2, y]]
		self.direction = "LEFT"

	
	def move(self):
		if self.direction == "LEFT":
			x_move, y_move = -1, 0
		elif self.direction == "RIGHT":
			x_move, y_move = 1, 0
		elif self.direction == "UP":
			x_move, y_move = 0, -1
		elif self.direction == "DOWN":
			x_move, y_move = 0, 1
		else:
			pass

		head = self.body[:]
		self.body[0] = [self.body[0][0]+x_move, self.body[0][1]+y_move]
		
		for el in range(1, len(self.body)):
			self.body[el] = head[el-1]

		if self.is_collide(self.body[0]):
			return False
		return True

	def is_collide(self, point):
		x, y = point
		if point in self.body[1:]:
			return True
		elif x==-1 or y==-1 or x==50 or y==50:
			return True
		else:
			pass
		return False


	def add_body(self, point):
		self.body.append(point)


class Food():
	def __init__(self):
		self.position = []

	def new(self):
		self.position = [random.randint(5, 45), random.randint(5, 45)]


class Field():
	def __init__(self):
		self.head = pygame.image.load('res/head.png')
		self.body = pygame.image.load('res/body.png')
		self.food = pygame.image.load('res/food.png')
		#self.tail = pygame.image.load('res/tail.png')
		#self.map = numpy.array([[0]*50]*50, dtype=int, ndmin=2)

	def new_surf(self, snake, food):
		surface = pygame.Surface((600, 600))
		surface.fill(pygame.Color(10, 10, 10))

		for point in range(len(snake)):
			if point == 0:
				surface.blit(self.head, (snake[point][0]*IMG_SHAPE, snake[point][1]*IMG_SHAPE))
			else:
				surface.blit(self.body, (snake[point][0]*IMG_SHAPE, snake[point][1]*IMG_SHAPE))

		surface.blit(self.food, (food[0]*IMG_SHAPE, food[1]*IMG_SHAPE))	
		return surface


#creacting and obj
SNAKE = Snake(random.randint(10, 30), random.randint(10, 30))
FIELD = Field()
FOOD = Food()
FOOD.new()

RUN = True
#main loop
while RUN:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	key = pygame.key.get_pressed()
	if key[pygame.K_UP]:
		SNAKE.direction = "UP"
	elif key[pygame.K_DOWN]:
		SNAKE.direction = "DOWN"
	elif key[pygame.K_LEFT]:
		SNAKE.direction = "LEFT"
	elif key[pygame.K_RIGHT]:
		SNAKE.direction = "RIGHT"
	else:
		pass

	if COUNT >= SNAKE_SPEED:
		if SNAKE.move():
			COUNT = 0
		else:
			RUN = False

	if SNAKE.body[-1] == FOOD.position:
		SNAKE.add_body(FOOD.position)
		FOOD.new()
		SCORE += 1
		if SCORE%5 == 0:
			SPEED += 1
	else:
		pass




	TMP_SURF = FIELD.new_surf(SNAKE.body, FOOD.position)
	COUNT += SPEED
	WINDOW.blit(TMP_SURF, (10, 50))
	pygame.display.flip()
	pygame.time.wait(DELAY)

