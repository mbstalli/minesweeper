import pygame, random, math

pygame.init()

#setup
WIDTH = 450
HEIGHT = 500
#white = (256, 256, 256)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.SysFont('Arial', 30, True)
numbers = [pygame.image.load('one.png'), pygame.image.load('two.png'), pygame.image.load('three.png'), pygame.image.load('four.png'), pygame.image.load('five.png'), pygame.image.load('six.png'), pygame.image.load('seven.png'), pygame.image.load('eight.png')]

#grid array
grid = []

#images
tile = pygame.image.load('tile.png')
mine = pygame.image.load('mine.png')

FPS = 60
clock = pygame.time.Clock()

mines = 0
cellcount = 256
column = math.sqrt(cellcount)
row = math.sqrt(cellcount)

class cell(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.revealed = False
		if(random.randint(0, cellcount) < round(cellcount / 6)):
			self.bomb = True
		else:
			self.bomb = False


# setting up grid by adding cells to list
# each list has an x and y coordinate in the grid
gridx = 1
gridy = 1

for i in range(1, cellcount + 1):
	newcell = cell(gridx, gridy)
	grid.append(newcell)
	gridx += 1
	if i % column == 0:
		gridx = 1
		gridy += 1

for i in grid:
	if i.bomb:
		mines += 1
		#print(i.x, i.y)

#mainloop
score = 0
running = True
while running:

	xcoord = 0
	ycoord = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			posx, posy = pygame.mouse.get_pos()
			#print(pos)
			while posx >= 25:
				xcoord += 1
				posx -= 25

			while posy >= 50:
				ycoord += 1
				posy -= 25

			for space in grid:
				if xcoord == space.x and ycoord == space.y:
					space.revealed = True
					#print(space.bomb)


			#print(str(xcoord) + "," + str(ycoord))


	win.fill((255, 255, 255))

	text = font.render("Mines: " + str(mines), 1, (0, 0, 0))
	win.blit(text, (20, 10))

	x = 25
	y = 50

	for i in grid:
		if i.revealed == True:
			if i.bomb:
				win.blit(mine, (x, y))
			else:
				win.blit(tile, (x, y))
			x += 25
			if i.x % column == 0:
				y += 25
				x = 25
		else:
			win.blit(tile, (x, y))
			x += 25
			if i.x % column == 0:
				y += 25
				x = 25

	pygame.display.update()

	clock.tick(FPS)
					
pygame.quit()