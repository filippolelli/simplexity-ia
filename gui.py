import math
import sys 
from simplexity import GameState, Simplexity
from ai_player import ai_player
from variables import *
from checkers import *
import pygame
from grid import Grid,Square
from piece import Piece

def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
    #print("screen.blit...", screen.blit(text_render, (x, y)))
    return screen.blit(text_render, (x, y)) # this is a rect pygame.Rect

def draw_board(board:Grid):
	#pygame.draw.rect(screen, BLUE_COLOR, (0, SQUARESIZE, SQUARESIZE*7, SQUARESIZE*8))
	for c in range(COLS):
		for r in range(ROWS):
			pygame.draw.rect(screen, BLUE_COLOR, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.rect(screen, BLACK_COLOR, (int(c*SQUARESIZE+SQUARESIZE/3), int(r*SQUARESIZE+4*SQUARESIZE/3), SQUARESIZE-20, SQUARESIZE-20))
	
	pygame.draw.rect(screen, BLUE_COLOR, (COLS*SQUARESIZE, SQUARESIZE, SQUARESIZE/3, SQUARESIZE*ROWS))
	pygame.draw.rect(screen, BLUE_COLOR, (0, ROWS*SQUARESIZE+SQUARESIZE, SQUARESIZE*COLS+SQUARESIZE/3, SQUARESIZE/3))
	

	for c in range(COLS):
		for r in range(ROWS):		
			if board.get_square(r,c).is_empty():
				continue
			piece:Piece = board.get_square(r,c).get_piece()
			if piece.get_shape() == ROUND:
				if(piece.get_color() == WHITE):
					pygame.draw.circle(screen, WHITE_COLOR, (int(c*SQUARESIZE+2*SQUARESIZE/3), int(r*SQUARESIZE+5*SQUARESIZE/3)), RADIUS)
				else: pygame.draw.circle(screen, RED_COLOR, (int(c*SQUARESIZE+2*SQUARESIZE/3), int(r*SQUARESIZE+5*SQUARESIZE/3)), RADIUS)
			else:
				if(piece.get_color() == WHITE):
					pygame.draw.rect(screen, WHITE_COLOR, (int(c*SQUARESIZE+SQUARESIZE/3+2), int(r*SQUARESIZE+4*SQUARESIZE/3+2), SQUARESIZE-30, SQUARESIZE-30))
				else: pygame.draw.rect(screen, RED_COLOR, (int(c*SQUARESIZE+SQUARESIZE/3+2), int(r*SQUARESIZE+4*SQUARESIZE/3+2), SQUARESIZE-30, SQUARESIZE-30))
	pygame.display.update()



if __name__=="__main__":
	game = Simplexity()
	state = game.initial
	board = state.grid
	current_shape=ROUND
	pygame.init()

	

	width = COLS * SQUARESIZE + SQUARESIZE/3
	height = (ROWS+1) * SQUARESIZE
	size = (width,720)

	RADIUS = int(SQUARESIZE/3 - 3)
	
	screen = pygame.display.set_mode(size)
	b1 = button(screen, (0, 600), "Change piece")
	draw_board(board)
	pygame.display.update()

	myfont = pygame.font.SysFont("Arial",20)

	turn = state.to_move
	end = False

	while (not end):
		pygame.draw.rect(screen, BLACK_COLOR, (265,600, width-265, 30))
		label = myfont.render(f"Hai a disposizione {state.pieces[state.to_move][SQUARE]} quadrati e {state.pieces[state.to_move][ROUND]} cerchi",False,WHITE_COLOR)
		screen.blit(label,(265,600))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			
			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK_COLOR, (0,0, width, SQUARESIZE))
				posx = event.pos[0]
				if turn == WHITE:
					if(current_shape == ROUND):
						pygame.draw.circle(screen, WHITE_COLOR, (posx, int(5*SQUARESIZE/3-SQUARESIZE)), RADIUS)
					else:
						pygame.draw.rect(screen, WHITE_COLOR, (posx, int(4*SQUARESIZE/3-SQUARESIZE), SQUARESIZE-30, SQUARESIZE-30))

			pygame.display.update()

			if event.type==pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK_COLOR, (0,0, width, SQUARESIZE))
				if b1.collidepoint(pygame.mouse.get_pos()):
					current_shape = SQUARE if current_shape==ROUND else ROUND
				else:
					if(turn == WHITE):
						posx = event.pos[0]
						col = int(min(6,math.floor(posx/SQUARESIZE)))
						grid = state.grid
						pieces = state.pieces
						piece = Piece(current_shape,state.to_move)
						row=grid.make_move(col,piece)

						if(row < 0):
							continue
						pieces[state.to_move][current_shape]-=1
						state=GameState(to_move=abs(state.to_move-1),grid=grid,pieces=pieces,utility=0)
						result=checkWin(state.grid, (row,col))
						if (result>=0):
							pygame.draw.rect(screen, BLACK_COLOR, (265,600, width-265, 30))
							label = myfont.render(f"Ha vinto {COLOURS[result]}",1,WHITE_COLOR )
							screen.blit(label,(265,600))
							end = True
						turn = abs(turn - 1)
						draw_board(state.grid)
						print(state.grid)
		
						
		if(turn==RED and not end):
			move=ai_player(game,state)
			grid=state.grid
			pieces=state.pieces
			piece = Piece(move.shape,state.to_move)
			row = grid.make_move(move.column,piece)
    
			pieces[state.to_move][move.shape]-=1
			state=GameState(to_move=abs(state.to_move-1),grid=grid,pieces=pieces,utility=0)
			result=checkWin(state.grid, (row,move.column))

			if (result>=0):
				pygame.draw.rect(screen, BLACK_COLOR, (265,600, width-265, 30))
				label = myfont.render(f"Ha vinto {COLOURS[result]}",1,WHITE_COLOR )
				screen.blit(label,(265,600))
				end = True
			draw_board(state.grid)
			turn = abs(turn - 1)
			print(state.grid)

	pygame.time.wait(3000)
        
	