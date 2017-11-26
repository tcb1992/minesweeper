import enum
import random

class MinesweeperGame:
	"""Stores game state for current game of Minesweeper - seperate state from presentation code"""

	def __init__(self, x, y, mines):

		if mines >= (x * y):
			raise ValueError("There must be more grid squares than mines")

		self.width = x
		self.height = y
		self.mineCount = mines
		self.started = False

		self.grid = [[MinesweeperGridState.COVERED_BLANK for x in range(self.width)] for y in range(self.height)]

		"""distribute mines"""
		distributedMines = 0
		while distributedMines < self.mineCount:
			loc_x = random.randint(0, self.width - 1)
			loc_y = random.randint(0, self.height - 1)
			if self.grid[loc_y][loc_x] == MinesweeperGridState.COVERED_BLANK:
				self.grid[loc_y][loc_x] = MinesweeperGridState.COVERED_MINE;
				distributedMines += 1


class MinesweeperGridState(enum.Enum):
	COVERED_BLANK = enum.auto()
	COVERED_MINE = enum.auto()
	UNCOVERED_BLANK = enum.auto()
	UNCOVERED_MINE = enum.auto()