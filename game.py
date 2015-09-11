import pygame
import minimax, structure

m, n = 9, 6

pygame.init()
surface = pygame.display.set_mode((50*n, 50*m))
pygame.display.set_caption('Chain Reaction')
font = pygame.font.Font('Font.ttf', 48)

def drawBoard(board=structure.Board()):
	surface.fill((0,0,0))
	for pos in [(x,y) for x in xrange(board.m) for y in xrange(board.n)]:
		if structure.sgn(board[pos]) == 0:
			color = (255,255,255)
		elif structure.sgn(board[pos]) == 1:
			color = (255,0,0)
		else:
			color = (0,255,0)
		text = font.render(str(board[pos])[-1], 1, color)
		textpos = text.get_rect(centerx = pos[1]*50 + 25, centery = pos[0]*50 + 25)
		surface.blit(text, textpos)
	pygame.display.update()

def main():
	board = structure.Board()
	drawBoard(board)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				x,y = pygame.mouse.get_pos()
				x,y = x/50,y/50
				try:
					board = structure.move(board,(y,x))
					drawBoard(board)
				except:
					pass