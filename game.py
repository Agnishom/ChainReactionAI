import pygame
import minimax, structure
import thread

m, n = 9, 6

pygame.init()
surface = pygame.display.set_mode((50*n, 50*m))
pygame.display.set_caption('Chain Reaction')
lock = thread.allocate_lock()

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
	lock.release()

def show_move(pos):
	rect = pygame.Rect(pos[1]*50,pos[0]*50,50,50)
	pygame.draw.rect(surface,(255,255,0),rect,0)
	pygame.display.update()
	pygame.time.wait(250)


def main():
	global m,n, surface

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

	#rows screen
	surface.fill((0,0,0))
	font = pygame.font.Font('Font.ttf', 12)
	text = font.render("How many rows?", 1, (100,100,100))
	textpos = text.get_rect(centerx = 25*n, centery = 12*m)
	surface.blit(text, textpos)
	font = pygame.font.Font('Font.ttf', 48)
	rows = 9
	text = font.render(str(rows),1,(255,255,0))
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
					rows = int(chr(event.key))
					text = font.render(str(rows),1,(255,255,0))
					textpos = text.get_rect(centerx = 25*n, centery = 25*m)
					surface.blit(text, textpos)
					pygame.display.update()

	#columns screen
	surface.fill((0,0,0))
	font = pygame.font.Font('Font.ttf', 12)
	text = font.render("How many columns?", 1, (100,100,100))
	textpos = text.get_rect(centerx = 25*n, centery = 12*m)
	surface.blit(text, textpos)
	font = pygame.font.Font('Font.ttf', 48)
	columns = 6
	text = font.render(str(columns),1,(255,255,0))
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
					columns = int(chr(event.key))
					text = font.render(str(columns),1,(255,255,0))
					textpos = text.get_rect(centerx = 25*n, centery = 25*m)
					surface.blit(text, textpos)
					pygame.display.update()


	#some initialization code
	m, n = rows, columns
	surface = pygame.display.set_mode((50*n, 50*m))
	pygame.display.set_caption('Chain Reaction')
	board = structure.Board(m=m,n=n)
	total_moves = 0

	#game screen
	drawBoard(board)

	if not player_first:
		new_move = minimax.minimax(board)[0]
		lock.acquire()
		thread.start_new_thread(slowMove, (board, new_move))
		board = structure.move(board, new_move)
		total_moves += 1

	this_loop = True
	while this_loop:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				x,y = pygame.mouse.get_pos()
				x,y = x/50,y/50
				show_move((y,x))
				lock.acquire()
				thread.start_new_thread(slowMove, (board,(y,x)))
				board = structure.move(board,(y,x))
				total_moves += 1
				if total_moves >= 2:
					if structure.score(board,board.new_move*(-1)) == 10000:
						winner = board.new_move*(-1)
						this_loop = False
						break
				new_move = minimax.minimax(board,depth)[0]
				show_move(new_move)
				lock.acquire()
				thread.start_new_thread(slowMove, (board, new_move))
				board = structure.move(board, new_move)
				total_moves += 1
				if total_moves >= 2:
					if structure.score(board,board.new_move*(-1)) == 10000:
						winner = board.new_move*(-1)
						this_loop = False
						break

	#winning screen
	while lock.locked():
		continue
	m, n = 9, 6
	surface = pygame.display.set_mode((50*n, 50*m))
	font = pygame.font.Font('Font.ttf', 72)
	pygame.display.set_caption('Chain Reaction')
	if winner == -1:
		text = font.render("Red", 1, (255,0,0))
	else:
		text = font.render("Green", 1, (0,255,0))
	textpos = text.get_rect(centerx = 25*n, centery = 12*m)
	surface.blit(text, textpos)
	font = pygame.font.Font('Font.ttf', 48)
	text = font.render("Wins!", 1, (100,100,100))
	textpos = text.get_rect(centerx = 25*n, centery = 25*m)
	surface.blit(text, textpos)
	pygame.display.update()


if __name__ == "__main__":
	main()