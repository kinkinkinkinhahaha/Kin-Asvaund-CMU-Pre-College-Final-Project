from cmu_graphics import *
import random

class BridgeCell():
    def __init__(self):
        self.correct = False
        self.visible = True
        
class Player3():
    def __init__(self, app):
        self.x = app.width / 2
        self.y = app.height - 50
        self.bridge = [[BridgeCell() for i in range(2)] for j in range(10)] # I got this logic from ChatGPT (I asked how to create classes for every cell in a grid)
        self.cellwidth = 80
        self.cellheight = 55
        self.showIndex = 0 
        self.showTimer = 0  
        self.roundNumber = 1

        self.currentRow = -1   
        self.currentCol = 0   
        self.playerX = app.width / 2  
        self.playerY = app.height - 120  
        self.showIndex = 0
        self.showTimer = 0        
        self.showDelay = 30   
        self.revealing = False
        self.glowOn = False  
        self.teleportDelay = 0  
        self.gameOver = False
        self.falling = False

        self.playerWidth = 50
        self.playerHeight = 60
        self.greenScreen = False


        self.updatePlayerPosition(app)

    
    def drawMap(self, app):
        drawImage(app.rockbackground, 0, 0, 
                  width = app.width, height = app.height)
        drawRect(0, 0, app.width, app.height, 
                 fill = 'black', opacity = 50)
        drawImage(app.middleground, app.width / 2, 
                  app.height - 100, width = 600, height = 600, align = 'top')
        drawImage(app.middleground, app.width / 2, 100, 
                  width = 600, height = 600, align = 'bottom')
        drawImage(app.wall, app.width / 2, app.height / 2, 
                  width = 600, height = 20, align = 'center', rotateAngle = 90)
        drawImage(app.wall, app.width / 2 - 100, app.height / 2, 
                  width = 600, height = 20, align = 'center', rotateAngle = 90)
        drawImage(app.wall, app.width / 2 + 100, app.height / 2, 
                  width = 600, height = 20, align = 'center', rotateAngle = 90)
    
    def startReveal(self):
        self.revealing = True
        self.currentGlowRow = 0
        self.glowTimer = 0
        self.glowOn = True

    def drawBridge(self, app):
        gap = 20
        row_gap = 5
        leftx = app.width / 2 - (self.cellwidth / 2 + gap / 2)
        rightx = app.width / 2 + (self.cellwidth / 2 + gap / 2)
        starty = app.height - 125

        for j in range(len(self.bridge)):        
            for i in range(len(self.bridge[0])):
                x = leftx if i == 0 else rightx
                y = starty - j * (self.cellheight + row_gap)

                if self.bridge[j][i].visible:
                    drawImage(app.bridge, x, y, width=self.cellwidth, height=self.cellheight, align='center')

                if (self.glowOn and j == self.currentGlowRow and
                    self.bridge[j][i].correct and self.bridge[j][i].visible):
                    drawRect(x, y, self.cellwidth, self.cellheight, fill='white', opacity=50, align='center')


    
    def randomizeCorrect(self, app):
        for j in range(len(self.bridge)):
            for i in range(len(self.bridge[0])):
                self.bridge[j][i].correct = False
            safe = random.choice([0, 1])
            self.bridge[j][safe].correct = True
    
    def completeRound(self):
        if self.roundNumber < 5:      
            self.roundNumber += 1
            self.startReveal()       
        else:
            app.game3success = True
    
    def updatePlayerPosition(self, app):
        gap = 20
        rowgap = 5
        leftx = app.width / 2 - (self.cellwidth / 2 + gap / 2)
        rightx = app.width / 2 + (self.cellwidth / 2 + gap / 2)
        starty = app.height - 125

        if self.currentRow == -1:
            self.playerX = app.width / 2
            self.playerY = app.height - 125 
        else:
            self.playerX = leftx if self.currentCol == 0 else rightx
            self.playerY = starty - self.currentRow * (self.cellheight + rowgap)


    def drawPlayer(self, app):
        drawImage(app.game3character, self.playerX, self.playerY, width = self.playerWidth, height = self.playerHeight , align = 'center') 
    
    def checkMove(self, app, col):
        if self.revealing or self.falling:
            return

        self.currentCol = col

        if self.currentRow == -1:
            self.currentRow = 0
            self.updatePlayerPosition(app)
            if not self.bridge[self.currentRow][self.currentCol].correct:
                self.bridge[self.currentRow][self.currentCol].visible = False
                self.falling = True
            return

        if self.currentRow >= self.roundNumber * 2 - 1:
            self.roundNumber += 1
            self.teleportDelay = 15
            return

        self.currentRow += 1
        self.updatePlayerPosition(app)

        if self.bridge[self.currentRow][self.currentCol].correct:
            if self.currentRow >= len(self.bridge) - 1:
                app.game3success = True
                app.game3pass = True
                return
        else:
            self.bridge[self.currentRow][self.currentCol].visible = False
            self.falling = True



    def updateGlow(self, app):

        if not self.falling and not self.revealing and self.teleportDelay == 0:
            if self.currentRow == self.roundNumber * 2 - 1:
                self.roundNumber += 1
                self.teleportDelay = 15
                self.greenScreen = True

        if self.falling:
            self.playerWidth *= 0.9
            self.playerHeight *= 0.9

            if self.playerWidth < 15:
                app.gameOver = True
                self.falling = False
                self.gameOver = True
            return

        if self.teleportDelay > 0:
            self.teleportDelay -= 1
            if self.teleportDelay == 0:
                self.currentRow = -1
                self.updatePlayerPosition(app)
                self.startReveal()
                self.greenScreen = False
            return

        if not self.revealing:
            return

        self.glowTimer += 1

        if self.glowOn and self.glowTimer >= 15:
            self.glowOn = False
            self.glowTimer = 0

        elif not self.glowOn and self.glowTimer >= 15:
            self.currentGlowRow += 1
            self.glowTimer = 0

            if self.currentGlowRow >= min(self.roundNumber * 2, len(self.bridge)):
                self.revealing = False
            else:
                self.glowOn = True
        


