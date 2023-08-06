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
MAXeggs=20

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
alert=load_sound('secosmic_lo.wav')
fooss=load_sound('fooss.wav')

FPSCLOCK = pygame.time.Clock()
pygame.display.set_icon(load_image('gameicon.png',0))
#DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption('Nani Fighter')

homeIMG=load_image('home.png',False)
startIMG=load_image('start.png',False)
contIMG=load_image('continue.png',False)
extIMG=load_image('exit.png',False)
aboutIMG=load_image('about.png',False)
instIMG=load_image('instruction.png',False)
hiScoreIMG=load_image('highScore.png',False)

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
        if x%10==0:
            show('',60,30+x,'EGGs!')
    pygame.draw.circle(DISPLAYSURF,RED,(60,25),abs(x))
    pygame.draw.ellipse(DISPLAYSURF,(225+x,225+x,30+x),(WINWIDTH-90,WINHEIGHT-100,80,60))
    pygame.draw.ellipse(DISPLAYSURF,(0,225+x,225+x),(WINWIDTH-90,WINHEIGHT-100,80,60),3)
    eggSurf=pygame.font.Font('freesansbold.ttf', 15).render('Eggs:'+str(eggs),False,BLACK)
    eggRect=eggSurf.get_rect()
    eggRect.center=(WINWIDTH-50,WINHEIGHT-70)
    DISPLAYSURF.blit(eggSurf,eggRect)

