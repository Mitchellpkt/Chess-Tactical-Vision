print('**************************')
print('Chess-heat-vision project')
print(' * M.P.K.-T. *')
print('**************************\n')

# CHANGELOG ETC
# v1 = first attempts
# v2 = turned v1 into functions
# v3 = start toying with drawing boards.... BROKEN
# v4 = reboot of v2 ...
#       ... VERSION 4 WORKS!!! Output tallyFEN.png
#       ... v4 [[PRESERVED]]
# v6 = updated v4 to Python 3

# KNOWN BUGS
# a) A spot will not be counted as attacked by pawn unless a piece is on it. 
# b) I think that I import ChessNut and FEN in a werid way.
# c) Everything flipped if black to move
# d) Defenses not counted since not considered a legal move.


import os
import sys

fenpath = "./FenDir"
chessnutpath = "./ChessNut"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(fenpath))
sys.path.append(os.path.abspath(chessnutpath))

from Chessnut import Game
from numpy import transpose
import fen

############################################
############################################
##### IMPORTED FROM FEN ####################
##### VVVVVVVVVVVVVVVVV ####################
############################################

import sys
import StringIO
import tempfile
import os
import pdb

import Image
import ImageDraw
import cairo
import rsvg
import argparse
from images import *

def open_svgstring_as_image(string, width, height):
    try:
        tmpfd, tmppath = tempfile.mkstemp(".svg")
        tmpfile = os.fdopen(tmpfd, 'w')
        tmpfile.write(string)
        tmpfile.close()
        return open_svg_as_image(tmppath, width, height)
    finally:
        os.remove(tmppath)

def open_svg_as_image(fn, width, height):
    for i in range(10):
        try:
            tmpfd, tmppath = tempfile.mkstemp(".png")
            tmpfile = os.fdopen(tmpfd,'w')
            
            file = StringIO.StringIO()
            svgsurface = cairo.SVGSurface (file, width, height)
            svgctx = cairo.Context(svgsurface)
            svg = rsvg.Handle(file=fn)
            svgwidth = svg.get_property('width')
            svgheight = svg.get_property('height')
            svgctx.scale(width/float(svgwidth),height/float(svgheight))
            svg.render_cairo(svgctx)
            
            svgsurface.write_to_png(tmpfile)
            svgsurface.finish()
            tmpfile.close()
            
            tmpfile = open(tmppath, 'r')
            imgsurface = cairo.ImageSurface.create_from_png(tmpfile)
            imgwidth = imgsurface.get_width()
            imgheight = imgsurface.get_height()
            
            data = imgsurface.get_data()
        
            im = Image.frombuffer("RGBA",(imgwidth, imgheight), data ,"raw","RGBA",0,1)
            os.remove(tmppath)
            break
        except MemoryError:
            print('Memory Error. Try again ...')
            continue
    else:
        raise Exception('Problem loading image {0}'.format(fn))
    return im   