class MazeCell(): #Got this logic from ChatGPT
    def __init__(self):
        self.visited = False
        self.walls = {'top': True, 
                      'right': True, 
                      'bottom': True, 
                      'left': True}
        
class Player2():
    def __init__(self, app):
        self.cellSize = 40
        self.rows = 20
        self.cols = 20
        self.maze = [[MazeCell() for i in range(self.cols)] for j in range(self.rows)] 
        self.gameOver2 = False


    def drawGrid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cellSize
                y = row * self.cellSize
                cell = self.maze[row][col]
                
                if cell.walls['top']:
                    drawImage('middleground.png', x, y, width=self.cellSize, height=4)
                if cell.walls['right']:
                    drawImage('middleground.png', x + self.cellSize - 4, y, width=4, height=self.cellSize)
                if cell.walls['bottom']:
                    drawImage('middleground.png', x, y + self.cellSize - 4, width=self.cellSize, height=4)
                if cell.walls['left']:
                    drawImage('middleground.png', x, y, width=4, height=self.cellSize)


    
    def generateMaze(self, row, col):
        cell = self.maze[row][col]
        cell.visited = True

        directions = ['top', 'right', 'bottom', 'left']
        random.shuffle(directions) #Got random.shuffle from w3 schools

        for direction in directions:
            dr, dc = 0, 0
            if direction == 'top':
                dr = -1
            elif direction == 'bottom':
                dr = 1
            elif direction == 'left':
                dc = -1
            elif direction == 'right':
                dc = 1

            newRow = row + dr
            newCol = col + dc

            if 0 <= newRow < self.rows and 0 <= newCol < self.cols:
                next = self.maze[newRow][newCol]
                if not next.visited:
                    cell.walls[direction] = False
                    opposite = {'top': 'bottom', 'bottom': 'top', 'left': 'right', 'right': 'left'}
                    next.walls[opposite[direction]] = False

                    self.generateMaze(newRow, newCol)


class Player1():
    def __init__(self, x ,y, app):
        self.x = x
        self.y = y
        self.playercount = 0
        self.start = False
        self.images = ['rightdown.png', 'rightup.png']
        self.platformgroup = []
        self.platformTimer = 0 
        self.vy = 0
        self.gravity = 1
        self.jumpPower = -16
        self.onGround = False
        self.startPlatform = {
            'x': app.width / 2,
            'y': 600,
            'width': 1700,
            'height': 800
        }
        self.gameOver1 = False

    
    def drawbackground(self, app):
        color = rgb(68, 30, 10)
        drawImage('cavebackground2.png', 0, 0, width = app.width * 2, 
                  height = app.height)
        drawRect(0, 0, app.width, app.height, fill = color, opacity = 50)
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    
    def drawplayer(self, app):
        if self.start:
            if app.count % 5 == 0:
                self.playercount += 1

        drawImage('starterplatform.png', 
          self.startPlatform['x'], self.startPlatform['y'], 
          width=self.startPlatform['width'], height=self.startPlatform['height'], 
          align='top')
        
        
        drawImage(self.images[self.playercount % 2], self.x, self.y, 
                  width = 75, height = 125, align = 'center')


    def drawPlatforms(self, app):
        for platform in self.platformgroup:
            drawImage('middleground.png', platform['x'], platform['y'],
                    width=platform['width'], height=platform['height'], align='top')
            drawImage('middleground.png', platform['x'], platform['y'] - 325,
                    width=platform['width'], height=platform['height'], align='bottom')

    def updatePlatforms(self, app):
        if self.start:
            self.platformTimer += 1
            self.startPlatform['x'] -= 20

            if self.platformTimer % 15 == 0:
                newX = app.width + 300  
                newY = random.randint(500, 600)
                self.platformgroup.append({
                    'x': newX,
                    'y': newY,
                    'width': 300,
                    'height': 800
                })

            newPlatforms = []
            for platform in self.platformgroup:
                platform['x'] -= 20
                if platform['x'] + platform['width'] / 2 > -100:  
                    newPlatforms.append(platform)
            self.platformgroup = newPlatforms
               
             

    def resolveSideCollision(self, platform):
        platformLeft = platform['x'] - platform['width'] / 2
        platformTop = platform['y']
        platformBottom = platformTop + platform['height']

        playerBottom = self.y + 60
        playerTop = self.y - 60
        playerLeft = self.x - 37
        playerRight = self.x + 37

        if playerBottom > platformTop and playerTop < platformBottom:
            if playerRight > platformLeft > playerLeft:
                self.x = platformLeft - 37


    def updatejump(self, app):
        self.vy += self.gravity
        self.y += self.vy
        self.onGround = False
        allPlatforms = self.platformgroup + [self.startPlatform]

        for platform in allPlatforms:
            platformLeft = platform['x'] - platform['width'] / 2
            platformRight = platform['x'] + platform['width'] / 2
            platformTop = platform['y']
            platformBottom = platformTop + platform['height']

            playerBottom = self.y + 60
            playerTop = self.y - 60
            playerLeft = self.x - 37
            playerRight = self.x + 37

            if (self.vy >= 0 and
                playerBottom >= platformTop and 
                playerBottom <= platformTop + abs(self.vy) + 1 and
                playerRight > platformLeft and playerLeft < platformRight):
                self.y = platformTop - 60
                self.vy = 0
                self.onGround = True

            self.resolveSideCollision(platform)

        if self.onGround and abs(self.vy) < 0.5:
            centerX = app.width / 2
            if abs(self.x - centerX) > 1:
                if self.x < centerX:
                    self.x += 0.5

        if self.x < -50 or self.x > app.width + 50 or self.y > app.height:
            self.gameOver1 = True

    def jump(self):
        if self.onGround:
            self.vy = self.jumpPower
            self.onGround = False

    def isOnPlatform(self, platform): # I asked ChatGPT for the logic
        playerBottom = self.y + 60  
        platformTop = platform['y']
        return ( abs(self.x - platform['x']) < platform['width'] / 2 and
            abs(playerBottom - platformTop) < 15 )

