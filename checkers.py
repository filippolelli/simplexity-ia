import collections.abc
from piece import Piece
from variables import *

def checkRow(mat, row, col):
    lastPiece:Piece = mat.get_square(row,col).get_piece()
    player=lastPiece.get_color()

    start = max(0, col-PIECESTOWIN+1)
    end = min(COLS-1, col+PIECESTOWIN-1)

    win=count(mat,row,range(start, end+1),player)
    if (win>=0):
        return win        
    return -1

def checkColumn(mat, row, col):
    lastPiece:Piece = mat.get_square(row,col).get_piece()
    player=lastPiece.get_color()

    start = max(0, row-PIECESTOWIN+1)
    end = min(ROWS-1, row+PIECESTOWIN-1)

    win=count(mat,range(start,end+1),col,player)
    if (win>=0):
        return win        
    return -1

def checkDiagonals(mat, row, col):
    shift=PIECESTOWIN-1
    lastPiece:Piece = mat.get_square(row,col).get_piece()
    player=lastPiece.get_color()
    
    ###calcolo dei 4 punti estremi delle due diagonali
    a, b, c, d = (row-shift,col-shift), (row-shift,col+shift), (row+shift,col-shift), (row+shift,col+shift) 

    ###calcolo della distanza dei punti dal bordo: (0 se sono già dentro)
    da,db,dc,dd=max(0,-a[0] if -a[0]>-a[1] else -a[1]),\
        max(0,-b[0] if -b[0]>(b[1]-COLS+1) else b[1]-COLS+1 ),\
            max(0,c[0]-ROWS+1 if (c[0]-ROWS+1)>-c[1] else -c[1]),\
                max(0,d[0]-ROWS+1 if (d[0]-ROWS+1)>(d[1]-COLS+1) else d[1]-COLS+1) 
    
    ###i punti fuori vengono portati dentro, queli già dentro non vengono modificati perchè hanno distanza 0
    a, b, c, d = (a[0]+da, a[1]+da),(b[0]+db, b[1]-db),(c[0]-dc, c[1]+dc),(d[0]-dd, d[1]-dd) 
    
    diagonals=[]
    if length(b,c) >= 4:
        diagonals.append([b, c])
    if length(a,d) >= 4:
        diagonals.append([a, d])
    
    for d in diagonals:
        start=d[0]
        end=d[1]
        stepColumn=1
        if(start[1]>end[1]):
            stepColumn=-1
        win=count(mat,range(start[0],end[0]+1),range(start[1],end[1]+stepColumn,stepColumn),player)
        if (win>=0):
            return win
    return -1

def checkWin(mat, lastIndex):  # -1 continua, 0 pareggio, 1 vittoria
    result = checkRow(mat, lastIndex[0], lastIndex[1]) 
    if(result>=0):
        return result
    result=checkColumn(mat, lastIndex[0], lastIndex[1])
    if(result>=0):
        return result
    result=checkDiagonals(mat, lastIndex[0], lastIndex[1])    
    return result

def inside(point):
    
    if(point[0]<0 or point[0]>ROWS-1 or point[1]<0 or point[1]>COLS-1):
        return False
    return True

def length(p1,p2):
    return abs(p1[1]-p2[1])+1

def count(mat,rangeRow,rangeCol,player):
    if (not  isinstance(rangeRow,collections.abc.Iterable)):
        rangeRow=[rangeRow]*len(rangeCol)
    elif(not isinstance(rangeCol,collections.abc.Iterable)):
        rangeCol=[rangeCol]*len(rangeRow)

    countColor=0
    countShape=[0,0]
    for r,c in zip(rangeRow,rangeCol):  
        
        if(mat.get_square(r,c).is_empty()): ###se c'è un buco si può skippare
            countColor=0
            countShape=[0,0]
            continue
        if (mat.get_square(r,c).get_piece().get_color()==player):
            countColor+=1
        else:
            countColor=0
        countShape[mat.get_square(r,c).get_piece().get_shape()]+=1  
        countShape[abs(mat.get_square(r,c).get_piece().get_shape()-1)]=0  
        
        if(countShape[ROUND]==PIECESTOWIN):
            return WHITE
        if(countShape[SQUARE]==PIECESTOWIN):
            return RED
        if (countColor == PIECESTOWIN):
            return player
    return -1

"""def modifiableCount(mat,rangeRow,rangeCol,player,piecesToCheck):
    if (not  isinstance(rangeRow,collections.abc.Iterable)):
        rangeRow=[rangeRow]*len(rangeCol)
    elif(not isinstance(rangeCol,collections.abc.Iterable)):
        rangeCol=[rangeCol]*len(rangeRow)

    countColor=0
    countShape=[0,0]
    for r,c in zip(rangeRow,rangeCol):  
        
        if(mat.get_square(r,c).is_empty()): ###se c'è un buco si può skippare
            countColor=0
            countShape=[0,0]
            continue
        if (mat.get_square(r,c).get_piece().get_color()==player):
            countColor+=1
        else:
            countColor=0
        countShape[mat.get_square(r,c).get_piece().get_shape()]+=1  
        countShape[abs(mat.get_square(r,c).get_piece().get_shape()-1)]=0  
        
        if(countShape[ROUND]==piecesToCheck):
            return WHITE
        if(countShape[SQUARE]==piecesToCheck):
            return RED
        if (countColor == piecesToCheck):
            return player
    return -1

def checkRow_NEW():
    lastPiece:Piece = mat.get_square(row,col).get_piece()
    player=lastPiece.get_color()

    start = max(0, col-PIECESTOWIN+1)
    end = min(COLS-1, col+PIECESTOWIN-1)

    win=count(mat,row,range(start, end+1),player)
    if (win>=0):
        return win        
    return -1"""