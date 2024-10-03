import math
import sys
import time

import pygame.gfxdraw
from human_player import Move
from simplexity import GameState, Simplexity
from ai_player import ai_player
from variables import *
import pygame
from grid import Grid
from grid import Piece
from check import check_win

# Inizializzazione di Pygame
pygame.init()


# Definizione dei colori
WHITE_COLOR = (245, 245, 245)
RED_COLOR = (255, 25, 25)
BLUE_COLOR = (74, 171, 176)
BLACK_COLOR = (0, 0, 0)
GREY_COLOR = (100, 100, 100)
GREYER_COLOR = (33, 33, 33)
GREEN_COLOR=(0,220,0)
START = 0
GAME = 1
END = 2
RAPP=0.7
LAMP=1000
# Impostazione della finestra di gioco
#IN CASO VISIBILITA' PARZIALE MODIFICARE LA SCREEN WIDTH
screen_width = 800
SQUARESIZE = screen_width//COLS+1
screen_height = SQUARESIZE*(ROWS+2)


RADIUS = SQUARESIZE*RAPP//2

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simplexity")


# Caricamento del font personalizzato per il titolo, sottotitoli e bottoni
title_font = pygame.font.Font(pygame.font.match_font(
    'Georgia', bold=True), 100)  # Font moderno per il titolo
font = pygame.font.Font(pygame.font.match_font(
    'Georgia', bold=False), 30)  # Font per il sottotitolo

rules_font = pygame.font.Font(pygame.font.match_font(
    'Georgia', bold=False), 25)  # Font per le regole
pieces_font = pygame.font.Font(pygame.font.match_font(
    'Georgia', bold=False), 20)  # Font per le regole
names_font=pygame.font.Font(pygame.font.match_font(
    'Georgia', bold=False), 15)  # Font per le regole
# Funzione per disegnare il testo al centro dello schermo
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Funzione per creare un bottone


def draw_button(text, font, rect, color, text_color, surface):
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, GREY_COLOR, rect, 3)  # Bordo grigio attorno al bottone
    draw_text(text, font, text_color, surface, rect.centerx, rect.centery)

# Funzione per mostrare le regole del gioco con gestione dell'andare a capo