def onAppStart(app):
    app.count = 0
    app.width = 800
    app.height = 800
    
    app.backgroundx = app.width / 2
    app.backgroundy = app.height / 2
    app.speed = 10
    
    app.urlbackgroundmain = 'tiles.png' #I got every image from opengameart.org. 
    app.urlwood = 'planks.png' #I found them around a week ago so I don't have the specific links for each of them
    app.urlwoodtw = 'plankstw.png'
    app.bush = 'bush.png'
    app.cobble = 'cobble.png'
    app.wall = 'woodwalls.png'
    app.middleground = 'middleground.png'
    app.greenportal = 'greenportal.png'
    app.redportal = 'redportal.png'
    app.blueportal = 'blueportal.png'
    app.yellowportal = 'yellowportal.png'
    app.metalportal = 'metalportal.png'
    app.castle = 'castle.png'
    app.vignette = 'vignette.png'
    app.startingbackground = 'startingbackground.png'
    app.key = 'keyIcons.png'
    app.crown = 'crown.png'
    app.opacity = 0
    app.rockbackground = 'rock_background.png'

    app.rotatedirections = ['left', 'bottom', 'right', 'top']
    
    app.charactermoveright = ['rightdown.png', 'rightup.png']
    app.charactermoveleft = ['leftdown.png', 'leftup.png']
    app.charactermovefront = ['frontup.png', 'frontdown.png']
    app.charactermoveback = ['backup.png', 'backdown.png']
    app.wizard = ['wizard1.png', 'wizard2.png', 'wizard3.png']
    app.characterdirection = app.charactermovefront
    app.charactercount = 0
    app.wizardcount = 0
    app.wizardy = -100
    app.wizardTargetY = app.height / 2 - 100
    app.wizardSpeed = 4
    app.wizardWalkingIn = True  
    app.speechStart = False
    app.speechDone = False
    app.speechcount = 0
    app.speech = ['Welcome to my dungeon. ',
                  'I hear from the messenger you are seeking for the crown...',
                  'Well... it is not as easy you think it is...',
                  'The existence of this crown you are looking for is a myth...',
                  'However... I do know where you can start your journey.',
                  'To get the crown, you must first retrieve three different keys...',
                  'They are hidden away in three different worlds...',
                  'Each key unlocks the next world...',
                  'The possesion of all three keys will then unlock the final world.',
                  'Each world presents its own challenges, so be careful...',
                  'Good luck.'
                  ]

    app.characterx = app.width / 2
    app.charactery = app.height / 2

    app.backgroundmovingleft = False
    app.backgroundmovingright = False
    app.backgroundmovingup = False
    app.backgroundmovingdown = False
    app.opacityfull = False
    
    app.mainpage = False
    app.starting = True
    app.startingcount = 0

    app.showWelcomeOverlay = False

    app.game1 = False
    app.game1pass = False
    app.player = Player1(app.width / 2, 540, app)
    app.game1On = False
    app.gameOver1 = False
    app.game1counter = 0
    app.game1success = False
    app.keycounter = 0
    app.fadeOpacity1 = 0
    app.fadingOut1 = False

    app.game2 = False
    app.game2pass = False
    app.player2 = Player2(app)
    app.player2.generateMaze(0, 0)
    app.playerRow = 0
    app.playerCol = 0
    app.fadeOpacity2 = 0
    app.fadingOut2 = False
    app.game2characterchoices = ['frontdown.png','backdown.png','rightdown.png', 'leftdown.png']
    app.game2character = 'frontdown.png'
    app.game2On = False
    app.game2speechStart = True  #
    app.game2speechDone = False
    app.game2success = False
    app.gameOver2 = False
    app.game2speechcount = 0
    app.game2speeches = [ 
        'The maze ahead was built by ancient mages...',
        'Only those with a sharp mind and brave heart can find the exit.',
        'Beware of the paths that lead nowhere...',
        'Use WASD or ARROW KEYS to move.',
        'Press any key to begin your journey.'
    ]
    app.mazecompletion = 1500
    app.waitingAfterGame2 = False
    
    app.mazecompletioncolors = ['green', 'yellow', 'red']


    app.game3 = False
    app.game3pass = False
    app.bridge = 'bridgeplatform.png'
    app.game3On = False
    app.game3success = False
 
    app.player3 = Player3(app)
    app.fadeOpacity3 = 0
    app.fadingOut3 = False

    app.game3character = 'backdown.png'
    app.game3speechStart = True  
    app.game3speechDone = False
    app.game3speechcount = 0
    app.game3speeches = [ 
        'No one has ever made it this far...',
        'This last test will reveal your true brain power',
        'Use the left and right arrow keys or A and D keys to play',
        'Press any key to begin your final quest.'
    ]

    app.ending = False
    app.endingy = 0
    app.fadingOut4 = False
    app.fadeOpacity4 = 0
    app.endingcount = 0
    app.drawCrown = False
    app.waitingAfterGame1 = False

