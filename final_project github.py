from cmu_graphics import *
import random
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
    
    app.urlbackgroundmain = 'tiles.png'
    app.urlwood = 'planks.png'
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

    app.game2 = False
    app.game2pass = False
    app.game3 = False
    app.game3pass = False
    app.game4 = False
    app.gameOver = False

    app.fadeOpacity = 0
    app.fadingOut = False

    app.waitingAfterGame1 = False

                
