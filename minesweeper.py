import pygame, random, math, time

pygame.init()

#setup
WIDTH = 450
HEIGHT = 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.SysFont('Arial', 30, True)

#grid array
grid = []

#images
tile = pygame.image.load('tile.png')
mine = pygame.image.load('mine.png')
numbers = [pygame.image.load('one.png'), pygame.image.load('two.png'), pygame.image.load('three.png'), pygame.image.load('four.png'), pygame.image.load('five.png'), pygame.image.load('six.png'), pygame.image.load('seven.png'), pygame.image.load('eight.png')]
empty = pygame.image.load('empty.png')
flag = pygame.image.load('flag.png')

FPS = 60
clock = pygame.time.Clock()

#game variables
mines = 0
cellcount = 256
column = math.sqrt(cellcount)
row = math.sqrt(cellcount)

class cell(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.revealed = False
		self.bombAround = 0
		self.flag = False
		#randomly determines bomb location
		if(random.randint(0, cellcount) < round(cellcount / 8)):
			self.bomb = True
		else:
			self.bomb = False

#function to search for and return a cell in the "grid" list
def searchForCell(xcoord, ycoord, grid):
	for entry in grid:
		if entry.x == xcoord and entry.y == ycoord:
			return entry

#function to search 8 tiles around space for bombs
def searchForBombs(xcoord, ycoord, grid):
	bombcount = 0
	
	# top left
	if xcoord - 1 > 0 and ycoord - 1 > 0:
		bombcount += searchList(xcoord - 1, ycoord - 1, grid)

	#top middle
	if ycoord - 1 > 0:
		bombcount += searchList(xcoord, ycoord - 1, grid)

	#top right
	if xcoord + 1 < 17 and ycoord - 1 > 0:
		bombcount += searchList(xcoord + 1, ycoord - 1, grid)

	#left middle
	if xcoord - 1 > 0:
		bombcount += searchList(xcoord - 1, ycoord, grid)

	#right middle
	if xcoord + 1 < 17:
		bombcount += searchList(xcoord + 1, ycoord, grid)

	#left bottom
	if xcoord - 1 > 0 and ycoord + 1 < 17:
		bombcount += searchList(xcoord - 1, ycoord + 1, grid)

	#middle bottom
	if ycoord + 1 < 17:
		bombcount += searchList(xcoord, ycoord + 1, grid)

	#right bottom
	if xcoord + 1 < 17 and ycoord + 1 < 17:
		bombcount += searchList(xcoord + 1, ycoord + 1, grid)

	return bombcount

#helper function for searchForBombs
#goes through list and looks at specific space to determine if bomb or not
def searchList(xcoord, ycoord, grid):
	bombcount = 0
	for entry in grid:
		if entry.x == xcoord and entry.y == ycoord and entry.bomb == True:
			bombcount = 1
	return bombcount

#function to start process of revealing adjacent empty cells
#returns a list to call that contains the adjacent spaces that are empty, if there are any
def revealEmptyCells(grid, xcoord, ycoord):
	emptycells = []

	#top left
	if xcoord - 1 > 0 and ycoord - 1 > 0:
		bombcount = searchForBombs(xcoord - 1, ycoord - 1, grid)
		if bombcount == 0:
			emptycells.append(searchForCell(xcoord - 1, ycoord - 1, grid))
		searchAndReveal(xcoord - 1, ycoord - 1, grid, bombcount)
		revealList(xcoord - 1, ycoord - 1, grid)

	#top middle
	if ycoord - 1 > 0:
		bombcount = searchForBombs(xcoord, ycoord - 1, grid)
		if bombcount == 0:
			emptycells.append(searchForCell(xcoord, ycoord - 1, grid))
		searchAndReveal(xcoord, ycoord - 1, grid, bombcount)
		revealList(xcoord, ycoord - 1, grid)

	#top right
	if xcoord + 1 < 17 and ycoord - 1 > 0:
		bombcount = searchForBombs(xcoord + 1, ycoord - 1, grid)
		if bombcount == 0:
			emptycells.append(searchForCell(xcoord + 1, ycoord - 1, grid))
		searchAndReveal(xcoord + 1, ycoord - 1, grid, bombcount)
		revealList(xcoord + 1, ycoord - 1, grid)

	#left middle
	if xcoord - 1 > 0:
		bombcount = searchForBombs(xcoord - 1, ycoord, grid)
		if bombcount == 0:
			emptycells.append(searchForCell(xcoord - 1, ycoord, grid))
		searchAndReveal(xcoord - 1, ycoord, grid, bombcount)
		revealList(xcoord - 1, ycoord, grid)

	#right middle
	if xcoord + 1 < 17:
		bombcount = searchForBombs(xcoord + 1, ycoord, grid)
		if bombcount == 0:
			emptycells.append(searchForCell(xcoord + 1, ycoord, grid))
		searchAndReveal(xcoord + 1, ycoord, grid, bombcount)
		revealList(xcoord + 1, ycoord, grid)

	#left bottom
	if xcoord - 1 > 0 and ycoord + 1 < 17:
		bombcount = searchForBombs(xcoord - 1, ycoord + 1, grid)
		if bombcount == 0:
			emptycells.append(searchForCell(xcoord - 1, ycoord + 1, grid))
		searchAndReveal(xcoord - 1, ycoord + 1, grid, bombcount)
		revealList(xcoord - 1, ycoord + 1, grid)

	#middle bottom
	if ycoord + 1 < 17:
		bombcount = searchForBombs(xcoord, ycoord + 1, grid)
		if bombcount == 0:
			emptycells.append(searchForCell(xcoord, ycoord + 1, grid))
		searchAndReveal(xcoord, ycoord + 1, grid, bombcount)
		revealList(xcoord, ycoord + 1, grid)

	#right bottom
	if xcoord + 1 < 17 and ycoord + 1 < 17:
		bombcount = searchForBombs(xcoord + 1, ycoord + 1, grid)
		if bombcount == 0:
			emptycells.append(searchForCell(xcoord + 1, ycoord + 1, grid))
		searchAndReveal(xcoord + 1, ycoord + 1, grid, bombcount)
		revealList(xcoord + 1, ycoord + 1, grid)

	return emptycells

#helper function for revealEmptyCells to reveal a cell in the grid and set its bombAround
def searchAndReveal(xcoord, ycoord, grid, bombcount):
	for space in grid:
		if xcoord == space.x and ycoord == space.y:
			space.revealed = True
			space.bombAround = bombcount

#helper function for revealEmptyCells to reveal a cell in the grid
def revealList(xcoord, ycoord, grid):
	for entry in grid:
		if entry.x == xcoord and entry.y == ycoord:
			entry.revealed = True

# setting up grid by adding cells to list
# each list has an x and y coordinate in the grid
gridx = 1
gridy = 1

#adds 256 cells in a square
for i in range(1, cellcount + 1):
	newcell = cell(gridx, gridy)
	grid.append(newcell)
	gridx += 1
	if i % column == 0:
		gridx = 1
		gridy += 1

#determines the amount of bombs placed in the grid
for i in grid:
	if i.bomb:
		mines += 1
		#print(i.x, i.y)

#mainloop
score = 0
running = True
while running:
	#variables to reveal adjacent empty cells
	toExpand = []
	cellsToClear = []
	cellsToReveal = []
	needToAdd = True

	xcoord = 0
	ycoord = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			posx, posy = pygame.mouse.get_pos()

			#right click
			if event.button == 3:
				while posx >= 25:
					xcoord += 1
					posx -= 25

				while posy >= 50:
					ycoord += 1
					posy -= 25

				for tempcell in grid:
					if xcoord == tempcell.x and ycoord == tempcell.y:
						if tempcell.flag == False:
							tempcell.flag = True
						else:
							tempcell.flag = False
			#left click
			else:
				while posx >= 25:
					xcoord += 1
					posx -= 25

				while posy >= 50:
					ycoord += 1
					posy -= 25

				bombcount = searchForBombs(xcoord, ycoord, grid)

				#functionality to find adjacent empty cells and reveal them
				if bombcount == 0:
					toExpand = revealEmptyCells(grid, xcoord, ycoord)
					#look through adjacent empty cells until there are no more
					while needToAdd:
						needToAdd = False
						toExpand, temp = [], toExpand

						for entry in temp:
							cellsToClear = revealEmptyCells(grid, entry.x, entry.y)
							for e in cellsToClear:
								if not e.bomb and e not in cellsToReveal:
									cellsToReveal.append(e)
									if e.bombAround == 0:
										toExpand.append(e)
										needToAdd = True

					#once we have found all adjacent empty cells, reveal them and their neighbors
					for entry in cellsToReveal:
						revealList(entry.x, entry.y, grid)

				#reveal the original cell you clicked on no matter if it is has 0 adjacent bombs or not
				for space in grid:
					if xcoord == space.x and ycoord == space.y:
						space.revealed = True
						space.bombAround = bombcount

	#fill the screen with white
	win.fill((255, 255, 255))

	text = font.render("Mines: " + str(mines), 1, (0, 0, 0))
	win.blit(text, (20, 10))

	x = 25
	y = 50

	#image processing for the screen
	for i in grid:
		#if you have clicked on the cell
		if i.revealed == True and i.flag == False:
			#if it is a bomb
			if i.bomb:
				win.blit(mine, (x, y))
			#if there are no adjacent bombs
			elif i.bombAround == 0:
				win.blit(empty, (x, y))
			#if there are bombs around, show the amount
			else:
				win.blit(numbers[i.bombAround - 1], (x, y))
			x += 25
			if i.x % column == 0:
				y += 25
				x = 25
		#if you have right-clicked on a cell, a flag will appear
		elif i.flag == True:
			win.blit(flag, (x, y))
			x += 25
			if i.x % column == 0:
				y += 25
				x = 25
		#if you haven't clicked on the cell at all
		else:
			win.blit(tile, (x, y))
			x += 25
			if i.x % column == 0:
				y += 25
				x = 25

	pygame.display.update()

	clock.tick(FPS)
					
pygame.quit()