def redrawAll(app):
    if app.starting:
        drawStarting(app)

    elif app.mainpage:
        drawMainPage(app)
        if app.showWelcomeOverlay:
            drawWelcomePage(app)
        elif app.mainpage:
            drawMainPage(app)
            drawImage('statusframe.png',20,20, width = 300, height = 50)
            if app.game1pass:
                drawImage(app.key, 50, 28, width = 40, height = 30)
            if app.game2pass:
                drawImage(app.key, 150, 28, width = 40, height = 30)
            if app.game3pass:
                drawImage(app.key, 250, 28, width = 40, height = 30)
            if app.showWelcomeOverlay:
                drawWelcomePage(app)
            if app.fadingOut1:
                drawRect(0, 0, app.width, app.height, fill='black', opacity=app.fadeOpacity1)
            if app.fadingOut2:
                drawRect(0, 0, app.width, app.height, fill='black', opacity=app.fadeOpacity2)
            if app.fadingOut3:
                drawRect(0, 0, app.width, app.height, fill='black', opacity=app.fadeOpacity3)


    elif app.game1:
        drawgame1(app)
        if app.player.gameOver1:
            drawRect(0, 0, app.width, app.height, fill = 'red', opacity = 40)
            drawLabel('[Press any KEY to go back to the mainpage]', app.width / 2, app.height / 2, size = 30, bold = True, fill = 'white', font = 'monospace')
        if app.game1success:
            drawRect(0, 0, app.width, app.height, fill = 'gold', opacity = 40)
            drawLabel('SUCCESS', app.width / 2, app.height / 2 - 300, size = 80, bold = True, fill = 'white', font = 'monospace')
            drawKey(app)
    
    elif app.game2:
        drawgame2(app)
        if app.player2.gameOver2:
            drawRect(0, 0, app.width, app.height, fill = 'red', opacity = 40)
            drawLabel('[Press any KEY to go back to the mainpage]', app.width / 2, app.height / 2, size = 30, bold = True, fill = 'white', font = 'monospace')
        if app.game2success:
            drawRect(0, 0, app.width, app.height, fill = 'gold', opacity = 40)
            drawLabel('SUCCESS', app.width / 2, app.height / 2 - 300, size = 80, bold = True, fill = 'white', font = 'monospace')
            drawKey(app)
    
    elif app.game3:
        drawgame3(app)
        if app.player3.greenScreen:
            drawRect(0, 0, app.width, app.height, fill = 'green', opacity = 40)

        if app.player3.gameOver:
            drawRect(0, 0, app.width, app.height, fill = 'red', opacity = 40)
            drawLabel('[Press any KEY to go back to the mainpage]', app.width / 2, app.height / 2, size = 30, bold = True, fill = 'white', font = 'monospace')
        if app.game3success:
            drawRect(0, 0, app.width, app.height, fill = 'gold', opacity = 40)
            drawLabel('SUCCESS', app.width / 2, app.height / 2 - 300, size = 80, bold = True, fill = 'white', font = 'monospace')
            drawKey(app)

    elif app.ending:
        drawEnding(app)
        if app.drawCrown:
            drawImage(app.crown, app.width/2, app.height/2 - 70, width = 120, height = 120, align = 'center')
            drawLabel('YOU WON!', app.width/2, app.height/2 + 100, size = 50, font = 'monospace', fill = 'white', bold = True)
        

            

