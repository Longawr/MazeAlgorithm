import pygame
from sys import exit
from pygame.locals import *
from Controller import *

# state
start = True
mode = False
# global variable
solution = []
count = 0
score = 0
frame = 30
currentTime = 0
startTime = 0
limitTime = 5000
# constant
BUFFER = 2
current = (-1, -1)
# color
VISITED =    (248, 237, 227)
START =      (154, 220, 255)
CURRENT =    (0, 255, 171)
CHECK =      (162, 178, 159)
UNCHECK =    (121, 135, 119)
BUTTONTEXT = (227, 202, 165)
OBSTACLE =   (199, 75, 80)

pygame.init()
gundam = Gundam()
screen = pygame.display.set_mode((650, 450))
pygame.display.set_caption('Gundam Find Path')
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
# sound
clickSound = pygame.mixer.Sound('resources\\click.wav')
clickSound.set_volume(0.1)
bgMusic = pygame.mixer.Sound('resources\\Music.wav')
bgMusic.set_volume(0.2)
bgMusic.play(loops=-1)
# some button
playButton = myfont.render("Play", True, BUTTONTEXT)
performButton = myfont.render("Perform", True, BUTTONTEXT)
startButton = myfont.render("Start", True, BUTTONTEXT)
inputButton = myfont.render("Open File", True, BUTTONTEXT)
backButton = myfont.render("Back", True, BUTTONTEXT)
outputButton = myfont.render("Output", True, BUTTONTEXT)
# modeButton
modetext = myfont.render("Catch Mode", True, UNCHECK)
modeButonOff = pygame.image.load('resources\\modebuttonoff.png').convert_alpha()
modeButonOff = pygame.transform.rotozoom(modeButonOff,0,0.46)
modeButonOn = pygame.image.load('resources\\modebuttonon.png').convert_alpha()
modeButonOn = pygame.transform.rotozoom(modeButonOn,0,0.46)
modeButtonSur = modeButonOff
# gundam
gundamSurf = pygame.image.load('resources\\gundam2.png').convert_alpha()
gundamSurf = pygame.transform.rotozoom(gundamSurf,0,0.5)

gundamStand = pygame.image.load('resources\\gundam3.png').convert_alpha()
gundamStand = pygame.transform.rotozoom(gundamStand,0,0.75)
gundamFlight = pygame.image.load('resources\\gundam4.png').convert_alpha()
gundamFlight = pygame.transform.rotozoom(gundamFlight,45,0.75)
gundamMode = gundamStand
# app's name
name = myfont.render('GUNDAM FIND PATH', True, (137, 15, 13))

