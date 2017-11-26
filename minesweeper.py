from MinesweeperGame import MinesweeperGame, MinesweeperGridState

import pygame
import time

pygame.init()

def pixelSize(game):
	width = game.width * 16 #grid squares are 16px
	height = game.height * 16
	width += 20 #side borders are 10
	height += 10 + 52 #bottom border is 10, top border is 2*10 + 32

	return (width, height)

# --- setup ---

game = MinesweeperGame(10, 10, 18)

screen = pygame.display.set_mode(pixelSize(game))
pygame.display.set_caption("Minesweeper")

GREY = (0xC0, 0xC0, 0xC0)
done = False

clock = pygame.time.Clock()

# --- main loop ---

while not done:
	# --- handle events ---
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	# --- update state ---

	# --- draw ---

	screen.fill(GREY)

	pygame.display.flip()

	clock.tick(60)

while(True):
	time.sleep(2)