def drawWelcomePage(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=70)
    drawLabel("WELCOME TO THE KING'S QUEST", app.width / 2, app.height / 2 - 50, 
                fill='white', size=40, font='monospace', bold=True)
    
    drawLabel("Each portal will send you to different worlds.", app.width / 2, app.height / 2 - 10, 
                fill='white', size=20, font='monospace', bold=True)

    drawLabel('Enter the first portal to start your journey.', app.width / 2, app.height / 2 + 10, 
                fill='white', size=20, font='monospace', bold=True)

    drawLabel('*** To move, use the WASD or the Arrow keys ***', app.width / 2, app.height / 2 + 120, 
                fill='white', size=20, font='monospace')  

    drawLabel('Press any KEY to START', app.width / 2, app.height / 2 + 70, 
                fill='white', size=40, font='monospace')

    drawImage(app.castle, app.width / 2, app.height / 2 - 200, width=200, height=200, align='center')

def drawMainPage(app):
    drawImage(app.urlbackgroundmain, app.backgroundx, app.backgroundy, width=1600, 
                height=1600, align='center')
    
    for i in range(4):
        drawImage(app.urlwood, app.backgroundx, app.backgroundy, width=800, 
                    height=180, align=app.rotatedirections[i], rotateAngle=90 * i)
        drawImage(app.cobble, app.backgroundx, app.backgroundy, width=800, 
                    height=100, align=app.rotatedirections[i], rotateAngle=90 * i)

    drawImage(app.wall, app.backgroundx, app.backgroundy + 90, width=800, height=20, align='left')
    drawImage(app.wall, app.backgroundx, app.backgroundy + 90, width=800, height=20, align='right')
    drawImage(app.wall, app.backgroundx, app.backgroundy - 90, width=800, height=20, align='left')
    drawImage(app.wall, app.backgroundx, app.backgroundy - 90, width=800, height=20, align='right')
    drawImage(app.wall, app.backgroundx + 90, app.backgroundy, width=800, height=20, align='top', rotateAngle=90)
    drawImage(app.wall, app.backgroundx + 90, app.backgroundy, width=800, height=20, align='bottom', rotateAngle=90)
    drawImage(app.wall, app.backgroundx - 90, app.backgroundy, width=800, height=20, align='top', rotateAngle=90)
    drawImage(app.wall, app.backgroundx - 90, app.backgroundy, width=800, height=20, align='bottom', rotateAngle=90)

    drawImage(app.middleground, app.backgroundx, app.backgroundy + 5, width=180, height=180, align='center')
    drawImage(app.middleground, app.backgroundx + 300, app.backgroundy, width=500, height=300, align='left')
    
    drawImage(app.middleground, app.backgroundx - 300, app.backgroundy, width=500, height=300, align='right')
    drawImage(app.middleground, app.backgroundx, app.backgroundy - 300, width=500, height=800, align='bottom')
    drawImage(app.middleground, app.backgroundx, app.backgroundy + 300, width=500, height=800, align='top')

    drawImage(app.greenportal, app.backgroundx + 300, app.backgroundy, width=50, height=250, align='center')

    if app.game1pass:
        drawImage(app.blueportal, app.backgroundx - 300, app.backgroundy, width=50, height=250, align='center', rotateAngle=180)
    
    if app.game2pass:
        drawImage(app.yellowportal, app.backgroundx, app.backgroundy - 300, width=80, height=300, align='center', rotateAngle=-90)
    
    if app.game3pass:
        drawImage(app.redportal, app.backgroundx, app.backgroundy + 300, width=80, height=300, align='center', rotateAngle=90)

    drawImage(app.characterdirection[app.charactercount % 2], app.characterx, 
            app.charactery, width=75, height=125, align='bottom')
    drawImage(app.vignette, app.width/2, app.height/2, width=app.width, height=app.height, align='center')

def drawStarting(app):
    
    color = rgb(68, 30, 10)
    drawImage(app.startingbackground, 0, 0, width = app.width, height = app.height)
    drawRect(0, 0, app.width, app.height, fill = color, opacity = 50)

    drawOval(app.width / 2, app.height / 2, 600, 500, fill = 'red' , opacity = 10)
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 60)
    drawImage(app.wizard[app.wizardcount % 3], app.width / 2 , app.wizardy, width = 150, height = 250, align = 'center')
    drawImage(app.charactermoveback[app.wizardcount % 2], app.width / 2 , app.height / 2 + 100, width = 75, height = 125, align = 'center')

    if app.speechStart:
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 50)
        drawRect(app.width / 2 , app.height / 2 - 200, app.width, 200, fill = 'black', opacity = 50, align = 'center' )
        drawLabel(app.speech[app.speechcount], app.width / 2, app.height / 2 - 225, font = 'monospace', size = 18, fill = 'white', bold = True)
        drawLabel('[click SPACE to continue]', app.width / 2, app.height / 2 - 150, font = 'monospace', size = 20, fill = 'white')
    
    if app.speechDone:
        drawLabel('[click any KEY to continue]', app.width / 2, app.height / 2 + 300, font = 'monospace', size = 40, fill = 'white', bold = True)
   
    drawImage(app.vignette, app.width/2, app.height/2, width=app.width, height=app.height, align='center', opacity = 100)

def restartMain(app):
    app.mainpage = True
    app.characterx = app.width / 2
    app.charactery = app.height / 2
    app.backgroundx = app.width / 2
    app.backgroundy = app.height / 2

    app.backgroundmovingleft = False
    app.backgroundmovingright = False
    app.backgroundmovingup = False
    app.backgroundmovingdown = False
    app.opacityfull = False

