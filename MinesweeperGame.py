import enum
import random
from functools import reduce

class MinesweeperGame:
	"""Stores game state for current game of Minesweeper - seperate state from presentation code"""

	def __init__(self, x, y, mines):

		if mines >= (x * y):
			raise ValueError("There must be more grid squares than mines")

		if (x < 8):
			raise ValueError("Minimum width is 8 squares")

		self.width = x
		self.height = y
		self.mineCount = mines
		self.running = False
		self.over = False
		self.won = False
		self.time = 0

		self.grid = [[MinesweeperGridState.COVERED for x in range(self.width)] for y in range(self.height)]

		"""distribute mines"""
		distributedMines = 0
		while distributedMines < self.mineCount:
			loc = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
			if self.state(loc) == MinesweeperGridState.COVERED:
				self.setState(loc, MinesweeperGridState.COVERED | MinesweeperGridState.MINE);
				distributedMines += 1

	def flag(self, loc):
		if not self.running:
			self.running = True
		if self.state(loc) & MinesweeperGridState.COVERED:
			if self.state(loc) & MinesweeperGridState.FLAGGED:
				self.setState(loc, self.state(loc) & ~MinesweeperGridState.FLAGGED)
			else:
				self.setState(loc, self.state(loc) | MinesweeperGridState.FLAGGED)

	def uncover(self, loc):
		if not self.over:
			if not self.running:
				self.running = True
			if (self.state(loc) & MinesweeperGridState.COVERED) and not (self.state(loc) & MinesweeperGridState.FLAGGED):
				self.setState(loc, self.state(loc) & ~MinesweeperGridState.COVERED)
				if self.state(loc) & MinesweeperGridState.MINE:
					#game over
					self.lose()
				elif self.gridNumber(loc) == 0:
					for loc in self.neighbours(loc):
						if (self.state(loc) & MinesweeperGridState.COVERED) and not (self.state(loc) & MinesweeperGridState.FLAGGED):
							self.uncover(loc)

	def gridNumber(self, loc):
		if self.state(loc) & MinesweeperGridState.MINE:
			return 0
		else:
			return sum(map(lambda loc: bool(self.state(loc) & MinesweeperGridState.MINE), self.neighbours(loc)))

	def state(self, loc):
		return self.grid[loc[1]][loc[0]]

	def setState(self, loc, val):
		self.grid[loc[1]][loc[0]] = val

	def neighbours(self, loc):
		returnVal = []
		if loc[0] > 0:
			returnVal.append((loc[0] - 1, loc[1]))
			if loc[1] > 0:
				returnVal.append((loc[0] - 1, loc[1] - 1))
			if loc[1] < self.height - 1:
				returnVal.append((loc[0] - 1, loc[1] + 1))
		if loc[1] > 0:
			returnVal.append((loc[0], loc[1] - 1))
		if loc[1] < self.height - 1:
			returnVal.append((loc[0], loc[1] + 1))
		if loc[0] < self.width - 1:
			returnVal.append((loc[0] + 1, loc[1]))
			if loc[1] > 0:
				returnVal.append((loc[0] + 1, loc[1] - 1))
			if loc[1] < self.height - 1:
				returnVal.append((loc[0] + 1, loc[1] + 1))
		return returnVal

	def updateClock(self, milliseconds):
		if self.running:
			self.time += milliseconds

	def lose(self):
		self.running = False
		self.over = True

	def win(self):
		self.running = False
		self.over = True
		self.won = True

		for x in range(self.width):
			for y in range(self.height):
				if (self.state((x, y)) & MinesweeperGridState.MINE) and (self.state((x, y)) & MinesweeperGridState.COVERED):
					self.setState((x, y), self.state((x, y)) | MinesweeperGridState.FLAGGED)

	def hasWon(self):
		for x in range(self.width):
			for y in range(self.height):
				if not (self.state((x, y)) & MinesweeperGridState.MINE) and (self.state((x, y)) & MinesweeperGridState.COVERED):
					return False;
		return True;

	def numFlags(self):
		flagCount = 0
		for x in range(self.width):
			for y in range(self.height):
				if self.state((x, y)) & MinesweeperGridState.FLAGGED:
					flagCount += 1
		return flagCount



class MinesweeperGridState(enum.Flag):
	MINE = enum.auto()
	COVERED = enum.auto()
	FLAGGED = enum.auto()
	Q_MARK = enum.auto()
