# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random
import time

class BW(QWidget):
	def __init__(self,parent=None):
		super(BW,self).__init__(parent)
		self.initUI()

	def initUI(self):
	
		self.playerLetter=''
		self.computerLetter=''
		self.turn=''
		self.move = ' '
		self.gamestart =False
		self.btn=[]
		self.x =0
		self.y =0
		self.theboard = []
		
		newfont = QFont("Times", 48, QFont.Bold) 
		newfont2 = QFont("Times", 14, QFont.Bold) 
		newfont3 = QFont("Times", 24, QFont.Bold) 
		newfont4 = QFont("Times", 12, QFont.Bold) 
		
		#初始化8x8個Button
		for i in range(8):
			self.btn.append([' '] * 8) #宣告8x8
			
		for q in range(8):
			for w in range(8):
				self.btn[q][w] = QPushButton("")
				self.btn[q][w].setCheckable(False)
				self.btn[q][w].setFixedSize(60,60) #宣告8x8個Button size 為60x60
				self.btn[q][w].setFont(newfont)
				self.btn[q][w].clicked.connect(self.btn_click)

		#初始化棋盤	
		self.theboard=self.getNewBoard()	
		self.resetBoard(self.theboard)
		
		grid = QGridLayout()
		grid.setSpacing(1)
		
		self.btnO = QPushButton("O")
		self.btnX = QPushButton("X")
		self.btn_reset = QPushButton("重新開始")

		self.btnO.setFixedSize(80,60)
		self.btnX.setFixedSize(80,60)
		self.btn_reset.setFixedSize(160,60)

		self.btnO.setFont(newfont3)
		self.btnX.setFont(newfont3)
		self.btn_reset.setFont(newfont3)
		
		self.btnO.clicked.connect(lambda:self.btnOX_click(self.btnO))
		self.btnX.clicked.connect(lambda:self.btnOX_click(self.btnX))
		
		self.btn_reset.clicked.connect(self.btn_reset_click)
		
		self.contentEdit = QTextEdit()
		self.contentEdit.setFont(newfont2)
		self.contentEdit.append('歡迎來玩黑白棋小遊戲!')
		self.contentEdit.append('請在下面按鈕選擇你要X還是O?')

		self.LB0_str='電腦子數:00'
		self.LB0 = QLabel(self.LB0_str, self)
		self.LB0.setFont(QFont('SimHei', 14))
		self.LB0.setStyleSheet("color: rgb(0, 0, 255);")
		self.LB0.setFixedSize(240,60)
		
		self.LB1_str='玩家子數:00'
		self.LB1 = QLabel(self.LB1_str, self)
		self.LB1.setFont(QFont('SimHei', 14))
		self.LB1.setStyleSheet("color: rgb(0, 0, 255);")
		self.LB1.setFixedSize(240,60)
		
		for i in range(8):
			for j in range(8):
				grid.addWidget(self.btn[i][j], j, i)

		grid.addWidget(self.LB0, 8, 0,1,4)
		grid.addWidget(self.LB1, 8, 4,1,4)						
		grid.addWidget(self.btnO, 8, 8)
		grid.addWidget(self.btnX, 8, 9)
		grid.addWidget(self.btn_reset, 8, 10,1,2)
		grid.addWidget(self.contentEdit, 0, 8, 8, 4)
		  
		self.setLayout(grid)
		self.setGeometry(200, 100, 800, 600)
		self.setWindowTitle('黑白棋 小遊戲')
	
	
	def resetBoard(self,board):
		# Blanks out the board it is passed, except for the original starting position.
		for x in range(8):
			for y in range(8):
				board[x][y] = ' '
				self.btn[x][y].setCheckable(False)
		# Starting pieces:
		board[3][3] = 'X'
		board[3][4] = 'O'
		board[4][3] = 'O'
		board[4][4] = 'X'

		self.btn[3][3].setText("X")	
		self.btn[3][4].setText("O")	
		self.btn[4][3].setText("O")	
		self.btn[4][4].setText("X")	
		
	def getNewBoard(self):
		# Creates a brand new, blank board data structure.
		board = []
		for i in range(8):
			board.append([' '] * 8)
		return board	
		
	def SetButtonCheckable(self):	
		#設定button可以Checkable
		for q in range(8):
				for w in range(8):	
					self.btn[q][w].setCheckable(True)
		self.btn[3][3].setCheckable(False)
		self.btn[3][4].setCheckable(False)
		self.btn[4][3].setCheckable(False)
		self.btn[4][4].setCheckable(False)		
	
	def whoGoesFirst(self):
		# Randomly choose the player who goes first.
		if random.randint(0, 1) == 0:
			return 'computer'
		else:
			return 'player'	
	
	def inputPlayerLetter(self):
		if self.playerLetter=='':
			self.contentEdit.append('請先在下面按鈕選擇你要X還是O?')
			return False 
		else:
			return True
			
	def getScoreOfBoard(self,board):
		# Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
		xscore = 0
		oscore = 0
		for x in range(8):
			for y in range(8):
				if board[x][y] == 'X':
					xscore += 1
				if board[x][y] == 'O':
					oscore += 1
		if self.playerLetter=='O':
			self.LB1.setText('玩家子數:'+str(oscore))	
			self.LB0.setText('電腦子數:'+str(xscore))	
		else:
			self.LB1.setText('玩家子數:'+str(xscore))	
			self.LB0.setText('電腦子數:'+str(oscore))
		return {'X':xscore, 'O':oscore}
			
	def getBoardCopy(self,board):
		# Make a duplicate of the board list and return the duplicate.
		dupeBoard = self.getNewBoard()
		for x in range(8):
			for y in range(8):
				dupeBoard[x][y] = board[x][y]
		return dupeBoard	
		
	def isOnCorner(self,x, y):
		# Returns True if the position is in one of the four corners.
		return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)
		
	def isValidMove(self,board, tile, xstart, ystart):
		# Returns False if the player's move on space xstart, ystart is invalid.
		# If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
		if board[xstart][ystart] != ' ' or not self.isOnBoard(xstart, ystart):
			return False

		board[xstart][ystart] = tile # temporarily set the tile on the board.

		if tile == 'X':
			otherTile = 'O'
		else:
			otherTile = 'X'

		tilesToFlip = []
		for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
			x, y = xstart, ystart
			x += xdirection # first step in the direction
			y += ydirection # first step in the direction
			if self.isOnBoard(x, y) and board[x][y] == otherTile:
				# There is a piece belonging to the other player next to our piece.
				x += xdirection
				y += ydirection
				if not self.isOnBoard(x, y):
					continue
				while board[x][y] == otherTile:
					x += xdirection
					y += ydirection
					if not self.isOnBoard(x, y): # break out of while loop, then continue in for loop
						break
				if not self.isOnBoard(x, y):
					continue
				if board[x][y] == tile:
					# There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
					while True:
						x -= xdirection
						y -= ydirection
						if x == xstart and y == ystart:
							break
						tilesToFlip.append([x, y])

		board[xstart][ystart] = ' ' # restore the empty space
		if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
			return False
		return tilesToFlip
	
	
	def getValidMoves(self,board, tile):
		# Returns a list of [x,y] lists of valid moves for the given player on the given board.
		validMoves = []

		for x in range(8):
			for y in range(8):
				if self.isValidMove(board, tile, x, y) != False:
					validMoves.append([x, y])
		return validMoves
		
	def makeMove(self,board, tile, xstart, ystart):
		# Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
		# Returns False if this is an invalid move, True if it is valid.
		tilesToFlip = self.isValidMove(board, tile, xstart, ystart)

		if tilesToFlip == False:
			return False
		board[xstart][ystart] = tile
		for x, y in tilesToFlip:
			board[x][y] = tile
			self.btn[x][y].setText(tile)	

		return True
		
		
	def makeMove_C(self,board, tile, xstart, ystart):
		# Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
		# Returns False if this is an invalid move, True if it is valid.
		tilesToFlip = self.isValidMove(board, tile, xstart, ystart)

		if tilesToFlip == False:
			return False
		board[xstart][ystart] = tile
		for x, y in tilesToFlip:
			board[x][y] = tile
		return True	
		
		
	def setothercheck_True(self,board):
		for x in range(8):
			for y in range(8):
				if board[x][y] != 'O' or  board[x][y] != 'X'  :
					self.btn[x][y].setCheckable(True)

	def getComputerMove(self,board, computerTile):
		# Given a board and the computer's tile, determine where to
		# move and return that move as a [x, y] list.
		possibleMoves = self.getValidMoves(board, computerTile)
		# randomize the order of the possible moves
		random.shuffle(possibleMoves)
		# always go for a corner if available.
		for x, y in possibleMoves:
			if self.isOnCorner(x, y):
				return [x, y]

		# Go through all the possible moves and remember the best scoring move
		bestScore = -1
		for x, y in possibleMoves:
			dupeBoard = self.getBoardCopy(board)
			self.makeMove_C(dupeBoard, computerTile, x, y)
			score = self.getScoreOfBoard(dupeBoard)[computerTile]
			if score > bestScore:
				bestMove = [x, y]
				bestScore = score
				
		return bestMove
	
	def btn_click(self):		
		if self.inputPlayerLetter() :
			for q in range(8):
				for w in range(8):
					if	self.btn[q][w].isChecked():
						self.x=q
						self.y=w
			if self.isValidMove(self.theboard, self.playerLetter, self.x, self.y) != False:
				if self.getValidMoves(self.theboard, self.playerLetter) != []  :
					self.btn[self.x][self.y].setCheckable(False)
					self.btn[self.x][self.y].setText(self.playerLetter)	
					self.setothercheck_True(self.theboard)
					self.makeMove(self.theboard, self.playerLetter, self.x, self.y)
				self.turn='computer'
			else:
				self.btn[self.x][self.y].setCheckable(False)
				self.contentEdit.append('這裡不能下子!')
			self.repaint()
			time.sleep(1)
			
			if self.getValidMoves(self.theboard, self.computerLetter) != []  :
				if	self.turn=='computer':
					x_c,y_c=self.getComputerMove(self.theboard, self.computerLetter)
					self.makeMove(self.theboard, self.computerLetter, x_c, y_c)
					self.btn[x_c][y_c].setCheckable(False)
					self.btn[x_c][y_c].setText(self.computerLetter)	
					self.turn='player'
			
			if self.getValidMoves(self.theboard, self.computerLetter) == [] and self.getValidMoves(self.theboard, self.playerLetter) == [] :
				self.contentEdit.append('遊戲結束!')
				scores=self.getScoreOfBoard(self.theboard)
				if scores[self.playerLetter] > scores[self.computerLetter]:
					self.contentEdit.append('恭喜你贏了電腦!')
				elif scores[self.playerLetter] < scores[self.computerLetter]:
					self.contentEdit.append('你輸了電腦!')
				else:
					self.contentEdit.append('遊戲平手!')
		
	def isOnBoard(self,x, y):
		# Returns True if the coordinates are located on the board.
		return x >= 0 and x <= 7 and y >= 0 and y <=7	

	def btnOX_click(self,btn):	
		if btn.text()=="O":
			self.contentEdit.append('你選擇了O')
			self.playerLetter='O'
			self.computerLetter='X'
		else:
			self.contentEdit.append('你選擇了X')
			self.playerLetter='X'
			self.computerLetter='O'
			
		self.btnO.setEnabled(False)
		self.btnX.setEnabled(False)
		self.turn=self.whoGoesFirst()
		self.gamestart =True
		if self.turn=='computer':
			self.contentEdit.append('隨機決定順序，電腦先下...')
			x_c,y_c=self.getComputerMove(self.theboard, self.computerLetter)
			self.makeMove(self.theboard, self.computerLetter, x_c, y_c)
			self.btn[x_c][y_c].setCheckable(False)
			self.btn[x_c][y_c].setText(self.computerLetter)	
			self.turn='player'
		else:
			self.contentEdit.append('隨機決定順序，玩家先下...')
		self.SetButtonCheckable()
	
	def btn_reset_click(self):		
		self.btnO.setEnabled(True)
		self.btnX.setEnabled(True)		
		for q in range(8):
			for w in range(8):
				self.btn[q][w].setText('')	
				self.btn[q][w].setEnabled(True)	
				self.btn[q][w].setCheckable(True)
		self.LB0.setText('電腦子數:00')	
		self.LB1.setText('玩家子數:00')	
		self.contentEdit.setText('歡迎來玩黑白棋小遊戲!')
		self.contentEdit.append('請在下面按鈕選擇你要X還是O?')
		self.playerLetter=''
		self.computerLetter=''
		self.turn=''
		self.move = ''
		#初始化棋盤	
		self.theboard=self.getNewBoard()	
		self.resetBoard(self.theboard)
		
if __name__ == "__main__":
		app = QApplication(sys.argv)
		form = BW()
		form.show()
		sys.exit(app.exec_())
