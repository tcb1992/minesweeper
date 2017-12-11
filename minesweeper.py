from MinesweeperGame import MinesweeperGame, MinesweeperGridState
from MinesweeperDisplay import MinesweeperDisplay

import pygame
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--level", help="choose the game level from the options: easy, med, hard, custom", choices=["easy", "med", "hard", "custom"])
parser.add_argument("-x", "--width", type=int, help="width of custom grid", default=9)
parser.add_argument("-y", "--height", type=int, help="height of custom grid", default=9)
parser.add_argument("-m", "--mines", type=int, help="number of mines in custom grid", default=10)
args = parser.parse_args()

pygame.init()

# --- setup ---

if args.level:
	if args.level == "easy":
		widthSetting = 9
		heightSetting = 9
		mineSetting = 10
	elif args.level == "med":
		widthSetting = 16
		heightSetting = 16
		mineSetting = 40
	elif args.level == "hard":
		widthSetting = 30
		heightSetting = 16
		mineSetting = 99
	elif args.level == "custom":
		widthSetting = args.width
		heightSetting = args.height
		mineSetting = args.mines
else:
	widthSetting = 9
	heightSetting = 9
	mineSetting = 10

game = MinesweeperGame(widthSetting, heightSetting, mineSetting)

display = MinesweeperDisplay(game)

done = False
clock = pygame.time.Clock()

# --- main loop ---

while not done:
	# --- handle events ---
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if display.gridRect().collidepoint(event.pos):
				"""game grid mouse down"""
				if game.running:
					if event.button == 3:
						game.flag(display.gridLocOfPos(event.pos))
					else:
						display.mouseDownLoc = display.gridLocOfPos(event.pos)
			elif display.smileyFaceRect().collidepoint(event.pos):
				"""smiley face button mousedown"""
				display.smileClicked = True
		elif event.type == pygame.MOUSEMOTION:
			if event.buttons[0] and game.running:
				if display.gridRect().collidepoint(event.pos):
					display.mouseDownLoc = display.gridLocOfPos(event.pos)
				else:
					display.mouseDownLoc = (-1, -1)
		elif event.type == pygame.MOUSEBUTTONUP:
			display.smileClicked = False
			display.mouseDownLoc = (-1, -1)
			if display.gridRect().collidepoint(event.pos):
				game.uncover(display.gridLocOfPos(event.pos))
			elif display.smileyFaceRect().collidepoint(event.pos):
				game = MinesweeperGame(widthSetting, heightSetting, mineSetting)
				display.reset(game)
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

