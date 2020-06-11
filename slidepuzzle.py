import pygame, sys, random

# начальные значения
boardwidth = 5  # столбцы
boardheight = 5  # строки
TILESIZE = 80 # размер плитки
# размер поля
WINDOWWIDTH = 740
WINDOWHEIGHT = 580

FPS = 30
BLANK = None
# цвета
BGCOLOR = (159, 227, 169)
TILECOLOR = (78, 98, 245)
TEXTCOLOR = (255, 255, 255)
BORDERCOLOR = (159, 162, 227)
BASICFONTSIZE = 20
BUTTONCOLOR = (255, 255, 255)
BUTTONTEXTCOLOR = (0, 0, 0)
MESSAGECOLOR = (255, 255, 255)
# Генерация поля 4 на 4
xmargin = int((WINDOWWIDTH - (TILESIZE * boardwidth + (boardwidth - 1))) / 2)
ymargin = int((WINDOWHEIGHT - (TILESIZE * boardheight + (boardheight - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Пятнашки')
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)


def main():
    TITLE, TITLE_R = makeText('Всеми любимые пятнашки', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 500, WINDOWHEIGHT - 500)
    exit_s, exit_r = makeText('Выход', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 400, WINDOWHEIGHT - 260)
    LEVEL_1, LEVEL_11 = makeText('1 уровень', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 420, WINDOWHEIGHT - 450)
    LEVEL_2, LEVEL_22 = makeText('2 уровень', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 420, WINDOWHEIGHT - 410)
    LEVEL_3, LEVEL_33 = makeText('3 уровень', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 420, WINDOWHEIGHT - 370)
    LEVEL_4, LEVEL_44 = makeText('4 уровень', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 420, WINDOWHEIGHT - 330)
    DISPLAYSURF.fill(BGCOLOR)
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (0, 0, 0, 0), 4)
    DISPLAYSURF.blit(exit_s, exit_r)
    DISPLAYSURF.blit(TITLE, TITLE_R)
    DISPLAYSURF.blit(LEVEL_1, LEVEL_11)
    DISPLAYSURF.blit(LEVEL_2, LEVEL_22)
    DISPLAYSURF.blit(LEVEL_3, LEVEL_33)
    DISPLAYSURF.blit(LEVEL_4, LEVEL_44)
    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                if LEVEL_11.collidepoint(mouse_pos):
                    boardwidth = 3
                    boardheight = 3
                    xmargin = int((WINDOWWIDTH - (TILESIZE * boardwidth + (boardwidth - 1))) / 2)
                    ymargin = int((WINDOWHEIGHT - (TILESIZE * boardheight + (boardheight - 1))) / 2)
                    pygame.display.flip()
                    game()
                elif LEVEL_22.collidepoint(mouse_pos):
                    boardwidth = 4
                    boardheight = 4
                    xmargin = int((WINDOWWIDTH - (TILESIZE * boardwidth + (boardwidth - 1))) / 2)
                    ymargin = int((WINDOWHEIGHT - (TILESIZE * boardheight + (boardheight - 1))) / 2)
                    pygame.display.flip()
                    game()
                elif LEVEL_33.collidepoint(mouse_pos):
                    boardwidth = 5
                    boardheight = 5
                    xmargin = int((WINDOWWIDTH - (TILESIZE * boardwidth + (boardwidth - 1))) / 2)
                    ymargin = int((WINDOWHEIGHT - (TILESIZE * boardheight + (boardheight - 1))) / 2)
                    pygame.display.flip()
                    game()
                elif LEVEL_44.collidepoint(mouse_pos):
                    boardwidth = 6
                    boardheight = 6
                    xmargin = int((WINDOWWIDTH - (TILESIZE * boardwidth + (boardwidth - 1))) / 2)
                    ymargin = int((WINDOWHEIGHT - (TILESIZE * boardheight + (boardheight - 1))) / 2)
                    pygame.display.flip()
                    game()
                elif exit_r.collidepoint(mouse_pos):
                    sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def game():
    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard()
    allMoves = [] # список ходов
    reset_surf, reset_rect = makeText('Сброс', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    new_surf, new_rect = makeText('Новая игра', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    solve_surf, solve_rect = makeText('Решение', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
    while True:
        slideTo = None
        msg = 'Нажмите на плитку или клавиши со стрелками'
        if mainBoard == SOLVEDBOARD:
            msg = 'Решено!'
        drawBoard(mainBoard, msg)
        checkForQuit()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # нажал ли пользователь на кнопку выбора
                    if reset_rect.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif new_rect.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif solve_rect.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                else:
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == pygame.KEYUP:
                # нажал ли пользователь клавишу, чтобы сдвинуть плитку
                if event.key in (pygame.K_LEFT, pygame.K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (pygame.K_UP, pygame.K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Нажмите на плитку или клавиши со стрелками', 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(pygame.QUIT):
        terminate()
    for event in pygame.event.get(pygame.KEYUP):
        if event.key == pygame.K_ESCAPE:
            terminate()
        pygame.event.post(event)


def getStartingBoard():
    # возвращает [[1, 4, 7], [2, 5, 8], [3, 6, пусто]]
    counter = 1
    board = []
    for x in range(boardwidth):
        column = []
        for y in range(boardheight):
            column.append(counter)
            counter += boardwidth
        board.append(column)
        counter -= boardwidth * (boardheight - 1) + boardwidth - 1

    board[boardwidth - 1][boardheight - 1] = BLANK
    return board


def getBlankPosition(board):
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]

    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = xmargin + (tileX * TILESIZE) + (tileX - 1)
    top = ymargin + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # создайте объекты Surface и Rect для некоторого текста.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    reset_surf, reset_rect = makeText('Сброс', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    new_surf, new_rect = makeText('Новая игра', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    solve_surf, solve_rect = makeText('Решение', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = boardwidth * TILESIZE
    height = boardheight * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(reset_surf, reset_rect)
    DISPLAYSURF.blit(new_surf, new_rect)
    DISPLAYSURF.blit(solve_surf, solve_rect)


def slideAnimation(board, direction, message, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # пустое пространство над движущейся плиткой
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Генерация нового поля...', animationSpeed=int(TILESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    revAllMoves = allMoves[:]  # копию списка
    revAllMoves.reverse()
    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)

if __name__ == '__main__':
     main()