def drawKey(app):
    drawImage(app.key, app.width/2, app.height/2 + 100, width = 200, height = 400, opacity = app.keycounter/160 * 100, align = 'center')

def drawCompletion(app):
    margin = 20
    barX = app.width - 300 - margin
    barY = margin

    barWidth = 300
    barHeight = 50

    progress = min(app.game1counter / 1500, 1)
    fillWidth = int(barWidth * progress)

    if fillWidth > 0:
        drawRect(barX, barY, fillWidth, barHeight, fill='green')
    drawRect(barX, barY, barWidth, barHeight, fill=None, border='black', borderWidth=10)

def drawMazeCompletion(app):
    margin = 20
    barX = app.width - 300 - margin
    barY = margin

    barWidth = 300
    barHeight = 50

    progress = min(app.mazecompletion / 1500, 1)
    fillWidth = int(barWidth * progress)

    i = 0
    if progress <= 0.50:
        i = 1
    if progress <= 0.25:
        i = 2

    if fillWidth > 0:
        drawRect(barX, barY, fillWidth, barHeight, fill=app.mazecompletioncolors[i], opacity = 50)
    drawRect(barX, barY, barWidth, barHeight, fill=None, border='black', borderWidth=5, opacity = 75)

def restartGame1(app):
    app.game1 = False
    app.player = Player1(app.width / 2, 540, app)
    app.game1On = False
    app.gameOver1 = False   
    app.game1success = False
    app.game1counter = 0
    app.keycounter = 0

def restartGame2(app):
    app.game2 = False
    app.player2 = Player2(app)
    app.player2.generateMaze(0, 0) 
    app.playerRow = 0  
    app.playerCol = 0  
    app.game2On = False
    app.gameOver2 = False
    app.game2success = False
    app.mazecompletion = 1500
    app.keycounter = 0
    app.game2speechStart = True
    app.game2speechDone = False
    app.game2speechcount = 0

def restartGame3(app):
    app.player3 = Player3(app) 
    app.player3.randomizeCorrect(app)
    
    app.game3speechStart = True
    app.game3speechDone = False
    app.game3speechcount = 0
    
    app.game3On = False
    app.game3success = False
    app.player3.gameOver = False
    
    app.wizardWalkingIn = True
    app.wizardy = -100



def drawgame1(app):
    app.player.drawbackground(app)
    app.player.drawPlatforms(app)
    app.player.updatejump(app)
    app.player.drawplayer(app)
    drawCompletion(app)

    if not app.game1On:
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        drawLabel('Your first key fragment lies', 
                app.width / 2 , app.height / 2 - 60, 
                size=20, font='monospace', fill = 'white', bold = True, align = 'left')
        
        drawLabel('at the end of this cave', 
                app.width / 2 , app.height / 2 - 40, 
                size=20, font='monospace', fill = 'white', bold = True, align = 'left')

        drawLabel('Be careful, the failure of this quest', 
                app.width / 2, app.height / 2 ,  
                size=15, font='monospace', fill='white', align = 'left')
        
        drawLabel('will send you back to the portals,', 
                app.width / 2, app.height / 2 + 20,  
                size=15, font='monospace', fill='white', align = 'left')

        drawLabel('where you will have to', 
                app.width / 2 , app.height / 2 + 40,  
                size=15, font='monospace', fill='white', align = 'left')

        drawLabel('start this journey again.', 
                app.width / 2 , app.height / 2 + 60,  
                size=15, font='monospace', fill='white', align = 'left')
        drawImage('wizard1.png', app.width/2 - 300, app.height/2 - 160,  width = 254, height = 304)
        
        drawLabel('Press any KEY to start the game', app.width/2, app.height/2 + 200, size = 25, font = 'monospace', fill = 'white', bold = True)
        drawCompletion(app)

def drawgame2(app):
    drawImage('rock_background.png', 0, 0, width = app.width, height = app.height)
    app.player2.drawGrid()
    x = app.playerCol * app.player2.cellSize + app.player2.cellSize / 2
    y = app.playerRow * app.player2.cellSize + app.player2.cellSize / 2
    drawImage(app.game2character, x, y, width = 40, height = 40, align = 'center')

    keyX = (app.player2.cols - 1) * app.player2.cellSize + app.player2.cellSize / 2
    keyY = (app.player2.rows - 1) * app.player2.cellSize + app.player2.cellSize / 2
    drawImage(app.key, keyX, keyY, width=30, height=30, align='center')

    drawMazeCompletion(app)

    if app.game2speechStart:
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        drawRect(app.width / 2 , app.height / 2 - 200, app.width, 200, fill = 'black', opacity = 50, align = 'center' )
        drawLabel(app.game2speeches[app.game2speechcount], app.width / 2, app.height / 2 - 225, font = 'monospace', size = 18, fill = 'white', bold = True)
        drawLabel('[click SPACE to continue]', app.width / 2, app.height / 2 - 150, font = 'monospace', size = 20, fill = 'white')
        drawImage('wizard1.png', app.width/2 , app.height/2 + 160,  width = 254, height = 304, align = 'center')
    