while True:
    # event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # giao dien khoi dong
        if start:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # play button
                if (75 < pos[0] < 75 + 150) and (100 < pos[1] < 100 + 50):
                    clickSound.play()
                    gundam.open()
                    frame = 60
                    start = False
                    play = True
                    gundam.mode = False
                    run = False
                    mess = myfont.render(f'Gundam start at {gundam.begin}', True, UNCHECK)
                # perform button
                if (75 < pos[0] < 75 + 150) and (175 < pos[1] < 175 + 50):
                    clickSound.play() 
                    gundam.open()
                    frame = 5
                    start = False
                    play = False
                    run = False
                    gundam.mode = False
                    mess = myfont.render(f'Gundam start at {gundam.begin}', True, UNCHECK)
                    pygame.time.delay(500)
                # input button
                if (75 < pos[0] < 75 + 150) and (250 < pos[1] < 250 + 50):
                    clickSound.play()
                    gundam.input()
        
        # trình bày thuật toán
        elif not run:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[K_RETURN]):
                pos = pygame.mouse.get_pos()
                keys = pygame.key.get_pressed()
                # start button
                if (115 < pos[0] < 115 + 100) and (HEIGH + 150 < pos[1] < HEIGH + 150 + 35) or keys[K_RETURN]:
                    if gundam.check(gundam.begin):
                        if not play:
                            solution.clear()
                            gundam.refresh()
                            mess = myfont.render('Gundam\'s thinking', True, UNCHECK)
                            screen.blit(mess, (50 + 25, HEIGH + 75))
                            gundam.start()
                            distance = 0
                            count = 0
                        else:
                            solution.clear()
                            gundam.refresh()
                            solution.append(gundam.begin)
                            current = gundam.begin
                            gundam.start()
                            gundam.visited.clear()
                            gundam.visited.append(current)
                            distance = 0
                            distance += gundam.field[current[0]][current[1]]
                            startTime = pygame.time.get_ticks()
                        run = True
                    else:
                        mess = myfont.render('Gundam\'s dead!!', True, UNCHECK)
                    clickSound.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # mode button
                if ((WIDTH + 190 < pos[0] < WIDTH + 275 + 15) and (HEIGH + 20 < pos[1] < HEIGH + 56)) and not play:
                    gundam.mode = not gundam.mode
                    solution.clear()
                    gundam.refresh()
                    clickSound.play()
                # back button
                elif ((WIDTH + 190 < pos[0] < WIDTH + 275 + 15) and (HEIGH + 75 < pos[1] < HEIGH + 110)):
                    start = True
                    clickSound.play()
                    solution.clear()
                    gundam.refresh()
                    pygame.time.delay(500)
                # output button
                elif ((WIDTH + 65 < pos[0] < WIDTH + 150 + 15) and (HEIGH + 75 < pos[1] < HEIGH + 110)):
                    clickSound.play()
                    gundam.output()
        # giao dien nguoi choi
        elif play and run:
            if (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed() == (True, False, False) 
               or event.type == pygame.MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                pos = (pos[1]//50 -1, pos[0]//50 -1)
                if surround(current, pos) and gundam.check(pos):
                    current = pos
                    solution.append(current)
                    gundam.visited.append(current)
                    distance += gundam.field[current[0]][current[1]]
                    clickSound.play()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_UP] and gundam.check((current[0] - 1, current[1])):
                    current = (current[0] - 1, current[1])
                    solution.append(current)
                    gundam.visited.append(current)
                    distance += gundam.field[current[0]][current[1]]
                    clickSound.play()
                if keys[K_DOWN] and gundam.check((current[0] + 1, current[1])):
                    current = (current[0] + 1, current[1])
                    solution.append(current)
                    gundam.visited.append(current)
                    distance += gundam.field[current[0]][current[1]]
                    clickSound.play()
                if keys[K_LEFT] and gundam.check((current[0], current[1] - 1)):
                    current = (current[0], current[1] - 1)
                    solution.append(current)
                    gundam.visited.append(current)
                    distance += gundam.field[current[0]][current[1]]
                    clickSound.play()
                if keys[K_RIGHT] and gundam.check((current[0], current[1] + 1)):
                    current = (current[0], current[1] + 1)
                    solution.append(current)
                    gundam.visited.append(current)
                    distance += gundam.field[current[0]][current[1]]
                    clickSound.play()

    # man hinh khoi dong
    if start:
        screen = pygame.display.set_mode((650, 450))
        screen.fill((189, 210, 182))
        # gundam
        screen.blit(gundamSurf, (200, -75))
        # name
        screen.blit(name, (150, 325))
        # play button
        pygame.draw.rect(screen, (162, 178, 159), (75 + BUFFER, 100 + BUFFER, 150 - 2*BUFFER , 50 - 2*BUFFER), 0, 10)
        pygame.draw.rect(screen, (121, 135, 119), (75, 100, 150, 50), 2, 10)
        screen.blit(playButton, (75 + 55, 100 + 10))
        # perform button
        pygame.draw.rect(screen, (162, 178, 159), (75 + BUFFER, 175 + BUFFER, 150 - 2*BUFFER , 50 - 2*BUFFER), 0, 10)
        pygame.draw.rect(screen, (121, 135, 119), (75, 175, 150, 50), 2, 10)
        screen.blit(performButton, (75 + 35, 175 + 10))
        # browse button
        pygame.draw.rect(screen, (162, 178, 159), (75 + BUFFER, 250 + BUFFER, 150 - 2*BUFFER , 50 - 2*BUFFER), 0, 10)
        pygame.draw.rect(screen, (121, 135, 119), (75, 250, 150, 50), 2, 10)
        screen.blit(inputButton, (75 + 30, 250 + 10))
    # giao dien chinh
    else:
        # resize screen
        WIDTH = 50*len(gundam.field[0])
        HEIGH = 50*len(gundam.field) if ( 50*len(gundam.field))>300 else 300
        screen = pygame.display.set_mode((WIDTH + 350, HEIGH + 200))
        screen.fill((189, 210, 182))
        # gundam
        modeButtonSur = modeButonOn if gundam.mode else modeButonOff
        gundamMode = gundamFlight if gundam.mode else gundamStand
        screen.blit(gundamMode, (WIDTH + 60,75))
        # ke bang
        for i in range(len(gundam.field[0])+1):
            pygame.draw.line(screen, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 50 + 50*len(gundam.field)), 2)
        for j in range(len(gundam.field)+1):
            pygame.draw.line(screen, (0,0,0), (50, 50 + 50*j), (50 + 50*len(gundam.field[0]), 50 + 50*j), 2)
        # to mau
        for i in range(len(gundam.field)):
            for j in range(len(gundam.field[0])):
                if(gundam.field[i][j] == 0):
                    cellColor = OBSTACLE
                    pygame.draw.rect(screen, cellColor, (50 + j*50 + BUFFER, 50 + i*50 + BUFFER, 50 - BUFFER , 50 - BUFFER))
        for i, j in solution:
            if (i,j) == current:
                cellColor = CURRENT
            elif (i,j) == gundam.begin:
                cellColor = START
            else:
                cellColor = VISITED
            if i >= 0:
                pygame.draw.rect(screen, cellColor, (50 + j*50 + BUFFER, 50 + i*50 + BUFFER, 50 - BUFFER , 50 - BUFFER))
        # viet so
        for i in range(len(gundam.field)):
                for j in range(len(gundam.field[i])):
                    numberColor = CHECK if ((i, j) in solution) else UNCHECK
                    value = myfont.render(str(gundam.field[i][j]), True, numberColor)
                    screen.blit(value, ((j+1)*50 + 10, (i+1)*50 + 10))
        # message
        if len(solution) == 0:
            screen.blit(mess, (50 + 25, HEIGH + 75))
        else: printStep(HEIGH, gundam, distance, myfont, UNCHECK, screen, mess, score)
        # start button
        if not run:
            pygame.draw.rect(screen, (121, 135, 119), (115, HEIGH + 150, 100, 35), 2, 10)
            pygame.draw.rect(screen, (162, 178, 159), (115 + BUFFER, HEIGH + 150 + BUFFER, 100 - 2*BUFFER , 35 - 2*BUFFER), 0, 10)
            screen.blit(startButton, (115 + 20, HEIGH + 150))
        # mode button
        if not play:
            screen.blit(modetext, (WIDTH + 65, HEIGH + 25))
            screen.blit(modeButtonSur, (WIDTH + 190, HEIGH + 20))
        # back button
        pygame.draw.rect(screen, (121, 135, 119), (WIDTH + 190, HEIGH + 75, 100, 35), 2, 10)
        pygame.draw.rect(screen, (162, 178, 159), (WIDTH + 190 + BUFFER, HEIGH + 75 + BUFFER, 100 - 2*BUFFER , 35 - 2*BUFFER), 0, 10)
        screen.blit(backButton, (WIDTH + 190 + 25, HEIGH + 75))
        # output button
        pygame.draw.rect(screen, (121, 135, 119), (WIDTH + 65, HEIGH + 75, 100, 35), 2, 10)
        pygame.draw.rect(screen, (162, 178, 159), (WIDTH + 65 + BUFFER, HEIGH + 75 + BUFFER, 100 - 2*BUFFER , 35 - 2*BUFFER), 0, 10)
        screen.blit(outputButton, (WIDTH + 65 + 15, HEIGH + 75))
        
        # tim duong
        if not play and run:
            if count in range(len(gundam.result)):
                current = gundam.result[count]
                solution.append(current)
                count +=1
                distance += gundam.field[current[0]][current[1]]
                clickSound.play()
            else:
                run = False
        elif play and run:
            # time
            gundam.time = (limitTime - (currentTime - startTime))/1000
            score = distance*100/gundam.maxSum
            if gundam.time <= 0:
                gundam.time = 0
                run = False
                gundam.visited.__delitem__(0)
    currentTime = pygame.time.get_ticks()
    pygame.display.update()
    clock.tick(frame)