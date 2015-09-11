import pygame
import minimax, structure
import thread

m, n = 9, 6

pygame.init()
surface = pygame.display.set_mode((50*n, 50*m))
pygame.display.set_caption('Chain Reaction')
font = pygame.font.Font('Font.ttf', 48)

def drawBoard(board=structure.Board()):
	surface.fill((0,0,0))
	for pos in [(x,y) for x in xrange(board.m) for y in xrange(board.n)]:
		if abs(board[pos]) >= board.critical_mass(pos):
			color = (255,255,0)
		elif structure.sgn(board[pos]) == 0:
			color = (255,255,255)
		elif structure.sgn(board[pos]) == 1:
			color = (255,0,0)
		else:
			color = (0,255,0)
		text = font.render(str(board[pos])[-1], 1, color)
		textpos = text.get_rect(centerx = pos[1]*50 + 25, centery = pos[0]*50 + 25)
		surface.blit(text, textpos)
	pygame.display.update()

def slowMove(board, pos):
	board = structure.copy.deepcopy(board)
	assert board.new_move == structure.sgn(board[pos]) or 0 == structure.sgn(board[pos])
	board[pos] = board[pos] + board.new_move
	while True:
		drawBoard(board)
		pygame.time.wait(250)
		unstable = []
		for pos in [(x,y) for x in xrange(board.m) for y in xrange(board.n)]:
			if abs(board[pos]) >= board.critical_mass(pos):
				unstable.append(pos)
		#raw_input()
		if not unstable:
			break
		for pos in unstable:
			board[pos] -= board.new_move*board.critical_mass(pos)
			for i in board.neighbors(pos):
				board[i] = structure.sgn(board.new_move)*(abs(board[i])+1)
	drawBoard(board)

def main():
	board = structure.Board()
	drawBoard(board)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				x,y = pygame.mouse.get_pos()
				x,y = x/50,y/50
				thread.start_new_thread(slowMove, (board,(y,x)))
				board = structure.move(board,(y,x))
				new_move = minimax.minimax(board)[0]
				print "am here"
				thread.start_new_thread(slowMove, (board, new_move))
				board = structure.move(board, new_move)

if __name__ == "__main__":
	main()