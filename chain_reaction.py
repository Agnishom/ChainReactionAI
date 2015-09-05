import copy

sgn = lambda n: 0 if n == 0 else n/abs(n)

class Board():
	def __init__(self, n=6, m=9, new_move=1):
		self.m = m
		self.n = n
		self.board = [[0 for i in xrange(self.n)] for i in xrange(self.m)]
		self.new_move = new_move
	def __getitem__(self, pos):
		return self.board[pos[0]][pos[1]]
	def __setitem__(self, pos, value):
		self.board[pos[0]][pos[1]]=value
	def __str__(self):
		s = ""
		for i in xrange(self.m):
			for j in xrange(self.n):
				s += str(self[(i,j)])
				s += " "
			s += "\n"
		return s
	def critical_mass(self,pos):
		if pos == (0,0) or pos == (self.m - 1, self.n - 1) or pos == (self.m - 1, 0) or pos == (0, self.n - 1):
			return 2
		elif pos[0] == 0 or pos[0] == self.m-1 or pos[1] == 0 or pos[1] == self.n-1:
			return 3
		else:
			return 4
	def neighbors(self,pos):
		n = []
		for i in [(pos[0],pos[1]+1), (pos[0],pos[1]-1), (pos[0]+1,pos[1]), (pos[0]-1,pos[1])]:
			if 0 <= i[0] < self.m and 0 <= i[1] < self.n:
				n.append(i)
		return n

def move(board, pos):
	board = copy.deepcopy(board)
	assert board.new_move == sgn(board[pos]) or 0 == sgn(board[pos])
	board[pos] = board[pos] + board.new_move
	while True:
		unstable = []
		for pos in [(x,y) for x in xrange(board.m) for y in xrange(board.n)]:
			if abs(board[pos]) >= board.critical_mass(pos):
				unstable.append(pos)
		#print board
		#raw_input()
		if not unstable:
			break
		for pos in unstable:
			board[pos] -= board.new_move*board.critical_mass(pos)
			for i in board.neighbors(pos):
				board[i] = sgn(board.new_move)*(abs(board[i])+1)
	board.new_move *= -1
	return board

def chains(board,player):
	board = copy.deepcopy(board)
	lengths = []
	for pos in [(x,y) for x in xrange(board.m) for y in xrange(board.n)]:
		if abs(board[pos]) == (board.critical_mass(pos) - 1) and sgn(board[pos]) == player:
			l = 0
			visiting_stack = []
			visiting_stack.append(pos)
			while visiting_stack:
				pos = visiting_stack.pop()
				board[pos] = 0
				l += 1
				for i in board.neighbors(pos):
					if abs(board[i]) == (board.critical_mass(i) - 1) and sgn(board[i]) == player:
						visiting_stack.append(i)
			lengths.append(l)
	return lengths


def score(board, player):
	sc = 0
	my_orbs, enemy_orbs = 0, 0
	for pos in [(x,y) for x in xrange(board.m) for y in xrange(board.n)]:
		if sgn(board[pos]) == player:
			my_orbs += abs(board[pos])
			flag_not_vulnerable = True
			for i in board.neighbors(pos):
				if sgn(board[i]) == -player and (abs(board[i]) == board.critical_mass(i) - 1):
					sc -= 5-board.critical_mass(pos)
					flag_not_vulnerable = False
			if flag_not_vulnerable:
				#The edge Heuristic
				if board.critical_mass(pos) == 3:
					sc += 2
				#The corner Heuristic
				elif board.critical_mass(pos) == 2:
					sc += 3
				#The unstability Heuristic
				if abs(board[pos]) == board.critical_mass(pos) - 1:
					sc += 2
				#The vulnerablity Heuristic
		else:
			enemy_orbs += abs(board[pos])
	#The number of Orbs Heuristic
	sc += my_orbs
	#You win when the enemy has no orbs
	if enemy_orbs == 0 and my_orbs > 1:
		return 1000
	#You loose when you have no orbs
	elif my_orbs == 0 and enemy_orbs > 1:
		return -1000
	#The chain Heuristic
	sc += sum([2*i for i in chains(board,player) if i > 1])
	return sc

def bestn(board,n=10):
	conf = {}
	for pos in [(x,y) for x in xrange(board.m) for y in xrange(board.n)]:
		if board.new_move == sgn(board[pos]) or 0 == sgn(board[pos]): 
			conf[pos] = score(move(board,pos),board.new_move)
			#Return just the winning position in case you find one
			if conf[pos]==1000:
				return [pos]
	return sorted(conf, key=conf.get, reverse=True)[:n]

def minimax(board,depth=3):
	best_moves = bestn(board,n=5)
	if depth == 1:
		return (best_moves[0], score(move(board,best_moves[0]),board.new_move))
	best_pos, best_val = 0, 0
	for b_new_pos in bestn(board):
		b_new = move(board,b_new_pos)
		val = minimax(b_new, depth=depth-1)[1]
		if val > best_val:
			best_val = val
			best_pos = b_new_pos
	return best_pos, best_val

def game():
	a = Board()
	while True:
		new_move = minimax(a)[0]
		print new_move
		a = move(a, new_move)
		print a
		#p = input()
		#a = move(a, p)
		#print a