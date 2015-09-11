import pygame
import minimax, structure
import thread

m, n = 9, 6

pygame.init()
surface = pygame.display.set_mode((50*n, 50*m))
pygame.display.set_caption('Chain Reaction')

def drawBoard(board=structure.Board()):
	surface.fill((0,0,0))
	font = pygame.font.Font('Font.ttf', 48)
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

def show_move(pos):
	rect = pygame.Rect(pos[1]*50,pos[0]*50,50,50)
	pygame.draw.rect(surface,(255,255,0),rect,0)
	pygame.display.update()
	pygame.time.wait(250)

def main():

	#start screen
	font = pygame.font.Font('Font.ttf', 72)
	text = font.render("Red", 1, (255,0,0))
	textpos = text.get_rect(centerx = 25*n, centery = 12*m)
	surface.blit(text, textpos)
	text = font.render("Green", 1, (0,255,0))
	textpos = text.get_rect(centerx = 25*n, centery = 36*m)
	surface.blit(text, textpos)
	font = pygame.font.Font('Font.ttf', 12)
	text = font.render("Choose a Color", 1, (100,100,100))
	textpos = text.get_rect(centerx = 25*n, centery = 25*m)
	surface.blit(text, textpos)
	pygame.display.update()

	this_loop = True
	while this_loop:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				y = pygame.mouse.get_pos()[1]
				if y < 25*m:
					player_first = True
				else:
					player_first = False
				this_loop = False

	#depth screen
	surface.fill((0,0,0))
	font = pygame.font.Font('Font.ttf', 12)
	text = font.render("How deep should I look?", 1, (100,100,100))
	textpos = text.get_rect(centerx = 25*n, centery = 12*m)
	surface.blit(text, textpos)
	font = pygame.font.Font('Font.ttf', 48)
	depth = 3
	text = font.render(str(depth),1,(255,255,0))
	textpos = text.get_rect(centerx = 25*n, centery = 25*m)
	surface.blit(text, textpos)
	pygame.display.update()

	this_loop = True
	while this_loop:
		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
				this_loop = False
			elif event.type == pygame.KEYDOWN:
				if chr(event.key) in '1234567890':
					rect = pygame.Rect(12*m,25*n,100,100)
					pygame.draw.rect(surface,(0,0,0),rect,0)
					pygame.display.update()
					depth = int(chr(event.key))
					text = font.render(str(depth),1,(255,255,0))
					textpos = text.get_rect(centerx = 25*n, centery = 25*m)
					surface.blit(text, textpos)
					pygame.display.update()


	#game screen
	board = structure.Board()
	drawBoard(board)

	if not player_first:
		new_move = minimax.minimax(board)[0]
		thread.start_new_thread(slowMove, (board, new_move))
		board = structure.move(board, new_move)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				x,y = pygame.mouse.get_pos()
				x,y = x/50,y/50
				show_move((y,x))
				thread.start_new_thread(slowMove, (board,(y,x)))
				board = structure.move(board,(y,x))
				new_move = minimax.minimax(board,depth)[0]
				show_move(new_move)
				thread.start_new_thread(slowMove, (board, new_move))
				board = structure.move(board, new_move)

if __name__ == "__main__":
	main()