def show_rules():
    screen.fill(GREYER_COLOR)

    rules = (
        "1. Ogni giocatore ha disposizione 11 quadrati e 10 cerchi. Il giocatore rosso dispone di pezzi rossi, il giocatore bianco di pezzi bianchi.",
        "2. La partita si svolge su una griglia 6x7, lo scopo del gioco è impilare 4 pezzi verticalmente, orizzontalmente o diagonalmente.",
        "3. La prima mossa viene sempre effettuata dal giocatore bianco.",
        "4. Il giocatore Rosso vince con 4 quadrati o 4 pezzi rossi. Il giocatore Bianco vince con 4 cerchi o 4 pezzi bianchi.",
        "5. La forma dei pezzi ha la precedenza sul colore. Impilando 4 quadrati bianchi vince il rosso, impilando 4 cerchi rossi vince il bianco.",
    )

    # Funzione per spezzare il testo in righe che non superano la larghezza dello schermo
    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Prova ad aggiungere la parola alla riga corrente
            test_line = current_line + word + " "
            # Se la larghezza della linea di prova è inferiore alla larghezza massima, aggiornala
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                # Altrimenti, aggiungi la riga corrente alla lista e inizia una nuova riga
                lines.append(current_line.strip())
                current_line = word + " "

        # Aggiunge l'ultima riga
        if current_line:
            lines.append(current_line.strip())

        return lines

    max_width = screen_width - 40  # Imposta un margine di 20 pixel su entrambi i lati
    y_offset = 80

    for rule in rules:
        wRAPPed_lines = wrap_text(rule, rules_font, max_width)
        for line in wRAPPed_lines:
            draw_text(line, rules_font, WHITE, screen,
                      screen_width // 2, y_offset)
            y_offset += 40  # Spazio tra le righe
        y_offset += 20

    draw_text("Premi un tasto per tornare indietro", rules_font,
              GREY_COLOR, screen, screen_width // 2, screen_height - 50)

    pygame.display.flip()

    # Attende che l'utente prema un tasto per tornare al menu principale
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def draw_initial_menu():
    while True:
        screen.fill(GREYER_COLOR)
        # Disegna il titolo del gioco
        draw_text('Simplexity', title_font, BLUE_COLOR, screen,
                  screen_width // 2, screen_height // 6)
        
        draw_text('Scegli con quale colore giocare', font, WHITE,
                  screen, screen_width // 2, screen_height // 2 - 50)
        draw_text('Sviluppato da Alessandro Cingolani e Filippo Lelli', names_font, GREY_COLOR,
                  screen,170, screen_height - 15)

        # Dimensioni dei bottoni
        button_width = 200
        button_height = 100
        button_spacing = 50  # Distanza tra i bottoni

        # Posizionamento centrato dei bottoni
        total_button_width = (button_width * 2) + button_spacing
        start_x = (screen_width - total_button_width) // 2

        red_button_rect = pygame.Rect(
            start_x, screen_height // 2, button_width, button_height)
        white_button_rect = pygame.Rect(
            start_x + button_width + button_spacing, screen_height // 2, button_width, button_height)

        # Bottone "Regole" in basso a destra
        rules_button_rect = pygame.Rect(
            screen_width - 150, screen_height - 50, 120, 40)

        # Disegna i bottoni per "Rosso", "Bianco" e "Regole"
        draw_button('', rules_font, red_button_rect, RED_COLOR, WHITE_COLOR, screen)
        draw_button('', rules_font, white_button_rect, WHITE_COLOR, BLACK_COLOR, screen)
        draw_button('Regole', rules_font,
                    rules_button_rect, GREYER_COLOR, WHITE_COLOR, screen)
        
        # Gestione degli eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Controlla se il giocatore ha cliccato su "Rosso"
                if red_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Hai scelto il Rosso!")
                    return RED

                # Controlla se il giocatore ha cliccato su "Bianco"
                if white_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Hai scelto il Bianco!")
                    return WHITE

                # Controlla se il giocatore ha cliccato su "Regole"
                if rules_button_rect.collidepoint(mouse_x, mouse_y):
                    show_rules()
        pygame.display.flip()

def draw_board(board: Grid,winnersPos=[],alt=-1):
    
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE_COLOR, (c*SQUARESIZE,
                         r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.rect(screen, GREYER_COLOR, (c*SQUARESIZE+(SQUARESIZE/2)*(1-RAPP),
                         r*SQUARESIZE+SQUARESIZE+(SQUARESIZE/2)*(1-RAPP), SQUARESIZE*RAPP, SQUARESIZE*RAPP))

  


    for c in range(COLS):
        for r in range(ROWS):
            square = board.get_cell(r, c)
            if square is None:
                continue
            piece: Piece = square

            if piece.get_shape() == ROUND:
                if (piece.get_color() == WHITE):
                    if  ([r,c] not in winnersPos):
                        draw_aacircle(screen,WHITE_COLOR,c*SQUARESIZE+SQUARESIZE*0.5,r*SQUARESIZE+SQUARESIZE*1.5,RADIUS,)
                    else:
                        draw_aacircle(screen,GREEN_COLOR if alt<(LAMP/2) else WHITE_COLOR,c*SQUARESIZE+SQUARESIZE*0.5,r*SQUARESIZE+SQUARESIZE*1.5,RADIUS,)

                else:
                    if  ([r,c] not in winnersPos):
                        draw_aacircle(screen,RED_COLOR,c*SQUARESIZE+SQUARESIZE*0.5,r*SQUARESIZE+SQUARESIZE*1.5,RADIUS,)
                    else:
                        draw_aacircle(screen,GREEN_COLOR if alt<(LAMP/2) else RED_COLOR,c*SQUARESIZE+SQUARESIZE*0.5,r*SQUARESIZE+SQUARESIZE*1.5,RADIUS,)
            else:
                if (piece.get_color() == WHITE):
                    if  [r,c] not in winnersPos:
                        pygame.draw.rect(screen, WHITE_COLOR, (c*SQUARESIZE+(SQUARESIZE/2)*(1-RAPP),
                         r*SQUARESIZE+SQUARESIZE+(SQUARESIZE/2)*(1-RAPP), SQUARESIZE*RAPP, SQUARESIZE*RAPP))
                    else:
                        pygame.draw.rect(screen, GREEN_COLOR if alt<(LAMP/2) else WHITE_COLOR, (c*SQUARESIZE+(SQUARESIZE/2)*(1-RAPP),
                         r*SQUARESIZE+SQUARESIZE+(SQUARESIZE/2)*(1-RAPP), SQUARESIZE*RAPP, SQUARESIZE*RAPP))
                else:
                    if  [r,c] not in winnersPos:
                        pygame.draw.rect(screen, RED_COLOR, (c*SQUARESIZE+(SQUARESIZE/2)*(1-RAPP),
                         r*SQUARESIZE+SQUARESIZE+(SQUARESIZE/2)*(1-RAPP), SQUARESIZE*RAPP, SQUARESIZE*RAPP))
                    else:
                        pygame.draw.rect(screen, GREEN_COLOR if alt<(LAMP/2) else RED_COLOR, (c*SQUARESIZE+(SQUARESIZE/2)*(1-RAPP),
                         r*SQUARESIZE+SQUARESIZE+(SQUARESIZE/2)*(1-RAPP), SQUARESIZE*RAPP, SQUARESIZE*RAPP))
                
    pygame.display.update()


def draw_game(chosen_color):
    game = Simplexity()
    current_shape = SQUARE if chosen_color == RED else ROUND
    ia_color=RED if chosen_color==WHITE else WHITE
    change_button_rect = pygame.Rect(0, screen_height-SQUARESIZE, screen_width/4, SQUARESIZE)
    restart_button_rect = pygame.Rect(screen_width-screen_width/4, screen_height-SQUARESIZE, screen_width/4, SQUARESIZE/2)

    exit_button_rect = pygame.Rect(screen_width-screen_width/4, screen_height-SQUARESIZE/2, screen_width/4, SQUARESIZE/2)

    state = game.initial
    pieces = state.pieces
    result=[-1,[]]
    screen.fill(GREYER_COLOR)
    draw_button('Cambia pezzo', rules_font,
                change_button_rect, GREYER_COLOR, WHITE_COLOR, screen)
    draw_button('Ricomincia', rules_font,
                restart_button_rect, GREYER_COLOR, WHITE_COLOR, screen)
    draw_button('Esci', rules_font,
                exit_button_rect, GREYER_COLOR, WHITE_COLOR, screen)
    draw_board(state.grid)
    drawPieces(state,ia_color,chosen_color)
    pygame.display.update()
    end=False
    while not end:
        if state.to_move==chosen_color:
            shape=drawUpperBarPlayer(screen,current_shape,chosen_color)
            pygame.display.update()
            for event in pygame.event.get():                
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if change_button_rect.collidepoint(pygame.mouse.get_pos()):
                        nextShape=swapShape(current_shape)
                        if pieces[state.to_move][nextShape]==0:
                            msg="quadrati" if current_shape==SQUARE else "cerchi"
                            showMessage(f"Ti rimangono solo i {msg}!",0.5)
                            continue
                        current_shape = swapShape(current_shape)
                    elif restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                        return
                    elif exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                        sys.exit()
                    else:
                        posx = shape.centerx
                        col = math.floor(posx/SQUARESIZE)
                        piece = Piece(state.to_move, current_shape)
                        row = state.grid.make_move(col,piece)
                        if(row < 0):
                            showMessage(f"Colonna piena!",0.5)
                            continue
                        state.pieces[state.to_move][current_shape]-=1
                        if state.pieces[state.to_move][current_shape]==0:
                            current_shape=SQUARE if current_shape==ROUND else ROUND
                            draw_button('Cambia pezzo', rules_font,
                            change_button_rect, GREYER_COLOR, GREY_COLOR, screen)

                        state=GameState(to_move=RED if state.to_move==WHITE else WHITE,grid=state.grid,pieces=pieces,utility=0)

                        result = check_win(state.grid, (row,col))                
        else:          
            showMessage("L'IA sta pensando...",0)

            move = ai_player(game,state)
            row = state.grid.make_move(move.column,Piece(state.to_move, move.shape))
            state.pieces[state.to_move][move.shape]-=1
            state=GameState(to_move=RED if state.to_move==WHITE else WHITE,grid=state.grid,pieces=pieces,utility=0)
            result=check_win(state.grid, (row,move.column))


        drawPieces(state,ia_color,chosen_color)
        
        if (result[0]!=-1):
            end=True
            if result[0]==chosen_color:
                showMessage("Hai vinto!",0)
            else:
                showMessage("Hai perso!",0)
        draw_board(state.grid,result[1])

    alt=0
    while True:
        alt=alt+1 if alt<LAMP else 0
        draw_board(state.grid,result[1], alt)      
        for event in pygame.event.get():                
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return
                elif exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()    

def showMessage(txt,t):
    pygame.draw.rect(screen, GREYER_COLOR, (0,0, screen_width, SQUARESIZE))
    draw_text(txt,rules_font,WHITE, screen, screen_width/2, 50)
    pygame.display.update()

    time.sleep(t)

def swapShape(current_shape):
    return SQUARE if current_shape==ROUND else ROUND
            
def drawUpperBarPlayer(screen,current_shape,chosen_color):
    posx=pygame.mouse.get_pos()[0]
    pygame.draw.rect(screen, GREYER_COLOR, (0,0, screen_width, SQUARESIZE))
    
    if(current_shape == ROUND):
        shape=draw_aacircle(screen, RED_COLOR if chosen_color==RED else WHITE_COLOR, min(posx+RADIUS,screen_width-RADIUS), math.floor(5*SQUARESIZE/3-SQUARESIZE)-2, RADIUS)
    else:
        shape=pygame.draw.rect(screen, chosen_color, (min(posx,screen_width-SQUARESIZE*RAPP), math.ceil(SQUARESIZE-SQUARESIZE*RAPP), SQUARESIZE*RAPP, SQUARESIZE*RAPP))
    return shape

def drawPieces(state,ia_color,chosen_color):
    pygame.draw.rect(screen, GREYER_COLOR, (screen_width/4,screen_height-SQUARESIZE, screen_width-screen_width/2, screen_height-SQUARESIZE))

    str="rossi" if ia_color==RED else "bianchi"
    draw_text(f"(IA) Pezzi {str}: {state.pieces[ia_color][SQUARE]} ■, {state.pieces[ia_color][ROUND]} ●",
                pieces_font, WHITE, screen, screen_width/2, screen_height-35)
    str="bianchi" if str=="rossi" else "rossi"
    draw_text(f"(TU) Pezzi {str}: {state.pieces[chosen_color][SQUARE]} ■, {state.pieces[chosen_color][ROUND]} ●",
                pieces_font, WHITE, screen, screen_width/2, screen_height-80)




def draw_aacircle(screen,color,x,y,radius):
    pygame.gfxdraw.aacircle(screen,
    int(x), int(y), math.floor(radius),color)

    pygame.gfxdraw.filled_circle(screen,
    int(x), int(y), math.floor(radius),color)
    
    return pygame.Rect(x-radius,y-radius,radius*2,radius*2)
           


def gui():
    
    while True:
        chosen_color = draw_initial_menu()
        winner = draw_game(chosen_color)
        print(winner)
        # Aggiorna lo schermo
# Esegui la GUI
gui()
