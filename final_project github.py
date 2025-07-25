from cmu_graphics import *
import random

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

                