def draw_board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
               title1="", title2="", footnote="", scale=1,TallyMatrix=[[0 for x in range(8)] for x in range(8)]):
    red = (255,0,0, 255)
    white_square = (255,255,255,255)
    black_square = (128,128,128,255)
    border_color = (156,156,156,255)
    font_color = (0,0,0,255)

    #custom colors!!! vvv
    mycolors = ((255,0,0, 255),(0,255,0, 255),(0,0,255, 255),(0,0,0, 255))
    mycolors = ((0,0,0),(36,24,130),(0,100,0),(238,173,14),(255,127,0),(238,0,0),(255,28,174),(0,0,0))
    #custom colors!!! ^^^
    
    sqsize = 45
    border_width = 12
    bord_offset = 0
    title_height = 40
    sqoffset = border_width + bord_offset
    footnote_height = 20
    
    imgwidth = bord_offset + border_width * 2 + sqsize * 8
    imgheight = bord_offset + border_width * 2 + sqsize * 8 + title_height + footnote_height
    
    im = Image.new('RGBA', (imgwidth, imgheight))
    draw = ImageDraw.Draw(im)
    
    color = white_square

    # Draw Title

    t1_w,t1_h = draw.textsize(title1)
    t2_w,t2_h = draw.textsize(title2)
    freespace = title_height - (t1_h + t2_h)
    
    t1pos = (bord_offset + ((8*sqsize + 2*border_width)-t1_w)/2,
             bord_offset + freespace/3.0
             )
    draw.text(t1pos, title1, fill=font_color)
    t2pos = (bord_offset + ((8*sqsize + 2*border_width)-t2_w)/2,
             bord_offset + 2*freespace/3.0 + t1_h
             )
    draw.text(t2pos, title2, fill=font_color)
    
    # Draw footnote
    f_w,f_h = draw.textsize(footnote)
    fpos = (bord_offset + ((8*sqsize + 2*border_width)-f_w)/2,
            bord_offset +border_width * 2 + sqsize * 8 + title_height + (footnote_height - f_h)/2)
    draw.text(fpos, footnote, fill=font_color)
    
    # Draw Borders
    
    for i in range(8):
        colchr = chr(ord('8')-i)
        rowchr = chr(ord('a')+i)
        # Left border
        rect = (bord_offset,
                title_height + bord_offset+border_width+i*sqsize,
                bord_offset+border_width,
                title_height + bord_offset+border_width+(i+1)*sqsize
                )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        
        (w,h) = draw.textsize(colchr)
        textpos = (bord_offset + (border_width-w)/2,
                   title_height + bord_offset + (sqsize-h)/2 + border_width + i*sqsize)
        draw.text(textpos, colchr, fill=font_color)
        
        # Right Border
        rect = (8*sqsize + border_width + bord_offset,
                title_height + bord_offset + border_width + i*sqsize,
                8*sqsize + border_width + bord_offset + border_width,
                title_height + bord_offset + border_width + (i+1)*sqsize
                )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        
        (w,h) = draw.textsize(colchr)
        textpos = (8*sqsize + border_width + bord_offset + (border_width-w)/2,
                   title_height + bord_offset + (sqsize-h)/2 + border_width + i*sqsize)
        draw.text(textpos, colchr, fill=font_color)
        
        # Top Border
    
        rect = (bord_offset + border_width+i*sqsize,
                title_height + bord_offset,
                bord_offset + border_width+(i+1)*sqsize,
                title_height + bord_offset+border_width,
                )
        draw.rectangle(rect, fill=border_color, outline=border_color)
    
        (w,h) = draw.textsize(rowchr)
        textpos = (bord_offset + border_width + i*sqsize + (sqsize-w)/2,
                   title_height + bord_offset + (border_width-h)/2)
        draw.text(textpos, rowchr, fill=font_color)
        
        # Bottom Border
        
        rect = (
            bord_offset + border_width + i*sqsize,
            title_height + 8*sqsize + border_width + bord_offset,
            bord_offset + border_width + (i+1)*sqsize,
            title_height + 8*sqsize + border_width + bord_offset + border_width,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
    
        (w,h) = draw.textsize(rowchr)
        textpos = (bord_offset + border_width + i*sqsize + (sqsize-w)/2,
                   title_height + 8*sqsize + border_width + bord_offset + (border_width-h)/2)
        draw.text(textpos, rowchr, fill=font_color)
    
    # Draw the corners
        rect = (
            bord_offset,
            title_height + bord_offset,
            bord_offset + border_width,
            title_height + bord_offset + border_width,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        rect = (
            bord_offset + border_width + 8*sqsize,
            title_height + bord_offset,
            bord_offset + 2 * border_width + 8*sqsize,
            title_height + bord_offset + border_width,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        rect = (
            bord_offset + border_width + 8*sqsize,
            title_height + bord_offset + border_width + 8*sqsize,
            bord_offset + 2 * border_width + 8*sqsize,
            title_height + bord_offset + 2 * border_width + 8*sqsize,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)
        rect = (
            bord_offset,
            title_height + bord_offset + border_width + 8*sqsize,
            bord_offset + border_width,
            title_height + bord_offset + 2 * border_width + 8*sqsize,
            )
        draw.rectangle(rect, fill=border_color, outline=border_color)

    print('- about to draw -')
    print('TallyMatrix : ')
    print(TallyMatrix)
    
    # Draw the squares
    for row in range(8):
        for col in range(8):
            rect = (col*sqsize+sqoffset,
                    title_height + row*sqsize+sqoffset,
                    (col+1)*sqsize+sqoffset,
                    title_height + (row+1)*sqsize+sqoffset)
            draw.rectangle(rect, fill=color, outline=color)

            
            
            if TallyMatrix[7-row][col]>0:#row == 3 and col == 3: # troubleshoot drawing on d5
                NuRect = (col*sqsize+sqoffset+0.6*sqsize,
                    title_height + row*sqsize+sqoffset+0.6*sqsize,
                    (col+1)*sqsize +sqoffset,
                    title_height + (row+1)*sqsize+sqoffset)
                #print TallyMatrix[row][col]
                ThisColor =  mycolors[TallyMatrix[7-row][col]]
                #print ThisColor
                draw.rectangle(NuRect, fill=ThisColor, outline=color)

            
            if color == black_square:
                color = white_square
            else:
                color = black_square
        if color == black_square:
            color = white_square
        else:
            color = black_square
    
    # Draw the pieces
    
    row, col = 8,1
    for c in fen:
        imgpos = (border_width+sqsize*(col-1),
                  title_height + border_width+sqsize*(8-row))
        if c == 'K':
            wking = open_svgstring_as_image(white_king, sqsize, sqsize)
            im.paste(wking, imgpos, wking)
            col += 1
        elif c == 'Q':
            wqueen = open_svgstring_as_image(white_queen, sqsize, sqsize)
            im.paste(wqueen, imgpos, wqueen)
            col += 1
        elif c == 'P':
            wpawn = open_svgstring_as_image(white_pawn, sqsize, sqsize)
            im.paste(wpawn, imgpos, wpawn)
            col += 1
        elif c == 'R':
            wrook = open_svgstring_as_image(white_rook, sqsize, sqsize)
            im.paste(wrook, imgpos, wrook)
            col += 1    
        elif c == 'B':
            wbishop = open_svgstring_as_image(white_bishop, sqsize, sqsize)
            im.paste(wbishop, imgpos, wbishop)
            col += 1
        elif c == 'N':
            wknight = open_svgstring_as_image(white_knight, sqsize, sqsize)
            im.paste(wknight, imgpos, wknight)
            col += 1
            
        elif c == 'k':
            wking = open_svgstring_as_image(black_king, sqsize, sqsize)
            im.paste(wking, imgpos, wking)
            col += 1
        elif c == 'q':
            wqueen = open_svgstring_as_image(black_queen, sqsize, sqsize)
            im.paste(wqueen, imgpos, wqueen)
            col += 1
        elif c == 'p':
            bpawn = open_svgstring_as_image(black_pawn, sqsize, sqsize)
            im.paste(bpawn, imgpos, bpawn)
            col += 1
        elif c == 'r':
            brook = open_svgstring_as_image(black_rook, sqsize, sqsize)
            im.paste(brook, imgpos, brook)
            col += 1
        elif c == 'b':
            bbishop = open_svgstring_as_image(black_bishop, sqsize, sqsize)
            im.paste(bbishop, imgpos, bbishop)
            col += 1
        elif c == 'n':
            bknight = open_svgstring_as_image(black_knight, sqsize, sqsize)
            im.paste(bknight, imgpos, bknight)
            col += 1  
        elif c in '12345678':
            col += int(c)
        elif c == '/':
            col = 1
            row -= 1
    return im.resize((int(scale*imgwidth),int(scale*imgheight)))

############################################
############################################
##### ^^^^^^^^^^^^^^^^^ ####################
##### IMPORTED FROM FEN ####################
############################################

#### vvvv DEFS
def rp(a, b): # from internets
    b = set(b)
    return [aa for aa in a if aa in b]
def printMatrix(testMatrix): # from internets
        print(' ')
        for i in range(len(testMatrix[1])):  # Make it work with non square matrices.
              print(i),
        for i, element in enumerate(testMatrix):
              print(i, ' '.join(element))
#### ^^^^ DEFS

def AttackMatrix(sFEN): # This I made
    print("FEN string is: " + sFEN)
    
    sFENnp = sFEN # setting up for sFEN without pawns
    sFENnp = sFENnp.replace('p','1')
    sFENnp = sFENnp.replace('P','1')

    
    ###############
    # DIAGNOSTIC
    #im = draw_board(fen=sFEN)
    #im.save(os.path.join(os.getcwd(),'diagnostics','withpawns.png'))
    #im = draw_board(fen=sFENnp)
    #im.save(os.path.join(os.getcwd(),'diagnostics','withoutpawns.png'))
    ###############\
    chessgame = Game(sFEN) # this and next ...
    possiblem = chessgame.get_moves() # ... get valid moves with all pieces
    chessgamenp = Game(sFENnp) # this and next ...
    possiblemnp = chessgamenp.get_moves() # ... get valid moves without pawns
    vm = rp(possiblem, possiblemnp) # all moves on board with pawns w/o pawn-fwd moves

    #TallyMatrix[row][column]
    TallyMatrix = [[0 for x in range(8)] for x in range(8)]

    for move in vm:
        vr = move[2]
        vc = move[3]
        vr = ''.join([(str(ord(x)-96) if x.isalpha() else x) for x in list(vr)])
        vr = int(vr)-1
        vc = int(vc)-1
        TallyMatrix[vc][vr] = TallyMatrix[vc][vr] + 1
    print('h1 ...... h8')
    for r in range(len(TallyMatrix)):
        print(TallyMatrix[7-r])
    print('a1 ...... a8')
    return TallyMatrix #need this line, d'oh!

def currentFEN(fen):
    im = draw_board(fen)
    im.save(os.path.join(os.getcwd(),'diagnostics','currentFEN.png'))

def tallyFEN(fen):
    tmat = AttackMatrix(fen)
    print('-*-')
    print(tmat)
    im = draw_board(fen, TallyMatrix=tmat)
    im.save(os.path.join(os.getcwd(),'diagnostics','tallyFEN.png'))



##############
#Stuff begins
#############

testFENa = 'rnb1k2r/pp3p2/4p1p1/2n1b1qp/4P3/3QNP2/P6P/1NB1KB1R w Kkq - 0 16' # game w/ Chris
testFENb = '3k4/8/8/8/8/1P6/7R/K6n w - - 8 8' # troubleshooting
dadFEN = 'r2q1rk1/1p2bppp/2np4/pNp2b2/2PP4/5Nn1/PPQBBPPP/4RRK1 w - - 6 14'
chrisFEN = 'r5r1/pp2kpNp/3b1n2/q1pPp1n1/P3P1b1/3B4/1P1P1K1P/RNB3QR w - - 3 14'
idealFEN = 'b7/2p1r1k1/1B1p1P2/n7/5Q2/2K5/8/3R4 w - - 1 1'
##################
# DIAGNOSTIC
# print 'Printing out testFENa'
# currentFEN(testFENa) # works OK
##################

print('Printing out Tallied testFENa')
tallyFEN(idealFEN)

print("tRiO")