def drawgame3(app):
    app.player3.drawMap(app)
    app.player3.drawBridge(app)
    app.player3.drawPlayer(app)

    if app.game3speechStart:
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        drawRect(app.width / 2 , app.height / 2 - 200, app.width, 200, fill = 'black', opacity = 50, align = 'center' )
        drawLabel(app.game3speeches[app.game3speechcount], app.width / 2, app.height / 2 - 225, font = 'monospace', size = 18, fill = 'white', bold = True)
        drawLabel('[click SPACE to continue]', app.width / 2, app.height / 2 - 150, font = 'monospace', size = 20, fill = 'white')
        drawImage('wizard1.png', app.width/2 , app.height/2 + 160,  width = 254, height = 304, align = 'center')

def drawEnding(app):
    
    color = rgb(68, 30, 10)
    drawImage(app.startingbackground, 0, 0, width = app.width, height = app.height)
    drawRect(0, 0, app.width, app.height, fill = color, opacity = 50)

    drawOval(app.width / 2, app.height / 2, 600, 500, fill = 'red' , opacity = 10)
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 60)
    drawImage(app.charactermovefront[app.endingcount % 2], app.width / 2 , app.endingy, width = 75, height = 125, align = 'center')
    drawImage(app.vignette, app.width/2, app.height/2, width=app.width, height=app.height, align='center', opacity = 100)

def onKeyPress(app, key):
    if app.starting and app.speechDone:
        app.starting = False
        app.mainpage = True
        app.showWelcomeOverlay = True

    elif app.starting:   
        if app.speechStart:
            if key == 'space':
                app.speechcount += 1
            if app.speechcount >= 11:
                app.speechStart = False
                app.speechDone = True

    elif app.showWelcomeOverlay:
        app.showWelcomeOverlay = False

    elif app.game1 and not app.player.gameOver1:
        if app.game1On:
            if not app.player.start:
                app.player.start = True
            elif key == 'space':
                app.player.jump()
        else:
            app.game1On = True

    if app.game2:
        if app.game2speechStart:
            if key == 'space':
                app.game2speechcount += 1
                if app.game2speechcount >= len(app.game2speeches):
                    app.game2speechStart = False
                    app.game2speechDone = True
        elif app.game2speechDone and not app.game2On:
            app.game2speechDone = False
            app.game2On = True
        elif app.game2On:
            row = app.playerRow
            col = app.playerCol
            cell = app.player2.maze[row][col]
            if (key == 'up' or key == "w") and not cell.walls['top']:
                app.playerRow -= 1
                app.game2character = app.game2characterchoices[1]
            elif (key == 'down' or key == 's') and not cell.walls['bottom']:
                app.playerRow += 1
                app.game2character = app.game2characterchoices[0]
            elif (key == 'left' or key == 'a') and not cell.walls['left']:
                app.playerCol -= 1
                app.game2character = app.game2characterchoices[3]
            elif (key == 'right' or key == 'd') and not cell.walls['right']:
                app.playerCol += 1
                app.game2character = app.game2characterchoices[2]

    if app.player2.gameOver2:
        app.player2.gameOver2 = False
        app.game2 = False
        restartMain(app)
        restartGame2(app)
        app.mainpage = True
    
    if app.player3.gameOver:
        app.player3.gameOver = False
        app.game3 = False
        restartMain(app)
        restartGame3(app)
        app.mainpage = True

    if app.playerRow == app.player2.rows - 1 and app.playerCol == app.player2.cols - 1:
        app.game2success = True
        app.game2pass = True
        return
    
   
    if app.game3:
        if app.game3speechStart:
            if key == 'space':
                app.game3speechcount += 1
                if app.game3speechcount >= len(app.game3speeches):
                    app.game3speechStart = False
                    app.game3speechDone = True
        elif app.game3speechDone and not app.game3On:
            app.game3On = True
            app.player3.randomizeCorrect(app)
            app.player3.startReveal()
        elif app.game3On and not app.game3success:
            if key in ['a', 'left']:
                app.player3.currentCol = 0
                app.player3.checkMove(app, 0)
            elif key in ['d', 'right']:
                app.player3.currentCol = 1
                app.player3.checkMove(app, 1)


    if app.player.gameOver1:
        app.player.gameOver1 = False
        app.game1 = False
        restartMain(app)
        restartGame1(app)
        app.mainpage = True
        
