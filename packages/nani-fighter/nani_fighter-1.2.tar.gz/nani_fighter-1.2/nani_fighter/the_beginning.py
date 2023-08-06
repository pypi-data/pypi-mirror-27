#nani fighter
from __future__ import division
import sys,time,math,pygame,random,os.path
from pygame.locals import*

FPS = 30 # frames per second to update the screen
WINWIDTH = 640 # width of the program's window, in pixels
WINHEIGHT = 480 # height in pixels
pi=math.pi


MAXHIT=5
MAXSHOT=5
MAXeggs=12

GRASSCOLOR = (24, 255, 0)
BLACK=(0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BROWN=(174,94,0,30)
YELLOW=(255,255,0)
DISPLAYSURF=pygame.display.set_mode((WINWIDTH,WINHEIGHT))


MAXHEALTH=3 #Credit
MAXENERGY=10 #Energy of nani
MAX_SHOTS = 2   #most player eggs onscreen

arrow = ( "xX                      ",
          "X.X                     ",
          "X..X                    ",
          "X...X                   ",
          "X....X                  ",
          "X.....X                 ",
          "X......X                ",
          "X.......X               ",
          "X........X              ",
          "X.........X             ",
          "X......XXXXX            ",
          "X...X..X                ",
          "X..XX..X                ",
          "X.X XX..X               ",
          "XX   X..X               ",
          "X     X..X              ",
          "      X..X              ",
          "       X..X             ",
          "       X..X             ",
          "        XX              ",
          "                        ",
          "                        ",
          "                        ",
          "                        ")



shoot = ("            ,           ",
         "            ,           ",
         "         XXXXXX         ",
         "       XX......XX       ",
         "      X..........X      ",
         "     X....XXXX....X     ",
         "    X...XX  , XX...X    ",
         "   X...X    ,   X...X   ",
         "   X..X     ,    X..X   ",
         "  X...X     ,    X...X  ",
         "  X..X      ,     X..X  ",
         "  X..X      ,     X..X  ",
         ",,X..X,,,,,,,,,,,,X..X,,",
         "  X..X      ,     X..X  ",
         "  X...X     ,    X...X  ",
         "   X..X     ,    X..X   ",
         "   X...X    ,   X...X   ",
         "    X...XX  ,  X...X    ",
         "     X....XXXXX...X     ",
         "      X..........X      ",
         "       XX......XX       ",
         "         XXXXXX         ",
         "            ,           ",
         "            ,           ",
        )

#BOOK
book=["WHAT IS THIS LIFE IF, FULL OF CARE",
      "WE HAVE NO TIME TO STAND AND STARE?",
      "NO TIME TO STAND BENEATH THE BOUGHS",
      "AND STARE AS LONG AS SHEEP OR COWS.",
      "NO TIME TO SEE, WHEN WOODS WE PASS,",
      "WHERE SQUIRRELS HIDE THEIR NUTS IN ",
      "GRASS.  NO TIME TO STAND AND STARE!",
      ]

#loading images:


#utility functions
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'res')

image_dict=dict()

def load_image(filename, transparent):
    if filename in image_dict:
        return image_dict[filename]

    file = os.path.join(data_dir, filename)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)

    convertedImg = surface.convert()
    image_dict[filename] = convertedImg
    return convertedImg

