from MinesweeperGame import MinesweeperGame, MinesweeperGridState
import pygame
import math

class MinesweeperDisplay:

	def __init__(self, game):
		
		self.game = game
		self.screen = pygame.display.set_mode(self.pixelSize())
		pygame.display.set_caption("Minesweeper")

		self.GREY = (0xC0, 0xC0, 0xC0)
		self.mouseDownLoc = (-1, -1)
		self.smileClicked = False

		spriteImage = pygame.image.load("sprites.gif").convert()

		self.sprites = {
			"NUMBER_0": spriteImage.subsurface(0, 0, 13, 23),
			"NUMBER_1": spriteImage.subsurface(13, 0, 13, 23),
			"NUMBER_2": spriteImage.subsurface(26, 0, 13, 23),
			"NUMBER_3": spriteImage.subsurface(39, 0, 13, 23),
			"NUMBER_4": spriteImage.subsurface(52, 0, 13, 23),
			"NUMBER_5": spriteImage.subsurface(65, 0, 13, 23),
			"NUMBER_6": spriteImage.subsurface(78, 0, 13, 23),
			"NUMBER_7": spriteImage.subsurface(91, 0, 13, 23),
			"NUMBER_8": spriteImage.subsurface(104, 0, 13, 23),
			"NUMBER_9": spriteImage.subsurface(117, 0, 13, 23),
			"NUMBER_-": spriteImage.subsurface(130, 0, 13, 23),
			"UNCOVERED_BLANK": spriteImage.subsurface(0, 23, 16, 16),
			"UNCOVERED_1": spriteImage.subsurface(16, 23, 16, 16),
			"UNCOVERED_2": spriteImage.subsurface(32, 23, 16, 16),
			"UNCOVERED_3": spriteImage.subsurface(48, 23, 16, 16),
			"UNCOVERED_4": spriteImage.subsurface(64, 23, 16, 16),
			"UNCOVERED_5": spriteImage.subsurface(80, 23, 16, 16),
			"UNCOVERED_6": spriteImage.subsurface(96, 23, 16, 16),
			"UNCOVERED_7": spriteImage.subsurface(112, 23, 16, 16),
			"UNCOVERED_8": spriteImage.subsurface(128, 23, 16, 16),
			"COVERED_BLANK": spriteImage.subsurface(0, 39, 16, 16),
			"COVERED_FLAG": spriteImage.subsurface(16, 39, 16, 16),
			"UNCOVERED_RED_MINE": spriteImage.subsurface(32, 39, 16, 16),
			"UNCOVERED_WRONG_MINE": spriteImage.subsurface(48, 39, 16, 16),
			"UNCOVERED_MINE": spriteImage.subsurface(64, 39, 16, 16),
			"COVERED_?": spriteImage.subsurface(80, 39, 16, 16),
			"UNCOVERED_?": spriteImage.subsurface(96, 39, 16, 16),
			"SMILE_FACE": spriteImage.subsurface(0, 55, 26, 26),
			"CLICKED_SMILE_FACE": spriteImage.subsurface(26, 55, 26, 26),
			"O_FACE": spriteImage.subsurface(52, 55, 26, 26),
			"DEAD_FACE": spriteImage.subsurface(78, 55, 26, 26),
			"SUNGLASSES_FACE": spriteImage.subsurface(104, 55, 26, 26),
			"BORDER_TL": spriteImage.subsurface(0, 81, 10, 10),
			"BORDER_TR": spriteImage.subsurface(10, 81, 10, 10),
			"BORDER_BL": spriteImage.subsurface(20, 81, 10, 10),
			"BORDER_BR": spriteImage.subsurface(30, 81, 10, 10),
			"BORDER_HORISONTAL": spriteImage.subsurface(40, 81, 16, 10),
			"BORDER_ML": spriteImage.subsurface(56, 81, 10, 10),
			"BORDER_MR": spriteImage.subsurface(66, 81, 10, 10),
			"BORDER_VERTICAL": spriteImage.subsurface(134, 39, 10, 16)
		}

	def pixelSize(self):
		width = self.game.width * 16 #grid squares are 16px
		height = self.game.height * 16
		width += 20 #side borders are 10
		height += 10 + 52 #bottom border is 10, top border is 2*10 + 32

		return (width, height)

	def gridSize(self):
		return (16*self.game.width, 16*self.game.height)

	def gridLoc(self):
		return (10, 52)

	def gridRect(self):
		return pygame.Rect(self.gridLoc(), self.gridSize())

	def smileyFaceRect(self):
		return pygame.Rect((self.pixelSize()[0]/2 - 13, 13), (26, 26))

	def gridLocOfPos(self, pos):
		#floor division: //
		return ((pos[0] - 10)//16, (pos[1] - 52)//16)

	def gridSprite(self, loc):
		state = self.game.state(loc)
		if self.game.over and not self.game.won:
			if not (state & MinesweeperGridState.COVERED) and (state & MinesweeperGridState.MINE):
				return "UNCOVERED_RED_MINE"
			elif state & MinesweeperGridState.COVERED:
				if state & MinesweeperGridState.FLAGGED:
					if state & MinesweeperGridState.MINE:
						return "COVERED_FLAG"
					else:
						return "UNCOVERED_WRONG_MINE"
				elif state & MinesweeperGridState.MINE:
					return "UNCOVERED_MINE"


		if state & MinesweeperGridState.COVERED:
			if state & MinesweeperGridState.FLAGGED:
				return "COVERED_FLAG"
			elif state & MinesweeperGridState.Q_MARK:
				return "COVERED_?"
			elif self.mouseDownLoc == loc:
				return "UNCOVERED_BLANK"
			else:
				return "COVERED_BLANK"
		else:
			gridNumber = self.game.gridNumber(loc)
			if gridNumber == 0:
				return "UNCOVERED_BLANK"
			else:
				return "UNCOVERED_" + str(gridNumber)

	def timeVal(self):
		return math.floor(self.game.time/1000)

	def numberSprites(self, num):
		digits = (math.floor(num/100) % 10, math.floor(num/10) % 10, math.floor(num) % 10)
		return list(map(lambda x: self.sprites["NUMBER_" + str(x)], digits))

	def smileState(self):
		if self.smileClicked:
			return "CLICKED_SMILE_FACE"
		elif self.game.running and not self.mouseDownLoc == (-1, -1):
			return "O_FACE"
		elif not self.game.running and self.game.over and self.game.won:
			return "SUNGLASSES_FACE"
		elif not self.game.running and self.game.over and not self.game.won:
			return "DEAD_FACE"
		else:
			return "SMILE_FACE"

	def reset(self, game):
		self.game = game
		self.screen = pygame.display.set_mode(self.pixelSize())
		pygame.display.set_caption("Minesweeper")
		self.mouseDownLoc = (-1, -1)
		self.smileClicked = False		

	def draw(self):
		self.screen.fill(self.GREY)

		#draw borders
		#top left
		self.screen.blit(self.sprites["BORDER_TL"], (0, 0))
		#top
		for x in range(self.game.width):
			self.screen.blit(self.sprites["BORDER_HORISONTAL"], (10+16*x, 0))
		#top right
		self.screen.blit(self.sprites["BORDER_TR"], (10+16*self.game.width, 0))
		#header sides
		self.screen.blit(self.sprites["BORDER_VERTICAL"], (0, 10))
		self.screen.blit(self.sprites["BORDER_VERTICAL"], (0, 26))
		self.screen.blit(self.sprites["BORDER_VERTICAL"], (10+16*self.game.width, 10))
		self.screen.blit(self.sprites["BORDER_VERTICAL"], (10+16*self.game.width, 26))
		#header/game border
		self.screen.blit(self.sprites["BORDER_ML"], (0, 42))
		for x in range(self.game.width):
			self.screen.blit(self.sprites["BORDER_HORISONTAL"], (10+16*x, 42))
		self.screen.blit(self.sprites["BORDER_MR"], (10+16*self.game.width, 42))
		#sides
		for y in range(self.game.height):
			self.screen.blit(self.sprites["BORDER_VERTICAL"], (0, 52+16*y))
			self.screen.blit(self.sprites["BORDER_VERTICAL"], (10+16*self.game.width, 52+16*y))
		#bottom left
		self.screen.blit(self.sprites["BORDER_BL"], (0, 52+16*self.game.height))
		#bottom
		for x in range(self.game.width):
			self.screen.blit(self.sprites["BORDER_HORISONTAL"], (10+16*x, 52+16*self.game.height))
		#bottom right
		self.screen.blit(self.sprites["BORDER_BR"], (10+16*self.game.width, 52+16*self.game.height))

		#grid
		for y in range(self.game.height):
			for x in range(self.game.width):
				self.screen.blit(self.sprites[self.gridSprite((x, y))], (10+16*x, 52+16*y))

		#timer
		timerSprites = self.numberSprites(self.timeVal())
		self.screen.blit(timerSprites[0], ((20+16*self.game.width) - 55, 14))
		self.screen.blit(timerSprites[1], ((20+16*self.game.width) - 42, 14))
		self.screen.blit(timerSprites[2], ((20+16*self.game.width) - 29, 14))

		#smiley face
		self.screen.blit(self.sprites[self.smileState()], self.smileyFaceRect())

		#flag count
		flagCount = self.game.mineCount - self.game.numFlags()
		if flagCount < 0:
			flagCount = 0
		flagCountSprites = self.numberSprites(flagCount)
		self.screen.blit(flagCountSprites[0], (16, 14))
		self.screen.blit(flagCountSprites[1], (29, 14))
		self.screen.blit(flagCountSprites[2], (42, 14))

		pygame.display.flip()
