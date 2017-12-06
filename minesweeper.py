from MinesweeperGame import MinesweeperGame, MinesweeperGridState
from MinesweeperDisplay import MinesweeperDisplay

import pygame
import time

pygame.init()

# --- setup ---

game = MinesweeperGame(10, 10, 10)

display = MinesweeperDisplay(game)

done = False
clock = pygame.time.Clock()

# --- main loop ---

while not done:
	# --- handle events ---
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and display.gridRect().collidepoint(event.pos):
			if event.button == 3:
				game.flag(display.gridLocOfPos(event.pos))
			else:
				display.mouseDownLoc = display.gridLocOfPos(event.pos)
		elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
			if display.gridRect().collidepoint(event.pos):
				display.mouseDownLoc = display.gridLocOfPos(event.pos)
			else:
				display.mouseDownLoc = (-1, -1)
		elif event.type == pygame.MOUSEBUTTONUP and display.gridRect().collidepoint(event.pos):
			if event.button == 1:
				game.uncover(display.gridLocOfPos(event.pos))
		elif event.type == pygame.QUIT:
			done = True

	# --- update state ---

	if game.hasWon():
		game.win()
	else:
		game.updateClock(clock.get_time())

	# --- draw ---

	display.draw()

	clock.tick(60)