def onKeyHold(app, keys):
    if app.fadingOut1 or app.game1 or app.waitingAfterGame1:
        return
    
    app.backgroundmovingleft = False
    app.backgroundmovingright = False
    app.backgroundmovingup = False
    app.backgroundmovingdown = False

    bgWidth = 1600
    bgHeight = 1600

    if not app.starting and app.mainpage:
        if ('a' in keys or 'left' in keys) and app.backgroundx < (bgWidth + (app.width - bgWidth)):
            if not((app.backgroundy < 300 or app.backgroundy > 500) and app.backgroundx > 475):
                app.backgroundmovingleft = True
                app.characterdirection = app.charactermoveleft

            if app.backgroundx >= 675 and not app.fadingOut2 and app.game1pass:
                app.fadingOut2 = True
                app.fadeOpacity2 = 0 

        elif ('d' in keys or 'right' in keys) and app.backgroundx > (app.width * 2 - bgWidth)/2:
            if not((app.backgroundy < 300 or app.backgroundy > 500) and app.backgroundx < 315):
                app.backgroundmovingright = True
                app.characterdirection = app.charactermoveright

            if app.backgroundx <= 125 and not app.fadingOut1:
                app.fadingOut1 = True
                app.fadeOpacity1 = 0 
        
        elif ('s' in keys or 'down' in keys) and app.backgroundy > (app.height * 2 - bgHeight)/2:
            if not((app.backgroundx < 300 or app.backgroundx > 500) and app.backgroundy < 315):
                app.backgroundmovingdown = True
                app.characterdirection = app.charactermovefront

            if app.backgroundy <= 125 and not app.fadingOut4:
                app.fadingOut4 = True
                app.fadeOpacity4 = 0 

        elif ('w' in keys or 'up' in keys) and app.backgroundy < (bgHeight + (app.height - bgHeight)):
            if not((app.backgroundx < 300 or app.backgroundx > 500) and app.backgroundy > 460):
                app.backgroundmovingup = True
                app.characterdirection = app.charactermoveback
            
            if app.backgroundy >= 600 and not app.fadingOut3 and app.game2pass:
                app.fadingOut3 = True
                app.fadeOpacity3 = 0 

def onKeyRelease(app, key):
    if not app.starting and app.mainpage:
        if 'a' in key or 'left' in key:
            app.backgroundmovingleft = False
        if 'd' in key or 'right' in key:
            app.backgroundmovingright = False
        if 's' in key or 'down' in key:
            app.backgroundmovingdown = False
        if 'w' in key or 'up' in key:
            app.backgroundmovingup = False

def onStep(app):
    app.count += 1

    if app.mainpage:
        if app.count % 5 == 0:
            app.charactercount += 1

        if app.backgroundmovingleft:
            app.backgroundx += app.speed
        if app.backgroundmovingright:
            app.backgroundx -= app.speed
        if app.backgroundmovingdown:
            app.backgroundy -= app.speed
        if app.backgroundmovingup:
            app.backgroundy += app.speed

    if app.game1 and app.game1On and not app.game1success:
        app.player.updatePlatforms(app)
        app.game1counter += 1
        if app.game1counter >= 1500:
            app.game1success = True
            app.game1pass = True
    
    if app.game2 and app.game2On:
        app.mazecompletion -= 5
        if app.mazecompletion <= 0 and not app.game2success:
            app.player2.gameOver2 = True
        
        

    if app.game1success:
        app.keycounter += 1
        app.waitingAfterGame1 = True
        if app.keycounter >= 160:
            app.waitingAfterGame1 = False
            app.game1 = False
            restartMain(app)
            restartGame1(app)
            app.mainpage = True
            app.game1success = False
            app.keycounter = 0

    if app.game2success:
        app.keycounter += 1
        app.waitingAfterGame2 = True
        if app.keycounter >= 60:
            app.waitingAfterGame2 = False
            app.game2 = False
            app.game2On = False
            restartMain(app)
            restartGame2(app)
            app.mainpage = True
            app.game2success = False
            app.keycounter = 0

    if app.game3success:
        app.keycounter += 1
        app.waitingAfterGame3 = True
        if app.keycounter >= 160:
            app.waitingAfterGame3 = False
            app.game3 = False
            app.game3On = False
            restartMain(app)
            restartGame3(app)
            app.mainpage = True
            app.game3success = False
            app.keycounter = 0
   

    if app.fadingOut1:
        app.fadeOpacity1 += 20  
        if app.fadeOpacity1 >= 100:
            app.fadeOpacity1 = 100
            app.fadingOut1 = False
            app.mainpage = False
            app.game1 = True
    
    if app.fadingOut2:
        app.fadeOpacity2 += 20  
        if app.fadeOpacity2 >= 100:
            app.fadeOpacity2 = 100
            app.fadingOut2 = False
            app.mainpage = False
            app.game2 = True
    
    if app.fadingOut3:
        app.fadeOpacity3 += 20  
        if app.fadeOpacity3 >= 100:
            app.fadeOpacity3 = 100
            app.fadingOut3 = False
            app.mainpage = False
            app.game3 = True

    if app.fadingOut4:
        app.fadeOpacity4 += 20  
        if app.fadeOpacity4 >= 100:
            app.fadeOpacity4 = 100
            app.fadingOut4 = False
            app.mainpage = False
            app.ending = True

    if app.starting and app.wizardWalkingIn:
        app.wizardy += app.wizardSpeed
        if app.wizardy >= app.wizardTargetY:
            app.wizardy = app.wizardTargetY
            app.wizardWalkingIn = False
            app.speechStart = True
    
    if app.starting:
        if app.count % 10 == 0:
            app.wizardcount += 1

    if app.ending:
        if app.count % 10 == 0:
            app.endingcount += 1
        app.endingy += 4
        if app.endingy >= app.height/2:
            app.endingy = app.height/2
            app.drawCrown = True
            

    if app.game3On: 
        app.player3.updateGlow(app)

    
def main():
    runApp()

main()
