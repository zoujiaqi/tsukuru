# The following Code Tsukuru is a CNC printer/cutter powered by Nintendo Switch emulator
# The software is composed of User Interface that would go onto Nintendo Switch's console
# Coded in Python and has Design / Fabrication / Experience features built-in
# Tsukuru App is developed at #NewHuamnHACKS @ HP Inc. Vancouver, Washington 
# Author: Jiaqi Zou (jiaqi.zou@hp.com)
# Co-author: Kirielle Singarajah (kirielle.singarajah@hp.com), Connie Fan (connie.fan@hp.com)

import sys, pygame
from pygame.locals import *
import os, math, random



class introScreen:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tsukuru: CNC Printer/Cutter Routing Algorithm Emulator') #Title


        #color panel and color schemes in RGB
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (200,0,0)
        self.light_red = (255,0,0)
        self.YELLOW = (200,200,0)
        self.light_yellow = (255,255,0)
        self.GREEN = (34,177,76)
        self.light_green = (22,222,105)
        self.BLUE = (67,94,132)
        self.light_blue = (114,203,255)
        self.COFFEE = (127,96,57)
        self.light_coffee = (229,173,103)
        self.CYAN = (54,104,127)
        self.light_cyan = (129,208,255)
        self.WINE = (127,0,0)
        self.light_wine = (229,0,0)
        self.JADE = (19,64,50)
        self.light_jade = (76,255,201)
        self.MORRON = (64, 48, 64)
        self.light_morron = (255, 192, 255)
        self.HP_BLUE = (20, 48, 64)
        self.light_hp_blue = (40, 95, 220)

        #speech recognition text
        self.recogText = ""
        self.gestTXT = ""
        self.isSpeaking = False
        self.isEndSpeech = False
        self.isGesturing = False
        self.inEndGesturing = False


        #program font panel
        self.font = pygame.font.SysFont("Bukhari Script", 20)
        self.smallfont = pygame.font.SysFont("Bukhari Script", 25)
        self.medfont = pygame.font.SysFont("Bukhari Script", 50)
        self.largefont = pygame.font.SysFont("Bukhari Script", 85)

        #program mouse control panel
        self.QUIT = False
        self.mousebutton = None
        self.mousedown = False
        self.mouse_buttons = ["Left Button","Middle Button","Right Button","Wheel Up","Wheel Down"]

        #clock declaration
        self.clock = pygame.time.Clock()

        #initialize system
        self.initialize()


       
    def initialize(self):

        #Setup the pygame screen
        self.screen_width = 1280
        self.screen_height = 720
        # self.screen_width = 375
        # self.screen_height = 667
        self.screen_size = (self.screen_width, self.screen_height)    
        self.screen = pygame.display.set_mode(self.screen_size)

        #setup a generic drawing surface/canvas
        self.canvas = pygame.Surface((self.screen_width, self.screen_height))


        # Load the image source for buttons
        self.bg = pygame.image.load("pics/intro_bg.png")
        self.bg_clean = pygame.image.load("pics/bg_clean.png")
        self.design_icon = pygame.image.load("pics/design_icon.png")
        self.fab_icon = pygame.image.load("pics/fab_icon.png")
        self.exp_icon = pygame.image.load("pics/exp_icon.png")
        self.back_icon = pygame.image.load("pics/back.png")

        # Make all the buttons objects 
        self.designbutton = pygame.transform.scale(self.design_icon, (130,130))
        self.fabbutton = pygame.transform.scale(self.fab_icon, (135,135))
        self.expbutton = pygame.transform.scale(self.exp_icon, (128,128))
        self.back_button = pygame.transform.scale(self.back_icon,(40,40))

    def record_audio(self):
        
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if(self.isSpeaking == True):
                print("Say something!")
                audio = r.listen(source)
            else:
                r.stop()

        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`

            self.recogText = r.recognize_google(audio)
            print("You said: " + self.recogText)
        except sr.UnknownValueError:
            print("Could not understand audio")
            self.recogText = "Could not understand audio"
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            self.recogText = "Could not request results from Google Speech Recognition service; {0}".format(e)



    #mouse handler takes care of all the mouse events 
    def mouse_handler(self,event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mousedown = True
            self.mousebutton = event.button  
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mousedown = False
            self.mousebutton = event.button

        self.mouseX, self.mouseY = pygame.mouse.get_pos()
 
        self.show_mousestate()

    #shows the position of the mouse and it's press state
    def show_mousestate(self):
        """Show the mouse position and button press on the screen"""
        if self.mousebutton and self.mousedown:
            info = "Mouse: "+str(self.mouse_buttons[self.mousebutton-1])
        else:
            info = "Mouse: "
        info += "X= "+str(self.mouseX)+" Y: "+str(self.mouseY)

        #NB: for now we clear the canvas with black
        self.canvas.fill(self.BLACK)

        #load font and blit to canvas
        font = pygame.font.Font(None, 20)        
        textimg = font.render(info, 1, self.WHITE)
        self.canvas.blit(textimg, (10, 10))


    # draw general stuff the doesn't need to repaint 
    def draw(self):
        """We use a generic surface / Canvas onto which we draw anything
           Then we blit this canvas onto the display screen"""
        self.screen.blit(self.bg, (0, 0))

        #creating the button objects
        self.button("Design", 465,595,70,70, self.JADE, self.light_jade, action="design")
        self.button("Fabrication", 667,598,70,70, self.MORRON, self.light_morron, action="fab")
        self.button("Experience", 865,595,70,70, self.HP_BLUE, self.light_hp_blue, action="exp")

        #display on the screen
        self.screen.blit(self.designbutton, (400, 530))
        self.screen.blit(self.fabbutton,    (600, 530))
        self.screen.blit(self.expbutton,    (800, 530))

    # customized button class (the main splashscreen and levelSelect all share 
    # one button class to maximize code reuse)
    def button(self, text, x, y, width, height, inactive_color, active_color, action = None):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if(abs(cur[0]-x)<width and abs(cur[1]-y)<height):
            
            pygame.draw.circle(self.screen, active_color, (x,y), width)
            if click[0] == 1 and action != None:
                
                # Action ID for the Intro Screens
                if action == "quit":
                    pygame.quit()
                    quit()

                if action == "design":
                    self.designScreen()
                    print("This is Design Mode")

                if action == "fab":
                    self.fabricationScreen()
                    
                    print("This is Fabrication Mode")

                if action == "exp":
                    self.experienceScreen()
                    
                    print("This is Experience Mode")

                # Back button action ID from each Mode
                if action == "backFromDesign":
                    print("This is back")
                    myWelcomScreen = introScreen()
                    myWelcomScreen.run()

                if action == "backFromFab":
                    print("This is back")
                    myWelcomScreen = introScreen()
                    myWelcomScreen.run()

                if action == "backFromExp":
                    print("This is back")
                    myWelcomScreen = introScreen()
                    myWelcomScreen.run()

                
        else:
            # the button returns to the unselected state
            pygame.draw.circle(self.screen, inactive_color, (x,y), width)


    # helper function to format text objects 
    def text_objects(self, text, color,size = "small"):

        if size == "small":
            textSurface = self.smallfont.render(text, True, color)
        if size == "medium":
            textSurface = self.medfont.render(text, True, color)
        if size == "large":
            textSurface = self.largefont.render(text, True, color)

        return textSurface, textSurface.get_rect()

    # helper function to fomat button 
    def text_to_button(self, msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
        textSurf, textRect = self.text_objects(msg,color,size)
        textRect.center = (buttonx, buttony)
        self.screen.blit(textSurf, textRect)

    # helper function to format text
    def message_to_screen(self,msg,color, y_displace = 0, size = "small"):
        textSurf, textRect = self.text_objects(msg,color,size)
        textRect.center = (int(1300 / 2), int(700 / 2)+y_displace)
        self.screen.blit(textSurf, textRect)

    # design mode allows user to design a shape to be printed / cut
    def designScreen(self):

        gcont = True
        while gcont:
            for event in pygame.event.get():
                    #print(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()


            self.screen.blit(self.bg_clean, (0,0))     
            
            self.button("back", 155,645,150,150, self.WINE, self.light_wine, action="backFromDesign")
            # self.button("Speak", 73,490,46,46, self.CYAN, self.light_cyan, action="speak")      

            listenScreenText = self.largefont.render("Design Mode",True, self.WHITE)

            self.screen.blit(self.back_icon, (35, 528))

            self.screen.blit(listenScreenText, [400,30])
            pygame.display.update()

            self.clock.tick(15)

    # Fabrication Mode uses graphical / geometry based algorithms to solve path planning for routers
    def fabricationScreen(self):
        gcont = True

        while gcont:
            for event in pygame.event.get():
                    #print(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            
            self.screen.blit(self.bg_clean, (0,0))     
            
            self.button("back", 155,645,150,150, self.WINE, self.light_wine, action="backFromFab")
            # self.button("Speak", 73,490,46,46, self.CYAN, self.light_cyan, action="speak")      

            listenScreenText = self.largefont.render("Fabrication Mode",True, self.WHITE)

            self.screen.blit(self.back_icon, (35, 528))

            self.screen.blit(listenScreenText, [300,30])
            
            pygame.display.update()

            self.clock.tick(15)

    # Experience Modes is for user to see what is capable of Nintendo Switch 
    def experienceScreen(self):
        gcont = True

        while gcont:
            for event in pygame.event.get():
                    #print(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            self.screen.blit(self.bg_clean, (0,0))     
            
            self.button("back", 155,645,150,150, self.WINE, self.light_wine, action="backFromExp")
            # self.button("Speak", 73,490,46,46, self.CYAN, self.light_cyan, action="speak")      

            listenScreenText = self.largefont.render("Experience Mode",True, self.WHITE)

            self.screen.blit(self.back_icon, (35, 528))

            self.screen.blit(listenScreenText, [300,30])

            

            pygame.display.update()

            self.clock.tick(15)

    # This is the main run function of the splashscreen
    def run(self):
        """This method provides the main application loop.
           It continues to run until either the ESC key is pressed
           or the window is closed
        """
        while True:
            
            events = pygame.event.get()
            for e in events:
                #pass event onto mouse handler only if something happens
                self.mouse_handler(e)
                
                #Set quit state when window is closed
                if e.type == pygame.QUIT :
                    self.QUIT = True
                if e.type == KEYDOWN:
                    #Set quit state on Esc key press
                    if e.key == K_ESCAPE:
                        self.QUIT = True
                                    
            if self.QUIT:
                #Exit pygame gracefully
                pygame.quit()
                sys.exit(0)

            #Process any drawing that needs to be done
            self.draw()

            #flip the display
            pygame.display.flip()

if __name__ == "__main__":
    myWelcomScreen = introScreen()
    myWelcomScreen.run()

        