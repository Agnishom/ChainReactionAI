from structure import *

def bestn(board,n=10):
	conf = {}
	for pos in [(x,y) for x in xrange(board.m) for y in xrange(board.n)]:
		if board.new_move == sgn(board[pos]) or 0 == sgn(board[pos]): 
			conf[pos] = score(move(board,pos),board.new_move)
			#Return just the winning position in case you find one
			if conf[pos]==10000:
				return [pos]
	return sorted(conf, key=conf.get, reverse=True)[:n]

def minimax(board,depth=3,breadth=5):
	best_moves = bestn(board,n=breadth)
	best_pos, best_val = (best_moves[0], score(move(board,best_moves[0]),board.new_move))
	if depth == 1:
		return best_pos, best_val
	for b_new_pos in bestn(board):
		b_new = move(board,b_new_pos)
		val = minimax(b_new, depth=depth-1)[1]
		if val > best_val:
			best_val = val
			best_pos = b_new_pos
	return best_pos, best_val