class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(data_dir,  file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

def WAIT_FOR_SECONDS(seconds):
    startTime = pygame.time.get_ticks()
    ms = seconds*1000
    while pygame.time.get_ticks() - startTime < ms:
        pygame.event.get() #event capture, update failure unresponsiveness workaroud for mac OSX

pygame.init()
chimes=load_sound('chimes.wav')
backMusic=load_sound('EA FIFA 2012.ogg')

FPSCLOCK = pygame.time.Clock()
pygame.display.set_icon(load_image('gameicon.png',0))
#DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption('Nani Fighter')



homeIMG=load_image('home.png',False)
startIMG=load_image('start.png',False)
contIMG=load_image('continue.png',False)
start=[startIMG,contIMG]
extIMG=load_image('exit.png',False)
aboutIMG=load_image('about.png',False)
instIMG=load_image('instruction.png',False)

def terminate():
    DISPLAYSURF.blit(load_image('exitYesNo.png',True),(140,123))
    pygame.display.update()
    Yrect=pygame.Rect(168,217,100,40)
    Nrect=pygame.Rect(337,217,100,40)

    while True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type==pygame.MOUSEBUTTONDOWN:

                cursorpos=pygame.mouse.get_pos()


                if Yrect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.draw.rect(DISPLAYSURF,WHITE,Yrect,5)
                    chimes.play()
                    pygame.display.update()
                    pygame.quit()
                    exit(0)

                elif Nrect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.draw.rect(DISPLAYSURF,WHITE,Nrect,5)
                    chimes.play()
                    pygame.display.update()
                    return 
        FPSCLOCK.tick(FPS)


def drawHealthMeter(currentHealth):
    x=0
    if currentHealth<=MAXHEALTH//3:
        x=random.randint(0,3)
    for i in range(currentHealth): # draw red health bars
        pygame.draw.rect(DISPLAYSURF, RED,   (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
    for i in range(MAXHEALTH): # draw the white outlines
        pygame.draw.rect(DISPLAYSURF, WHITE, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1+x)
    creditSurf=pygame.font.Font('freesansbold.ttf', 15).render('Credit',False,WHITE)
    creditRect=creditSurf.get_rect()
    creditRect.center=(24,24+(10*MAXHEALTH))
    DISPLAYSURF.blit(creditSurf,creditRect)


def drawNaniMeter(energy):
    color=[RED,YELLOW,GRASSCOLOR,GREEN]
    k=MAXENERGY//3
    p=energy//k
    for i in range(energy): # draw energy bars
        pygame.draw.rect(DISPLAYSURF, color[p], (WINWIDTH-10*(i+2), 5, 10, 10))
    pygame.draw.rect(DISPLAYSURF, WHITE, (WINWIDTH-10*(MAXENERGY+1), 5 , 10*MAXENERGY, 10), 1)
    energySurf=load_image('naniFace.png',1)
    energyRect=energySurf.get_rect()
    energyRect.center=(WINWIDTH-10*(MAXENERGY),43)
    DISPLAYSURF.blit(energySurf,energyRect)

def drawEggCounter(eggs):
    x=0
    if eggs<10:
        x=random.randint(-20,20)
    pygame.draw.ellipse(DISPLAYSURF,(225+x,225+x,50+x),(WINWIDTH-90,WINHEIGHT-120,80,60))
    pygame.draw.ellipse(DISPLAYSURF,(0,225,225),(WINWIDTH-90,WINHEIGHT-120,80,60),3)
    eggSurf=pygame.font.Font('freesansbold.ttf', 15).render('Eggs:'+str(eggs),False,BLACK)
    eggRect=eggSurf.get_rect()
    eggRect.center=(WINWIDTH-50,WINHEIGHT-90)
    DISPLAYSURF.blit(eggSurf,eggRect)


def drawCTboard():
    global CTrect,CTsurf

    pygame.draw.rect(DISPLAYSURF,GREEN, (5,WINHEIGHT-40,70,30))
    CTsurf=pygame.font.Font('freesansbold.ttf', 15).render('GIVE CT',True,RED)
    CTrect=CTsurf.get_rect()
    CTrect.center=(38,WINHEIGHT-22)
    DISPLAYSURF.blit(CTsurf,CTrect)

def drawCTlist(): #this function haven't been used in this game. expected to update in later version
    #creating blinking:
    pygame.draw.rect(DISPLAYSURF,BLUE, (5,WINHEIGHT-40,70,30))
    CTsurf=pygame.font.Font('freesansbold.ttf', 15).render('GIVE CT',True,WHITE)
    CTrect=CTsurf.get_rect()
    CTrect.center=(38,WINHEIGHT-22)
    DISPLAYSURF.blit(CTsurf,CTrect)
    pygame.display.update()
    WAIT_FOR_SECONDS(1)
    #main work:
    pygame.draw.rect(DISPLAYSURF,RED, (5,WINHEIGHT-170,90,120))
    #drawing arrow:
    pygame.draw.polygon(DISPLAYSURF,BLUE,((35,WINHEIGHT-42),(45,WINHEIGHT-42),(40,WINHEIGHT-50)))
    for i in range(4): # draw the white outlines
        pygame.draw.rect(DISPLAYSURF, WHITE, (5, WINHEIGHT-80- i * 30, 90, 30), 1)
    CTlistSurf=[pygame.font.Font('freesansbold.ttf', 15).render('EEE',True,YELLOW),
                pygame.font.Font('freesansbold.ttf', 15).render('MECHA',True,YELLOW),
                pygame.font.Font('freesansbold.ttf', 15).render('MATH',True,YELLOW),
                pygame.font.Font('freesansbold.ttf', 15).render('PHYSICS',True,YELLOW)]
    CTlistRect=[]
    for i in range(4):
        CTlistRect.append(CTlistSurf[i].get_rect())
    for i in range(4):
        CTlistRect[i].topleft=(7,WINHEIGHT-170+i*30+3)
    for i in range(4):
        DISPLAYSURF.blit(CTlistSurf[i],CTlistRect[i])


laugh=load_sound('man_laughing.wav')
def eggparty(eggs):

    DISPLAYSURF.blit(load_image('giveCTwarnLOW.png',True),(80,100))
    pygame.display.update()
    conRect=pygame.Rect(121,249,110,40)
    cancRect=pygame.Rect(341,249,110,40)
    a=True
    while a:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()
            if event.type==pygame.MOUSEBUTTONDOWN:
                cursorpos=pygame.mouse.get_pos()

                if conRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.draw.rect(DISPLAYSURF,WHITE,conRect,5)
                    chimes.play()
                    pygame.display.update()
                    a=False

                if cancRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.draw.rect(DISPLAYSURF,WHITE,cancRect,5)
                    chimes.play()
                    pygame.display.update()
                    return 0

            FPSCLOCK.tick(FPS)
    t=time.time()
    a=True
    x,y=245,63
    k=random.randint(0,20)
    eggSurf3=pygame.font.Font('freesansbold.ttf', 21).render('Now you have '+str(eggs+k-10)+' Eggs',True,BLACK)
    eggRect3=eggSurf3.get_rect()
    eggRect3.topleft=(30,400)

    if k!=0:
        eggSurf=pygame.font.Font('freesansbold.ttf', 21).render('YOU HAVE GOT '+str(k)+' EGGS.',True,BLACK)
        eggSurf2=pygame.font.Font('freesansbold.ttf', 21).render('Have a nice egg party.',True,BLACK)
        eggRect=eggSurf.get_rect()
        eggRect.topleft=(30,50)
        eggRect2=eggSurf2.get_rect()
        eggRect2.topleft=(30,100)

    else:
        eggSurf=pygame.font.Font('freesansbold.ttf', 21).render('BAD LUCK.I FAILED TO GIVE YOU ANY EGG',True,BLACK)
        eggRect=eggSurf.get_rect()
        eggRect.topleft=(30,50)

        DISPLAYSURF.fill(GRASSCOLOR)
        DISPLAYSURF.blit(load_image('blast.png',True),(0,0))
        DISPLAYSURF.blit(eggSurf,eggRect)
        DISPLAYSURF.blit(eggSurf3,eggRect3)
        pygame.display.update()
        explode.play()
        WAIT_FOR_SECONDS(2)
        return -10

    dmod=True
    laugh.play(1)
    while a:
        DISPLAYSURF.fill(GRASSCOLOR)

        DISPLAYSURF.blit(load_image('sirBody.png',False),(0,0))
        DISPLAYSURF.blit(eggSurf,eggRect)
        if k!=0:
            DISPLAYSURF.blit(eggSurf2,eggRect2)
        DISPLAYSURF.blit(eggSurf3,eggRect3)
        head=load_image('sirHead.png',True)

        if dmod:
            y+=1
            if y==70:
                dmod=False
        else:
            y-=1
            if y==56:
              dmod=True

        DISPLAYSURF.blit(head,(x,y))

        if time.time()-t>=4:
            return k-10
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        pygame.event.get() #event capture, update failure unresponsiveness workaroud for mac OSX

def drawPlayButton():
    alpha=120
    
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    flashSurf.fill((220,100,255, alpha))
    DISPLAYSURF.blit(flashSurf,(0,0))
    DISPLAYSURF.blit(psIMG[1],psRect)
    drawBackButton()
    origSurf = DISPLAYSURF.copy()
    pygame.display.update()
    a=True

    while a:
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()

            if event.type==pygame.MOUSEBUTTONDOWN:

                cursorpos=pygame.mouse.get_pos()


                if psRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    chimes.play()
                    a=False

                elif backRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.mixer.music.stop()
                    chimes.play()
                    startMenu(-2)
                    DISPLAYSURF.fill((0,0,0))
                    DISPLAYSURF.blit(origSurf,(0,0))                    
                    pygame.display.update()
        FPSCLOCK.tick(FPS)


backIMG=load_image('backImage.png',0)
def drawBackButton():
    global backRect
    backRect=pygame.Rect(backIMG.get_rect())
    backRect.center=(WINWIDTH//2+250,WINHEIGHT-20)
    DISPLAYSURF.blit(backIMG,backRect)


def drawClassRoom():
    #draw board:
    pygame.draw.rect(DISPLAYSURF, BLACK, (WINWIDTH//4,WINHEIGHT//15,WINWIDTH//2,WINHEIGHT//4))
    pygame.draw.rect(DISPLAYSURF, (255,255,255), (WINWIDTH//4,WINHEIGHT//15,WINWIDTH//2,WINHEIGHT//4),5)
    #draw platform:
    pygame.draw.polygon(DISPLAYSURF, (200,0,50), ((0,WINHEIGHT//2+30),(0,WINHEIGHT//2-50),(3*WINWIDTH//4+40,WINHEIGHT//2-50),
                                                  (3*WINWIDTH//4,WINHEIGHT//2+30)))
    pygame.draw.polygon(DISPLAYSURF, (150,0,50), ((0,WINHEIGHT//2+30),(0,WINHEIGHT//2+50),(3*WINWIDTH//4,WINHEIGHT//2+50),
                                                  (3*WINWIDTH//4,WINHEIGHT//2+30)))
    pygame.draw.polygon(DISPLAYSURF, (100,0,40), ((3*WINWIDTH//4,WINHEIGHT//2+30),(3*WINWIDTH//4+40,WINHEIGHT//2-50),
                                                  (3*WINWIDTH//4+40,WINHEIGHT//2-35),(3*WINWIDTH//4,WINHEIGHT//2+50)))
    #draw door:
    pygame.draw.line(DISPLAYSURF, BROWN, (WINWIDTH-50,WINHEIGHT//2-35),(WINWIDTH-50,WINHEIGHT//10),10)
    pygame.draw.line(DISPLAYSURF, BROWN, (WINWIDTH-54,WINHEIGHT//10),(WINWIDTH,WINHEIGHT//10),10)
    pygame.draw.rect(DISPLAYSURF, BLACK, (WINWIDTH-45,WINHEIGHT//10+5,45,WINHEIGHT//2-WINHEIGHT//10-40))
    #draw bench:
    pygame.draw.polygon(DISPLAYSURF,BROWN ,((WINWIDTH//4,WINHEIGHT),(WINWIDTH//4+15,WINHEIGHT-20),(WINWIDTH//2+180,WINHEIGHT-20),
                                            (WINWIDTH//2+170,WINHEIGHT)))



def drawBoardWork(x,y):
    '''x=words in yth line, y=book line'''
    i=-1
    for i in range(y-1):
        whiteSurf=pygame.font.Font(None, 21).render(book[i],True,YELLOW)
        whiteRect=whiteSurf.get_rect()
        whiteRect.topleft=(WINWIDTH//4+2,WINWIDTH//15+i*15)
        DISPLAYSURF.blit(whiteSurf,whiteRect)

    whiteSurf=pygame.font.Font(None,21).render(book[y-1][:x],True,YELLOW)
    whiteRect=whiteSurf.get_rect()
    whiteRect.topleft=(WINWIDTH//4+2,WINWIDTH//15+(i+1)*15)
    DISPLAYSURF.blit(whiteSurf,whiteRect)





def TestCursor(arrow):
    hotspot = None
    for y in range(len(arrow)):
        for x in range(len(arrow[y])):
            if arrow[y][x] in ['x', ',', 'O']:
                hotspot = x,y
                break
        if hotspot != None:
            break
    if hotspot == None:
        raise Exception("No hotspot specified for cursor '%s'!" %
cursorname)
    s2 = []
    for line in arrow:
        s2.append(line.replace(',', '.'))
    cursor, mask = pygame.cursors.compile(s2, 'X', '.', 'o')
    size = len(arrow[0]), len(arrow)
    pygame.mouse.set_cursor(size, hotspot, cursor, mask)

handposition=(WINWIDTH//4+3,WINHEIGHT//15+3)




explode=load_sound('EXPLODE.wav')
#explode.set_volume(.8)



def main():
    global initialNpos,GRASSIMAGES,eggIMG,player,nani,hand,h0rect,h1rect,psIMG
    global psRect


    #pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None


    #FPSCLOCK = pygame.time.Clock()
    #pygame.display.set_icon(load_image('gameicon.png',0))
    #DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    #pygame.display.set_caption('Teacher Fighter')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    eggs=MAXeggs #initial eggs
    health=MAXHEALTH
    # load the image files
    eggIMG=load_image('egg.png',True)
    eggWid=eggIMG.get_width()
    eggHet=eggIMG.get_height()


    player1IMG=load_image('player1.png',True)
    player2IMG=load_image('player2.png',True)
    player=[player1IMG,player2IMG]

    crashIMG=load_image('crash.png',True)

    naniRIMG=load_image('naniRight.png',True)
    naniLIMG= pygame.transform.flip(naniRIMG, True, False)
    naniFIMG=load_image('naniFront.png',True)
    nani=[naniRIMG,naniLIMG,naniFIMG]

    statePlayer=0 #initial player state
    stateNani=0 #initial nani position
    TestCursor(shoot)

    naniRect=pygame.Rect(nani[stateNani].get_rect()) #used in collide

    handPen=load_image('naniHandMarker.png',True)
    handPalm=load_image('naniHand.png',True)
    hand=[handPen,handPalm]
    h0rect=pygame.Rect(hand[0].get_rect())
    h1rect=pygame.Rect(hand[1].get_rect())


    sdrpos=[100,95] #shoulder position(initial)

    ps1=load_image('pauseImage1.png',0)
    ps2=load_image('pauseImage2.png',0)
    psIMG=[ps2,ps1]
    psRect=pygame.Rect(psIMG[0].get_rect())
    psRect.center=(WINWIDTH//4-30,WINHEIGHT-20)

    #DISPLAYSURF.blit(player1IMG,playerpos)

    #loading sound:
    hit_sound=load_sound('punch.wav')
    hit_sound.set_volume(0.60)

    joySound=load_sound('joy.wav')

    scream=load_sound('womanScream.wav')

    if pygame.mixer:
        music = os.path.join(data_dir, 'house_lo.wav')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.40)


    keys=[False,False,False,False]
    playerpos=[WINWIDTH//2,WINHEIGHT-103]
    initialNpos=[100,40] #initial nani position


    hposx=playerpos[0]+145 #position of hand of player x coordinate
    hposy=playerpos[1]+60 #position of hand of player y coordinate



    #calculating egg path:
    g=9.8 #gravity
    Range=2 #distance of board from bench
    c_angle=pi/6 #cameraAngle
    MaxHeight=4 #bench to ceiling distance
    mpc=hposy/( math.cos(c_angle)*MaxHeight + Range*math.sin(c_angle) )
    # meter to pixel conversion constant
    pmc=1/mpc #pixel to meter conversion constant
    tg=0.05 #time gap of drawing while in motion

    hit=[] # crash position
    glue=[] # crash image rendering time
    dix=[] # displacement in Range axis
    target=[] #stores cursor position
    position=[] #stores x position of player
    e_angle=[] #angle of throwing
    velocity=[] #velocity of egg
    period=[] #time period of projectile
    rotation=[] #rotation of egg
    incrementX=[] #increment in x direction
    incrementDix=[] #increment of dix (negative z axis to our respect)
    Time=[] #elapsed time
    sz=.01 #eggsize decreasing constant,is changed later
    size=[] #recorder of size


    #to draw nani:
    npos=initialNpos #coordinate of naniIMG
    inNposx=100 #initial pos only x co ordinate
    nposy=npos[1]
    line=1 #line on board
    fmot=True #forward motion is true
    pause=False #pause of motion false
    ncoll=False #nani collided

    shortEggs=False #short of eggs
    dirt=False
    energy=MAXENERGY




    while True:
        tt=time.time()
        DISPLAYSURF.fill((200,200,200))
        #drawing environment:

        
        drawClassRoom()
        drawCTboard()
        drawBackButton()

        #drawing player
        DISPLAYSURF.blit(psIMG[0],psRect)
        DISPLAYSURF.blit(player[statePlayer],playerpos)


        #drawing crashed eggs:
        i=0
        count=0

        while i<len(hit) and count<=MAXHIT:
            DISPLAYSURF.blit(crashIMG,hit[i])
            if time.time()-glue[i]>2:
                del hit[i]
                del glue[i]
                i=-1
            count+=1
            i+=1

        #drawing energy and egg display
        drawHealthMeter(health)
        drawNaniMeter(energy)
        drawEggCounter(eggs)

        #drawing Nani:
        npos[1]=nposy+(random.randint(-30,30)//30)
        if pause:
            stateNani=2

            if dirt and ncoll==False:
                stateNani=0
            if fmot:
                drawBoardWork((npos[0]-WINWIDTH//4)//7+8,line)
            else:
                drawBoardWork(len(book[line-1]),line)

            DISPLAYSURF.blit(nani[stateNani],(npos[0]-30*stateNani,npos[1]))
            if tt-note>=2:
                pause=False
                ncoll=False
                if dirt:
                    dirt=False
                    energy-=1
                    if energy==0:
                        pygame.mixer.music.stop()
                        joySound.play()
                        wingame()
                        backMusic.play()
                        about()
                        backMusic.stop()
                        return 


        else:
            flag=0
            if fmot:
                stateNani=0
                npos[0]+=random.randint(0,5)
                drawBoardWork((npos[0]-WINWIDTH//4)//7+9,line)
                pp=WINWIDTH//4+len(book[line-1])*6
                if npos[0]<pp+5:
                    DISPLAYSURF.blit(nani[stateNani],npos)
                    flag=1
                else:
                    npos[0]=pp
                    stateNani=1
                    DISPLAYSURF.blit(nani[stateNani],npos)
                    fmot=False
                    flag=1
                    if line==7:
                        #line=0
                        pygame.mixer.music.stop()
                        drawNhand(sdrpos[0],line,fmot)
                        gameOverAnimation(RED)
                        return 

            if flag==0:
                if stateNani==2:
                    ncoll=True
                npos[0]-=10
                drawBoardWork(len(book[line-1]),line)
                if npos[0]>inNposx:
                    DISPLAYSURF.blit(nani[stateNani],npos)
                else:
                    stateNani=0
                    ncoll=False
                    npos[0]=inNposx
                    DISPLAYSURF.blit(nani[stateNani],npos)
                    fmot=True
                    line+=1


        #draw hand of nani:
        sdrpos[0]=npos[0]
        drawNhand(sdrpos[0],line,fmot,ncoll,dirt)

        #got caught
        if stateNani==2 and statePlayer:
            #ncoll=True
            pygame.mixer.music.stop()
            scream.play()
            explode.play()
            caughtSurf=BASICFONT.render('YOU HAVE BEEN CAUGHT',True,WHITE)
            caughtRect=caughtSurf.get_rect()
            caughtRect.center=(WINWIDTH//2,WINHEIGHT//2)
            DISPLAYSURF.blit(caughtSurf,caughtRect)

            drawHealthMeter(0)
            pygame.display.update()
            WAIT_FOR_SECONDS(2)
            gameOverAnimation(RED)
            return 


        statePlayer=0
        #drawing flying eggs:
        i=0
        count=0
        while i<len(position) and count<=MAXSHOT:
            t=Time[i]
            u=velocity[i]
            k=u*math.sin(e_angle[i])

            posy=(k*t-0.5*g*t*t)*math.cos(c_angle)+dix[i]*math.sin(c_angle)


            posy=round((hposy-posy*mpc))-15
            posx=round(position[i])

            rsize=int(round(size[i]))
  
            segg=pygame.transform.scale(eggIMG,(eggWid-rsize,eggHet-rsize))
            regg=pygame.transform.rotate(segg,rotation[i]) #rotated egg

            DISPLAYSURF.blit(regg,(posx,posy))

            Time[i]+=tg
            dix[i]+=incrementDix[i]
            position[i]+=incrementX[i]
            rotation[i]+=10
            if size[i]!=0:
                size[i]+=sz



            if t>=period[i]-tg:
                pin=(target[i][0]-18,target[i][1]-7)
                DISPLAYSURF.blit(crashIMG,pin)
                hit_sound.play()
                #collide

                if stateNani==2:
                    ncoll=True
                    pygame.mixer.music.stop()
                    scream.play()
                    note=tt
                   
                    pygame.mixer.music.play(-1)

                if stateNani==1:
                    if npos[0]+30>target[i][0]:
                        ncoll=True
                        stateNani=2
                        pause=True

                        scream.play()
                        note=tt
                       

                naniRect.left=npos[0]+10
                naniRect.top=40
                naniRect.height=140
                #naniRect.width+=10

                eggRect=pygame.Rect(crashIMG.get_rect())
                eggRect.center=(pin)

                if naniRect.colliderect(eggRect):
                    ncoll=True
                    pause=True
                    note=tt
                    pygame.mixer.music.stop()
                    scream.play()
                    explode.play()
                    pygame.mixer.music.play(-1)
                    health-=1
                    if playerpos[1]==WINHEIGHT:
                        health+=1
                    if health==0:
                        pygame.mixer.music.stop()
                        #scream.play()
                        explode.play()
                        gameOverAnimation()
                        return 




                hit.append(pin)
                glue.append(time.time())
                del position[i],Time[i],velocity[i],incrementX[i],e_angle[i],rotation[i],target[i],incrementDix[i],period[i],dix[i],size[i]

                i-=1
            count+=1
            i+=1

        #dirty board needs to be clean

        if fmot and pause==False:
            dif=WINHEIGHT//15+line*15
            for i in range(len(hit)):
                if npos[0]<hit[i][0]<npos[0]+80+(3-line)*4:
                    if dif-25<hit[i][1]<dif:
                        pause=True
                        dirt=True
                        note=glue[i]
                        break




        if shortEggs==True and len(position)+len(hit)==0:
            DISPLAYSURF.fill(RED)
            eggSurf=pygame.font.Font('freesansbold.ttf', 25).render('YOU HAVE RUN OUT OF EGGS!',False,WHITE)
            eggRect=eggSurf.get_rect()
            eggRect.center=(WINWIDTH//2,WINHEIGHT//2)
            DISPLAYSURF.blit(eggSurf,eggRect)
            pygame.display.update()
            WAIT_FOR_SECONDS(2)
            explode.play()
            pygame.mixer.music.stop()
            gameOverAnimation()
            return 

        #looping through events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()

            if event.type==pygame.KEYDOWN:
                if event.key==K_RIGHT:
                    keys[0]=True
                elif event.key==K_LEFT:
                    keys[1]=True
                elif event.key==K_DOWN:
                    keys[2]=True
                elif event.key==K_UP:
                    keys[3]=True

            if event.type==pygame.KEYUP:
                if event.key==K_RIGHT:
                    keys[0]=False
                elif event.key==K_LEFT:
                    keys[1]=False
                elif event.key==K_DOWN:
                    keys[2]=False
                elif event.key==K_UP:
                    keys[3]=False



            if event.type==pygame.MOUSEBUTTONDOWN:
                cursorpos=pygame.mouse.get_pos()
                if CTrect.colliderect(cursorpos[0]-10,cursorpos[1],80,30):
                    chimes.play()

                    eggs+=eggparty(eggs)
                    if eggs<=0:
                        shortEggs=True

                elif psRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.mixer.music.stop()
                    chimes.play()
                    drawPlayButton()
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)

                elif backRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.mixer.music.stop()
                    chimes.play()
                    startMenu(-2)
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)

                elif playerpos[1]!=WINHEIGHT and shortEggs==False:
                    statePlayer=1
                    eggs-=1
                    if eggs==0:
                        shortEggs=True



                    #preparing egg variables
                    Time.append(0)

                    h=((hposy-cursorpos[1])*pmc-Range*math.sin(c_angle))/math.cos(c_angle)

                    dix.append(0)
                    target.append(cursorpos)
                    hposx=playerpos[0]+145 #hand position of player

                    position.append(hposx-20)

                    vel=(4*g*abs(h))**0.5 #velocity
                    velocity.append(vel)

                    dek=pi/4+(random.randint(1,5))*pi/60
                    e_angle.append(dek) #throwing angle

                    don=vel*math.sin(dek)
                    mon=don**2-2*g*h
                    T=(don+mon**0.5)/g

                    period.append(round(T,2)) # required time

                    if cursorpos[1]<=WINHEIGHT//2+50:
                        sz=eggWid/(T/tg)/5
                        size.append(sz)
                    else:
                        size.append(0)

                    z=cursorpos[0]-hposx
                    c=z/T*tg
                    incrementX.append(c) #increment along x axis

                    c2=Range/T*tg
                    incrementDix.append(c2) # increment along Range axis

                    rotation.append((random.randint(1,5))*12) #rotation of egg



        if keys[0]:
            if playerpos[0]+5 <= WINWIDTH//2+30:
                playerpos[0]+=5
            else:
                playerpos[0]=WINWIDTH//2+30
        elif keys[1]:
            if playerpos[0]-5 >= WINWIDTH//4:
                playerpos[0]-=5
            else:
                playerpos[0]=WINWIDTH//4
        elif keys[2]:
            playerpos[1]=WINHEIGHT
        elif keys[3]:
            playerpos[1]=WINHEIGHT-103







        pygame.display.update()
        FPSCLOCK.tick(FPS)

l,k=7,34
n,m=11,4

x=69 #h0rect.width
y=69 #h0rect.height

pAngle=math.atan2(k-m,x-n-l) #permanent angle
denom=((m-k)**2+(n+l-x)**2)**0.5

def drawNhand(sdrposx,line,fmot=True,collide=False,dirt=False):
    if collide==True:
        return 

    posx=sdrposx+68-15-30
    posy=95-30-100+72 #sdrpos[1]=95,play

    e=random.randint(1,3)
    if fmot==False:
        d=pygame.transform.flip(hand[1],True,False)
        DISPLAYSURF.blit(pygame.transform.rotate(d,70-e),(posx-50-e,posy+40+e))
        return 

    state=0
    freq=1
    if dirt:
        state=1
        freq=2

    H=(3-line)*15+5
    nAngle=math.asin(H/denom) #needed angle between shoulder and pen position

    angle=nAngle-pAngle
    #Counter(nAngle,100)
    #Counter(pAngle,200)
    a=math.sin(angle)
    b=math.cos(angle)
    new1=[k*a+l*b,(x-l)*a+k*b]
    new2=[(x-n)*b+m*a,m*b+n*a]
    posx=posx+(new1[0]-l)+line*2
    posy=posy-(new1[1]-(3-line)*12)
    angle*=180/pi

    DISPLAYSURF.blit(pygame.transform.rotate(hand[state],angle-e*freq),(posx-2+e,posy+18-e))


def show(eggs,pos): #useful function to check any parameter in the code. not used in the main game
    #pygame.draw.ellipse(DISPLAYSURF,(225,225,50),(WINWIDTH-90,WINHEIGHT-90,80,60))
    #pygame.draw.ellipse(DISPLAYSURF,(0,225,225),(WINWIDTH-90,WINHEIGHT-90,80,60),3)
    eggSurf=pygame.font.Font('freesansbold.ttf', 15).render(str(round(eggs,3)),False,BLACK)
    eggRect=eggSurf.get_rect()
    eggRect.center=(WINWIDTH-100-pos,WINHEIGHT-90)
    DISPLAYSURF.blit(eggSurf,eggRect)
    pygame.display.update()

def gameOverAnimation(color=WHITE, animationSpeed=50):
# play all beeps at once, then flash the background
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    #BEEP1.play() # play all four beeps at the same time, roughly.
    #BEEP2.play()
    #BEEP3.play()
    #BEEP4.play()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step): # animation loop
            # alpha means transparency. 255 is opaque, 0 is invisible
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                #drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                pygame.event.get() #event capture, update failure unresponsiveness workaroud for mac OSX 
    DISPLAYSURF.fill((0,0,0))
    DISPLAYSURF.blit(load_image('gameover.png',False),(0,0))
    pygame.display.update()
    WAIT_FOR_SECONDS(2)


def wingame():
    DISPLAYSURF.blit(load_image('win.png',False),(0,0))
    pygame.display.update()
    WAIT_FOR_SECONDS(2)


def instruction():
    img=load_image('helpTNF.png',False)
    imgRect=pygame.Rect(img.get_rect())
    DISPLAYSURF.blit(img,(0,0))
    drawBackButton()
    pygame.display.update()
    y=0
    keys=[False,False]
    while True:
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(img,(0,y))
        drawBackButton()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()

            if event.type==pygame.KEYDOWN:

                if event.key==K_DOWN:
                    keys[0]=True
                elif event.key==K_UP:
                    keys[1]=True

            if event.type==pygame.KEYUP:

                if event.key==K_DOWN:
                    keys[0]=False
                elif event.key==K_UP:
                    keys[1]=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                cursorpos=pygame.mouse.get_pos()

                if backRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    chimes.play()
                    return 

        if keys[0]:
            if y-10>WINHEIGHT-imgRect.height:
                y-=10
            else:
                y=WINHEIGHT-imgRect.height
        elif keys[1]:
            if y+20<0:
                y+=20
            else:
                y=0

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def about():
    img=load_image('aboutTNF.png',False)
    imgRect=pygame.Rect(img.get_rect())
    DISPLAYSURF.blit(img,(0,0))
    pygame.display.update()
    y=0
    keys=[False,False]
    while True:
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(img,(0,y))
        drawBackButton()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()

            if event.type==pygame.KEYDOWN:

                if event.key==K_DOWN:
                    keys[0]=True
                elif event.key==K_UP:
                    keys[1]=True

            if event.type==pygame.KEYUP:

                if event.key==K_DOWN:
                    keys[0]=False
                elif event.key==K_UP:
                    keys[1]=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                cursorpos=pygame.mouse.get_pos()

                if backRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    chimes.play()
                    return 

        if keys[0]:
            if y-10>WINHEIGHT-imgRect.height:
                y-=10
            else:
                y=WINHEIGHT-imgRect.height
        elif keys[1]:
            if y+20<0:
                y+=20
            else:
                y=0

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def startMenu(state=0):

    p,q=WINWIDTH//2,WINHEIGHT//4-50
    startRect=pygame.Rect(startIMG.get_rect())
    startRect.center=(p,q+50)

    instRect=pygame.Rect(startIMG.get_rect())
    instRect.center=(p,q+150)


    aboutRect=pygame.Rect(startIMG.get_rect())
    aboutRect.center=(p,q+250)

    extRect=pygame.Rect(startIMG.get_rect())
    extRect.center=(p,q+350)

    music = os.path.join(data_dir,  'EA FIFA 2012.ogg')
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)

    TestCursor(arrow)
    
    DISPLAYSURF.blit(homeIMG,(0,0))
    pygame.display.update()
    WAIT_FOR_SECONDS(state+2)
    DISPLAYSURF.blit(start[state//2],startRect)
    DISPLAYSURF.blit(instIMG,instRect)
    DISPLAYSURF.blit(extIMG,extRect)
    DISPLAYSURF.blit(aboutIMG,aboutRect)

    pygame.display.update()
    p,q,r,s=startRect.left,startRect.top,startRect.width,startRect.height

    
    while True:

        DISPLAYSURF.fill((0,0,0))
        DISPLAYSURF.blit(homeIMG,(0,0))
        DISPLAYSURF.blit(start[state//2],startRect)
        DISPLAYSURF.blit(instIMG,instRect)
        DISPLAYSURF.blit(extIMG,extRect)
        DISPLAYSURF.blit(aboutIMG,aboutRect)


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                 terminate()
            if event.type==pygame.MOUSEBUTTONDOWN:
                cursorpos=pygame.mouse.get_pos()

                if startRect.collidepoint(cursorpos):
                    pygame.draw.rect(DISPLAYSURF,WHITE,(p,q,r,s),5)
                    pygame.display.update()
                    pygame.mixer.music.stop()
                    chimes.play()
                    if state==0:
                        main()
                        TestCursor(arrow)
                        pygame.mixer.music.load(music)
                        pygame.mixer.music.play(-1)
                    else:
                        TestCursor(shoot)
                        pygame.mixer.music.stop()
                        return 



                if instRect.collidepoint(cursorpos):
                    chimes.play()
                    pygame.draw.rect(DISPLAYSURF,WHITE,(p,q+100,r,s),5)
                    pygame.display.update()
                    instruction()

                if aboutRect.collidepoint(cursorpos):
                    chimes.play()
                    pygame.draw.rect(DISPLAYSURF,WHITE,(p,q+200,r,s),5)
                    pygame.display.update()

                    about()

                if extRect.collidepoint(cursorpos):
                    chimes.play()
                    pygame.draw.rect(DISPLAYSURF,WHITE,(p,q+300,r,s),5)
                    pygame.display.update()
                    terminate()


        pygame.display.update()
        FPSCLOCK.tick(FPS)


def run():
    startMenu()

if __name__ == '__main__':
    run()