def drawPoint(point):
    pygame.draw.rect(DISPLAYSURF,(129,125,25),(100,WINHEIGHT//2-30,WINWIDTH-200,60))
    pygame.draw.rect(DISPLAYSURF,WHITE,(100,WINHEIGHT//2-30,WINWIDTH-200,60),5)
    pointSurf=pygame.font.Font('freesansbold.ttf',25).render("You've Got : "+str(point) +' Points',False,GREEN)
    pointRect=pointSurf.get_rect()
    pointRect.center=(WINWIDTH//2,WINHEIGHT//2)
    DISPLAYSURF.blit(pointSurf,pointRect)

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

def newGameWarn():
    DISPLAYSURF.blit(load_image('newGameWarn.png',True),(80,100))
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
                    return 1 #yes

                if cancRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.draw.rect(DISPLAYSURF,WHITE,cancRect,5)
                    chimes.play()
                    pygame.display.update()
                    return 0 #no

        FPSCLOCK.tick(FPS)

    
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
    eggSurf3=pygame.font.Font('freesansbold.ttf', 21).render('Now you have '+str(eggs+k-5)+' Eggs',True,BLACK)
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
        return -5

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
            return k-5
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
    origSurf = DISPLAYSURF.copy()
    pygame.display.update()
    a=True

    while a:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()

            if event.type==pygame.KEYDOWN:

                if event.key==K_SPACE or event.key==K_p:
                    chimes.play()
                    a=False

            elif event.type==pygame.MOUSEBUTTONDOWN:

                cursorpos=pygame.mouse.get_pos()

                if psRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    chimes.play()
                    a=False
               
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
    global initialNpos,eggIMG,player,nani,hand,h0rect,h1rect,psIMG,psRect

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
    cost=0 #how many eggs costed

    player1IMG=load_image('player1.png',True)
    player2IMG=load_image('player2.png',True)
    player=[player1IMG,player2IMG]

    crashIMG=load_image('crash.png',True)

    naniRIMG=load_image('naniRight.png',True)
    naniLIMG= pygame.transform.flip(naniRIMG, True, False)
    naniDrinkIMG=load_image('naniDrink.png',True)
    naniDrinkIMG= pygame.transform.flip(naniDrinkIMG, True, False)
    naniFIMG=load_image('naniFront.png',True)
    nani=[naniRIMG,naniLIMG,naniFIMG,naniDrinkIMG]

    statePlayer=0 #initial player state
    stateNani=0 #initial nani position
    TestCursor(shoot)

    naniRect=pygame.Rect(nani[stateNani].get_rect()) #used in collide

    naniRect.top=40
    naniRect.height=140
    nwidth=naniRect.width

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

    atelStand=load_image('atel.png',True)
    atelHit=load_image('atel2.png',True)
    atelSave=[load_image('booksave1.png',True),
             load_image('booksave2.png',True),
             load_image('booksave3.png',True)]
    atelShoot=[load_image('bookshoot1.png',True),
               load_image('bookshoot2.png',True)]

    smokeIMG=load_image('smoke.png',True)
    atelRect=pygame.Rect(atelStand.get_rect())
    inPos=(WINWIDTH-40,WINHEIGHT-60)#initial position
    atelRect.bottomright=inPos
    atelBodyRect=pygame.Rect(atelRect.left+40,atelRect.top,atelRect.width-56,atelRect.height)

    mx=atelRect.left+78 #mouthposx
    my=atelRect.top+40 #mouthposx
    #mouthRect=(mouthposx,mouthposy,20,4)
    busytime=0.5 #action time gap
    diversion=1 #diversion if blow happens
    

    atel=0
    atelEvent=(0,0)
    cursorpos=(0,0)


    bottleManIMG=[load_image('bottleMan1.png',True),
               load_image('bottleMan21.png',True),
               load_image('bottleMan2.png',True),
               load_image('bottleMan22.png',True),
               load_image('bottleManStand.png',True)]

    bottleIMG=load_image('bottle.png',True)
    botRect=pygame.Rect(bottleIMG.get_rect())
    botRect.center=(112,192)
    smokeIMG2= pygame.transform.flip(smokeIMG, True, False)
    bottleRect=pygame.Rect(bottleManIMG[0].get_rect())
    bottlepos=(-100,123)
    bottleRect.center=bottlepos
    bottlePause=False
    botIMG=False #image of the bottle

    walkRest=1 #time to take rest after every step

    bottleMan=0
    
    #loading sound:
    hit_sound=load_sound('punch.wav')
    hit_sound.set_volume(0.60)
    
    joySound=load_sound('joy.wav')

    scream=load_sound('womanScream.wav')

    if pygame.mixer:
        music = os.path.join(data_dir, 'house_lo.wav')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
        #pygame.mixer.music.set_volume(0.40)


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

    atelPause=False #atel is not in pause
    pauser=0

    shortEggs=False #short of eggs
    dirt=False
    energy=MAXENERGY
    #eggAlert=0
    startTime=time.time()
    invTime=random.randint(5,10) #time from the start when the atel will show up

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
        if atel==0:
            if tt-startTime>=invTime:
                atel=1
        #drawing crashed eggs:
        i=0
        count=0

        while i<len(hit) and count<=MAXHIT:
            DISPLAYSURF.blit(crashIMG,hit[i])
            if tt-glue[i]>2:
                del hit[i]
                del glue[i]
                i=-1
            count+=1
            i+=1

        #drawing atel
        if atel==3:
            if tt>=repeatTime:
                atel=1


        if atel==2:
            if tt-smokeTime<=0.5:
                DISPLAYSURF.blit(atelHit,(atelRect.left-10,atelRect.top-5))
                fooss.play()
            elif tt-smokeTime<=1:
                DISPLAYSURF.blit(smokeIMG,atelRect)
            else:
                atel=3
                repeatTime=tt
                repeatTime+=random.randint(5,10)
        

        if atel==1:

            did=atelEvent[0]
            watch=atelEvent[1]

            if tt-watch>busytime:
                atelPause=False
                pauser=0

            if atelRect.collidepoint(cursorpos):
                if cursorpos[1]<=250:
                    pauser=1
                elif cursorpos[1]<300:
                    pauser=2
                else:
                    pauser=3


            if did==1:
                DISPLAYSURF.blit(atelShoot[1],(atelRect.left-20,atelRect.top+5))
                atelEvent=(2,0)


            elif atelPause==True:
                DISPLAYSURF.blit(atelSave[did-3],(atelRect.left+50,atelRect.top+10))

            elif pauser:
                atelPause=True
                DISPLAYSURF.blit(atelSave[pauser-1],(atelRect.left+50,atelRect.top+10))
                cursorpos=(0,0)
                atelEvent=(pauser+2,tt)


            elif len(dix)!=0 and cursorpos[0]<atelRect.left+20:
                for i in range(len(dix)):
                    if .5<dix[i]<1:
                        incrementX[i]-=diversion
                        q1=target[i][0]
                        q2=target[i][1]
                        target[i]=(q1-20,q2)
                        DISPLAYSURF.blit(atelShoot[0],(atelRect.left+10,atelRect.top-50))
                        atelEvent=(1,tt)
                        break

                    else:
                       DISPLAYSURF.blit(atelStand,(atelRect.left,atelRect.top))
                       pygame.draw.ellipse(DISPLAYSURF,BLACK,(mx,my,15,8))

            elif atelPause==False:
                x=random.randint(10,25)//5
                y=random.randint(5,10)//5
                c=y//2
                DISPLAYSURF.blit(atelStand,(atelRect.left,atelRect.top+c))
                pygame.draw.ellipse(DISPLAYSURF,BLACK,(mx,my+c,15+x,8+y))
                pygame.draw.circle(DISPLAYSURF,BLACK,(mx-3,my-15+c),x-1)
                pygame.draw.circle(DISPLAYSURF,BLACK,(mx-3+22,my-15+c),x-1)




        #drawing bottle
        if botIMG==True:
            DISPLAYSURF.blit(bottleIMG,botRect)

        #drawing bottle Man
        if bottleMan==0:
            if energy<5:
                bottleMan=1
                alert.play()
                bottleEvent=(-1,0)
                bottleRect.center=bottlepos
                bottlePause=False
                step=53 #step of bottleman

        if bottleMan==3:
            if tt-bottleReturn>6:
                bottleMan=0        


        if bottleMan==1:
            cat=bottleEvent[0]
            dog=bottleEvent[1]

            if tt-dog>walkRest+cat//4:
                if cat==4:
                    cat=3
                    bottleMan=2
                    vanishTime=tt
                    fooss.play()
                    bottleRect.center=(bottleRect.center[0]-step*3,123)
                
                elif cat==2:
                    cat=3
                    bottlePause=True
                    botIMG=True
                bottleRect.center=(bottleRect.center[0]+step,123)
                DISPLAYSURF.blit(bottleManIMG[cat+1],bottleRect)
                bottleEvent=(cat+1,tt)

            
            else:
                DISPLAYSURF.blit(bottleManIMG[cat],bottleRect)
                #show(cat,100,50)
                #show(bottleRect.center[0],150,25)
            
        #drawing energy and egg display
        drawHealthMeter(health)
        drawNaniMeter(energy)
        drawEggCounter(eggs)
 

        #drawing Nani:
        npos[1]=nposy+(random.randint(-30,30)//30)
        if pause:
            stateNani=2

            btp=0
            if npos[0]<=inNposx:
                botIMG=1-bottlePause
                btp=bottlePause
                stateNani=2+bottlePause

            if dirt and ncoll==False:
                stateNani=0

            if fmot:
                drawBoardWork((npos[0]-WINWIDTH//4)//7+8+btp,line) #check here
            else:
                drawBoardWork(len(book[line-1]),line)
               

            DISPLAYSURF.blit(nani[stateNani],(npos[0]-30*stateNani+btp*50,npos[1]))
            if tt-note>=2:
                pause=False
                ncoll=False
                if dirt:
                    dirt=False
                    energy-=1
                    if energy==0:
                        pygame.mixer.music.stop()
                        joySound.play()
                        wingame(npos[0],line,health,cost)
                        backMusic.play()
                        about()
                        backMusic.stop()
                        return
                elif stateNani==3:
                    bottlePause=False
                    energy=MAXENERGY


        else:
            #flag=0
            if fmot:
                stateNani=0
                npos[0]+=random.randint(0,4+energy//3)
                drawBoardWork((npos[0]-WINWIDTH//4)//7+9,line)
                pp=WINWIDTH//4+len(book[line-1])*6
                if npos[0]<pp+5:
                    DISPLAYSURF.blit(nani[stateNani],npos)
                    #flag=1
                else:
                    npos[0]=pp
                    stateNani=1
                    DISPLAYSURF.blit(nani[stateNani],npos)
                    fmot=False
                    #flag=1
                    if line==7:
                        #line=0
                        pygame.mixer.music.stop()
                        drawNhand(sdrpos[0],line,fmot)
                        gameOverAnimation(RED)
                        return

            else:#if flag==0: #means forward motion False,backward True
                if stateNani==2:
                    ncoll=True
                npos[0]-=10
                drawBoardWork(len(book[line-1]),line)
                if npos[0]>inNposx:
                    DISPLAYSURF.blit(nani[stateNani],npos) #backward nani drawing
                else: # backward motion should be stoped
                    stateNani=0
                    ncoll=False
                    npos[0]=inNposx
                    fmot=True
                    line+=1
                    if bottlePause:
                        pause=True
                        ncoll=True #don't Draw any extra hands
                        stateNani=3
                        note=tt
                        
                    #DISPLAYSURF.blit(nani[stateNani],npos)

        if bottleMan==2:
            if tt-vanishTime<=0.5:
                DISPLAYSURF.blit(smokeIMG2,bottleRect)
                
            else:
                bottleMan=3
                bottleReturn=tt+random.randint(0,5)                    


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
                hit_sound.play()
                pin=(target[i][0]-18,target[i][1]-7)
                DISPLAYSURF.blit(crashIMG,pin)
                #collide


            
                naniRect.left=npos[0]+10
                naniRect.width=nwidth
                if stateNani==1:
                    naniRect.width=nwidth-30

                elif line>5:
                    naniRect.width=nwidth-25
                
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


                elif stateNani==2:
                    ncoll=True
                    pygame.mixer.music.stop()
                    scream.play()
                    note=tt

                    pygame.mixer.music.play(-1)

                elif stateNani==1:
                    if npos[0]+30>target[i][0]:
                        ncoll=True
                        stateNani=2
                        pause=True

                        scream.play()
                        note=tt



                hit.append(pin)
                glue.append(time.time())

                if bottleMan==1:
                    if bottleRect.collidepoint(pin):
                        glue[-1]=0

                        vanishTime=tt
                        fooss.play()
                        bottleMan=2
                        
                if atel==1:
                    if atelBodyRect.collidepoint(pin):
                        glue[-1]=0
            
                        if atelPause and (pauser+2)!=atelEvent[0]:
                            atel=2
                            smokeTime=tt

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

        #looping through events,event handling loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()

            if event.type==pygame.KEYDOWN:
                
                if event.key==K_SPACE or event.key==K_p:
                    pygame.mixer.music.stop()
                    chimes.play()
                    drawPlayButton()
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)

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
                    else:
                        shortEggs=False

                elif psRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.mixer.music.stop()
                    chimes.play()
                    drawPlayButton()
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)

                elif backRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    pygame.mixer.music.stop()
                    chimes.play()
                    cow=startMenu(1)
                    if cow==1:
                        return 1 #return to calf in startmenu
                    
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)
                    #pygame.mixer.music.set_volume(0.40)

                elif playerpos[1]!=WINHEIGHT and shortEggs==False:
                    statePlayer=1
                    eggs-=1
                    cost+=1
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

                    if atel==1:
                        if atelBodyRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                            period[-1]/=2

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



def show(eggs,pos=0,fontSize=15,string1='',string2='',color=WHITE): #useful function to check any parameter in the code.
    #pygame.draw.ellipse(DISPLAYSURF,(225,225,50),(WINWIDTH-90,WINHEIGHT-90,80,60))
    #pygame.draw.ellipse(DISPLAYSURF,(0,225,225),(WINWIDTH-90,WINHEIGHT-90,80,60),3)
    eggSurf=pygame.font.Font('freesansbold.ttf', fontSize).render(string1+str(eggs)+string2,False,color)
    eggRect=eggSurf.get_rect()
    eggRect.center=(WINWIDTH//2,WINHEIGHT//2+pos)
    DISPLAYSURF.blit(eggSurf,eggRect)
    #pygame.display.update()

def gameOverAnimation(color=WHITE, animationSpeed=50):
# play all beeps at once, then flash the background
    saveScore(0)
    
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()

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
    explode.play()
    DISPLAYSURF.blit(load_image('gameover.png',False),(0,0))
    pygame.display.update()
    WAIT_FOR_SECONDS(2)


def wingame(n,l,health,cost):
    DISPLAYSURF.blit(load_image('win.png',False),(0,0))
    s=500
    point=(s*6-(s*(l-1)+n))+health*100+20000//cost
    saveScore(point)
    pygame.display.update()
    WAIT_FOR_SECONDS(2)
    drawPoint(point)
    pygame.display.update()
    WAIT_FOR_SECONDS(3)


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

def saveScore(point):
    try:
        p=open(os.path.join(data_dir, 'ScoreBook.txt')).read()
    except:
        p=''
    f=open(os.path.join(data_dir, 'ScoreBook.txt'),'w')
    f.write(p+' \n'+time.ctime()+' '+str(point))
    f.close()

def showHighScore():
    alpha=120
    homeIMG=load_image('home.png',False)
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    flashSurf.fill((220,100,255, alpha))

    try:
        p=open(os.path.join(data_dir, 'ScoreBook.txt')).readlines()
    except:
        print('Failed to load scores file')
        p=[]
    Hiscore=0
    date=''
    counter=0
    total=0
    gover=0
    for i in p:
        if len(i)<10:
            continue
        a=i.split(' ')
        if '' in a:
            a.remove('')
        q=int(a[5])
        counter+=1
        total+=q
        if q==0:
            gover+=1
        if q>Hiscore:
            Hiscore=q
            date=i[:24]

    if counter==0:
        avg=0
        scr=0
    else:
        avg=round(total/counter,2)
        scr=round((counter-gover)/counter*100,2)


    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(homeIMG,(0,0))
    drawBackButton()    
    DISPLAYSURF.blit(flashSurf,(0,0))
    drawBackButton()
    show(Hiscore,0,30,'Highest Score : ')
    show(date,50,25,'Achieved on ')
    show(counter,125,20,'Total Played : ')
    show(counter-gover,150,20,'Succeded : ')
    show(scr,175,20,'Success Rate : ','%')
    show(avg,200,20,'Average points gained : ')
    pygame.display.update()
    while True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()

            if event.type==pygame.MOUSEBUTTONDOWN:
                cursorpos=pygame.mouse.get_pos()

                if backRect.collidepoint(cursorpos[0],cursorpos[1]+10):
                    chimes.play()

                    return
            



        FPSCLOCK.tick(FPS//2) 

def startMenu(state=0):

    p,q=WINWIDTH//2,WINHEIGHT//4-50
    startRect=pygame.Rect(startIMG.get_rect())
    startRect.center=(p,q+50)

    instRect=pygame.Rect(startIMG.get_rect())
    instRect.center=(p,q+125)

    aboutRect=pygame.Rect(startIMG.get_rect())
    aboutRect.center=(p,q+200)

    hiScoreRect=pygame.Rect(startIMG.get_rect())
    hiScoreRect.center=(p,q+275)

    extRect=pygame.Rect(startIMG.get_rect())
    extRect.center=(p,q+350)

    contRect=pygame.Rect(startIMG.get_rect())
    contRect.center=(p,q-25)

    music = os.path.join(data_dir, 'EA FIFA 2012.ogg')
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)
    
    TestCursor(arrow)
    delay=1-state
    DISPLAYSURF.blit(homeIMG,(0,0))
    pygame.display.update()
    boom=False

    while True:

        DISPLAYSURF.fill((0,0,0))
        DISPLAYSURF.blit(homeIMG,(0,0))
        DISPLAYSURF.blit(startIMG,startRect)
        DISPLAYSURF.blit(instIMG,instRect)
        DISPLAYSURF.blit(extIMG,extRect)
        DISPLAYSURF.blit(aboutIMG,aboutRect)
        DISPLAYSURF.blit(hiScoreIMG,hiScoreRect)
        if state==1:
           DISPLAYSURF.blit(contIMG,contRect)
        if delay:
            WAIT_FOR_SECONDS(2)
            delay=0

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                 terminate()
            if event.type==pygame.MOUSEBUTTONDOWN or boom:
                cursorpos=pygame.mouse.get_pos()

                if startRect.collidepoint(cursorpos) or boom:
                    boom=False
                    pygame.draw.rect(DISPLAYSURF,WHITE,startRect,5)
                    pygame.display.update()
                    pygame.mixer.music.stop()
                    chimes.play()
                    if state==1:

                        warn=newGameWarn()
                        if warn==1:
                            saveScore(0)
                            return 1 #returning to cow

                        else:
                           break 
                    
                    calf=main()
                    if calf==1:
                        state=0
                        boom=True
                    TestCursor(arrow)
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(1)

                elif contRect.collidepoint(cursorpos):
                    if state==1:
                        pygame.draw.rect(DISPLAYSURF,WHITE,contRect,5)
                        pygame.display.update()
                        pygame.mixer.music.stop()
                        chimes.play()
                    
                        TestCursor(shoot)
                        return



                elif instRect.collidepoint(cursorpos):
                    chimes.play()
                    pygame.draw.rect(DISPLAYSURF,WHITE,instRect,5)
                    pygame.display.update()
                    instruction()

                elif aboutRect.collidepoint(cursorpos):
                    chimes.play()
                    pygame.draw.rect(DISPLAYSURF,WHITE,aboutRect,5)
                    pygame.display.update()

                    about()

                elif extRect.collidepoint(cursorpos):
                    chimes.play()
                    pygame.draw.rect(DISPLAYSURF,WHITE,extRect,5)
                    pygame.display.update()
                    terminate()

                elif hiScoreRect.collidepoint(cursorpos):
                    chimes.play()
                    pygame.draw.rect(DISPLAYSURF,WHITE,hiScoreRect,5)
                    pygame.display.update()
                    showHighScore()


        pygame.display.update()
        FPSCLOCK.tick(FPS)



def run():
    startMenu()


if __name__ == '__main__':
    run()