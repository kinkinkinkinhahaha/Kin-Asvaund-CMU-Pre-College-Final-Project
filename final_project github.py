from cmu_graphics import *
import random
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

            
            if (self.vy < 0 and
                playerTop <= platformBottom and playerBottom > platformBottom and 
                playerRight > platformLeft and playerLeft < platformRight):
                self.y = platformBottom + 60
                self.vy = 0


            elif (self.vy >= 0 and
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
    app.castle = 'castle.png'
    app.vignette = 'vignette.png'
    app.startingbackground = 'startingbackground.png'
    app.key = 'keyIcons.png'
    app.opacity = 0

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
    app.game4 = False
    app.gameOver = False



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
            if app.showWelcomeOverlay:
                drawWelcomePage(app)
            if app.fadingOut1:
                drawRect(0, 0, app.width, app.height, fill='black', opacity=app.fadeOpacity1)
            if app.fadingOut2:
                drawRect(0, 0, app.width, app.height, fill='black', opacity=app.fadeOpacity2)


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
