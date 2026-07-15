import random
from tkinter import *
from PIL import Image, ImageTk
from components.pepe import Pepe
from cv2 import resize, cvtColor, COLOR_BGR2RGB, imread


class ImageLabel(Label):
    def __init__(self,parent,  location, width, height):
        

        rawImg=Image.open(location)
        resizedImg= rawImg.resize((width, height))
        self.img=ImageTk.PhotoImage(resizedImg)
        
        super().__init__(parent, image = self.img)

class PlayArea(Frame):

    def __init__(self, parent, width, height):
        super().__init__(
            parent,
            width = width,
            height = height,
            relief = RAISED,
            bd = 4,
            bg= "black"
        )
       

        self.backgroundImage = ImageLabel(
            self,
            "assets/playareaBG.png",
            int(width-12),
            int(height-12)
        )

        self.backgroundImage.place(relx = 0, rely = 0)


class ControlButtons(Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent, width = width, height= height, bg= "black", relief= SUNKEN)

        #button config
        self.rightButton=Button(self,text="➡️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
        self.leftButton=Button(self,text="⬅️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
        self.upButton=Button(self,text="⬆️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
        self.downButton=Button(self,text="⬇️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)

        #button placemnet
        self.upButton.grid(row = 0, column = 1, sticky = "nsew")
        self.rightButton.grid(row = 1, column = 2, sticky = "nsew")
        self.leftButton.grid(row = 1, column = 0, sticky = "nsew")
        
        self.downButton.grid(row = 1, column = 1, sticky = "nsew")

        self.buttons_list = [self.rightButton, self.leftButton, self.upButton, self.downButton]
    
    def set_commands(self, left, right, up, down):
        
        if left:
            self.leftButton.config(command = left)

        if right:
            self.rightButton.config(command = right)

        if up:
            self.upButton.config(command = up)
        if down:
            self.downButton.config(command = down)
        

        
class BottomArea(Frame):
    def __init__(self, parent, width, height):
        super().__init__(
            parent,
            width = width,
            height= height,
            bd = 10,
            relief = SUNKEN,
            bg = "black"
        )

        #camera
        self.cam = Cam(self, width*0.25, height*0.85)
        self.cam.place(relx = 0, x = 10 , y = 0)

        

        #controls buttons
        self.controlButtons = ControlButtons(self, width*0.4, height)
        self.controlButtons.place(relx = 1, x = -10, y = 0, anchor = "ne")
        



class Cam(Frame):
    def __init__(self, parent, width, height):

        super().__init__(
            parent,
            width = width,
            height = height,
            bg="black",
            
        )

        self.imageLabel = Label(self, bg =  "black", bd=3, relief="ridge")
        self.imageLabel.place(relx= 0, rely= 0, relwidth = 0.7, relheight=1)

        self.textLabel = Label(
            self,
            bg="black",
            fg = "white",
            text= "Right",
            bd=3,
            font=( "Montserrat", 12)
        )
        self.textLabel.place( relx = 0.7, rely = 0.7, anchor= "nw")

        self.photo = None
    
    
    
    def update_camera(self, frame):

        w = self.winfo_width()
        h = self.winfo_height()

        
        frame = cvtColor(frame, COLOR_BGR2RGB)

        frame = resize(frame, (w, h))

        img = Image.fromarray(frame)

        img = ImageTk.PhotoImage(image=img)

        self.photo = img
        self.imageLabel.config(image = self.photo)
    
    def disableCam(self):
        self.imageLabel.config(
            image="",
            bg = "black",
            text= "Camera Disabled",
            fg = "white")
    
    def setText(self, text):
        self.textLabel.config(text= text)

class TopArea(Frame):
    def __init__(self,parent, width, height):
        super().__init__(
            parent,
            width = width,
            height = height,
            relief = SUNKEN,
            bd = 5,
            bg = "black"
        )

        self.highScoreLabel = Label(
            self, 
            text = "High Score: 0",
            bg = "black",
            fg = "#e3e3e3",
            font = ("Georgia", 10, "bold")
        )
        

        self.scoreLabel = Label(
            self, 
            text = "Score: 0",
            bg = "black",
            fg = "yellow",
            font = ("Georgia", 15, "bold")
        )


        self.lifeLabel = Label(
            self, 
            text = "🥀",
            bg = "black",
            fg = "red",
            font = ("Georgia", 15, "bold")
        ) 


        self.highScoreLabel.place(relx = 0, rely=0.2, x = 10)
        self.scoreLabel.place(relx = 0.5, rely = 0.5, anchor="center")
        self.lifeLabel.place(relx = 1, rely = 0, x = -10, anchor = "ne")

    def updateHighScore(self, score):
        self.highScoreLabel.config(text= f"High Score: {score}")
    
    def update_score(self, score):
        self.scoreLabel.config(text = f"Score: {score}")
    
    def update_lives(self, count):
        self.lifeLabel.config(text = "🩷" * count)


class GameOverScreen(Frame):
    def __init__(self, parent, width, height):
        super().__init__(
            parent,
            width = width,
            height = height,
            bd = 2,
            relief = RAISED
        )

        self.backgroundImage = ImageLabel(
            self,
            location = "assets/gameOver.png",
            width = width-10,
            height = height-10
        )
        self.backgroundImage.place(x=0 ,y = 0)


        

        # #restart button
        self.restartButton=Button(self,
                            text="Restart",
                            bg="#022211",
                            fg="#28ed38",
                            font=("Lucida Console",18,"bold"),
                            width= int(width * 0.025),
                            bd = 0
                           
                            )


        #score place
        self.score_display=Label(self,text="0",
                            width=10,
                            height=1,
                            font=("Komika Axis",15,"bold"),
                            bg="#011228",
                            padx= 1,
                            pady= 1,
                            fg="white"
                            )

        self.quitButton = Button(self,
            text = "Quit",
            bg="#080717",
            fg="#e8e8e8",
            font=("Lucida Console",10,"bold"),
            bd = 2
        )
        self.menuButton = Button(self,
            text = "Main Menu",
            bg="#080717",
            fg="#e8e8e8",
            font=("Lucida Console",10,"bold"),
            width= int(width * 0.025),
            bd = 2
        )

        self.restartButton.place(relx=0.33, rely=0.805, anchor = "center")
        self.score_display.place(relx=0.19,rely=0.43)
        self.menuButton.place(relx = 0.10, rely = 0.89)
        self.quitButton.place(relx = 0.4, rely = 0.89)

        self.lower()

    def show(self, score):
        self.score_display.config(text = f'{score}')
        self.lift()
    
    def hide(self):
        self.lower()
    
    def set_button_commands(self, restart = None, menu = None, quit = None):
        if restart:
            self.restartButton.config(command= restart)
        if menu:
            self.menuButton.config(command= menu)
        if quit:
            self.quitButton.config(command= quit)

class DropDown(Frame):
    def __init__(self, parent, width, height, options):
        super().__init__(
            master= parent,
            width= width,
            height= height,
            bg = "#020810",
            relief= FLAT,
        )

        self.optionText = Label(
            master= self,
            bg = "#020810",
            fg = "yellow",
            font= ("Montserrat", 8, "bold"),
            anchor="w"
        )
        self.optionText.config(text= "Select An Option")

        
        self.dropDown = None
        

        self.optionText.place(relx= 0, rely = 0, relwidth=0.9)

            
    
    def setText(self, text):
        self.optionText.config(text = text)

    def getSelected(self):
        return self.selectedOption.get()
    
    def createDropdown(self, options):

        if self.dropDown:
            self.dropDown = None
        
        self.selectedOption = StringVar(self)
        self.selectedOption.set(options[0])

        self.dropdown =  OptionMenu(
            self,
            self.selectedOption,
            *options,

        )
        self.dropdown.config(
            bg ="green",
            fg = "green",
            relief= FLAT,
            text= "↓"
        )
        self.selectedOption.trace_add("write", lambda *args: self.setText(self.selectedOption.get()))

        self.dropdown.place(relx = 0.85, rely = 0, relwidth= 0.15, relheight=0.9)
    
    def disableDropDown(self):
        if self.dropDown:
            self.dropDown.config(state = DISABLED)
        self.optionText.config(fg = "grey")
            

    def enableDropDown(self):
        if self.dropDown:
            self.dropDown.config(state = NORMAL)
            
        self.optionText.config(fg = "yellow")


        
class SettingsMenu(Frame):
    def __init__(self, parent, width, height):
        super().__init__(
            master= parent,
            width= width,
            height= height,
            bd = 0,
            bg = "black"
        )

        self.background = ImageLabel(self, "assets/settings.png", width, height+1)
        self.background.place(relx = 0.5, rely = 0.5, anchor= "center")

        self.volumebar = Scale(
            self,
            from_ = 0,
            to = 100,
            orient= "horizontal",
            length= 345,
            fg = "#000000",
            bg = "#0D5C0D",
            bd = 0,
            troughcolor= "#020810",
            highlightbackground= "#0D5C0D",
            width= 30,
           
        )
        
        self.volumeLabel = Label(
            self, 
            fg = "yellow",
            bg = "#020810",
            text = "50",
            font= ("Montserrat", 20, "bold"),
            padx = 10
        )
        
        self.crossButton = Button(
            self,
            text= "X",
            fg= "#d0351a",
            bg = "#000912",
            font= ("Lucida Console",16,"bold"),
            bd = 0,
            padx=0,
            pady=0,
            borderwidth=0,
            highlightthickness=0,
            command= lambda : self.lower()
        )

        self.enableButton = Button(
            self,
            text= "Enable Camera",
            fg = "#11C911",
            bg = "#020810",
            bd = 1,
            font= ( "Montserrat", 10, "bold"),
            padx = 20, pady = 0,
            relief= FLAT
        )

        self.dropdown = DropDown(
            self,
            width= int(width* 0.3),
            height= int(height* 0.1),
            options= ["1", "2", "3"]
        )

        self.backButton = Button(
            self,
            text= "Back",
            fg = "#269926",
            bg = "#020810",
            bd = 1,
            font= ( "Montserrat", 8, "bold"),
            padx = 20, pady = 0,
            relief= FLAT,
            command= lambda: self.lower()
        )
    

    
        self.volumebar.place(relx = 0.51, rely = 0.26, anchor="center")
        self.volumebar.set(50)

        self.volumeLabel.place(relx= 0.89, rely= 0.27, anchor= "center")
        self.crossButton.place(relx = 0.925, rely =0.0835, anchor="center")

        self.enableButton.place(relx = 0.3, rely = 0.535, anchor="center")

        self.dropdown.place(relx = 0.09, rely= 0.68, relheight=0.07, relwidth=0.37)
        self.backButton.place(relx = 0.45, rely = 0.9)

    def show(self):
        self.lift()
    
    def setVolumeText(self, text):
        self.volumeLabel.config(text = text)

    def setCommands(self, volumeBar = None, enable = None):
        if volumeBar:
            self.volumebar.config(command= volumeBar)
        if enable:
            self.enableButton.config(command=enable)
        
    def setEnableButtonText(self, text):
        self.enableButton.config(text= text)
    
    

            
class MainMenu(Frame):
    def __init__(self, parent, width, height):
        super().__init__(master=parent, width=width, height=height, bd = 5, relief=RAISED, bg = "black")

       

        self.background = ImageLabel(self, "assets/main_menu.png", width=width-10, height=height-10)
        self.background.place(relx = 0.5, rely=0.5, anchor="center")

        self.playButton = Button(self,
            text = "PLAY",
            bg="black",
            fg="#0AAD0A",
            font=("Lucida Console",14,"bold"),
            bd = 0
            
        )

        self.settingsButton = Button(self,
            text = "SETTINGS",
            bg="black",
            fg="#0d3876",
            font=("Lucida Console",14,"bold"),
            bd = 0
        )

        self.helpButton = Button(self,
            text = "HELP",
            bg="black",
            fg="#0d3876",
            font=("Lucida Console",13,"bold"),
            bd = 0
        )

        self.helpButton = Button(self,
            text = "HELP",
            bg="black",
            fg="#0d3876",
            font=("Lucida Console",13,"bold"),
            bd = 0
        )

        self.quitButton = Button(self,
            text = "QUIT",
            bg="black",
            fg="#0d3876",
            font=("Lucida Console",13,"bold"),
            bd = 0
        )


        self.playButton.place(relx=0.55, rely=0.44, anchor="center")
        self.settingsButton.place(relx=0.55, rely=0.555, anchor="center")
        self.helpButton.place(relx=0.55, rely=0.67, anchor="center")
        self.quitButton.place(relx=0.55, rely=0.784, anchor="center")

    def show(self):
        self.lift()
    
    def hide(self):
        self.lower()
    
    def set_button_commands(self, play = None, settings = None, help= None, quit= None):
        if play:
            self.playButton.config(command=play)
        if settings:
            self.settingsButton.config(command=settings)
        if help:
            self.helpButton.config(command=help)
        if quit:
            self.quitButton.config(command=quit)

class HelpMenu(Frame):
    def __init__(self, parent, width, height):
        super().__init__(
            master=parent,
            height=height,
            width=width,
            bg= "black",
            relief=SUNKEN
        )

        self.background = ImageLabel(self, "assets/help_screen.png", height=height+1, width=width+1)
        self.background.place(relx=0.5, rely=0.5, anchor="center")

        self.crossButton = Button(
            self,
            text= "X",
            fg= "#d0351a",
            bg = "#050c14",
            font= ("Lucida Console",16,"bold"),
            bd = 0,
            padx=0,
            pady=0,
            borderwidth=0,
            highlightthickness=0
        )

        self.crossButton.place(relx = 0.925, rely =0.085, anchor="center")

    def set_button_command(self, cross = None):
        if cross:
            self.crossButton.config(command= cross)

    def show(self):
        self.lift()
    
    def hide(self):
        self.lower()



class App(Tk):
    def __init__(self, width, height, title):
        super().__init__()

        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.title(title)

        pepe=PhotoImage(file="assets/pepe.png")
        self.iconphoto(True,pepe)
        self.config(bg="black")
        



class Screen:
    def __init__(self):
        self.windowHeight=600
        self.windowWidth=900

        self.playwidth=self.windowWidth
        self.playHeight=self.windowHeight*0.74

        self.controlHeight=self.windowHeight*0.19
        self.controlWidth=self.windowWidth*0.4



class Ui:
    def __init__(self):
        
        self.screen = Screen()

        self.pepe = None
        
        self.window = App(self.screen.windowWidth, self.screen.windowHeight, "Pepe Run")

        #setup top bar
        self.topArea = TopArea(self.window, width = self.screen.windowWidth, height = self.screen.windowHeight*0.07)
        self.topArea.grid(row = 0, column = 0)

        #setup play Area
        self.playArea = PlayArea(self.window, self.screen.playwidth, self.screen.playHeight)
        self.playArea.grid(row = 1, column = 0)

        #setup pepe
        self.pepe= Pepe(self.playArea, self.screen)
        self.pepe.place()

        #setup bottom area
        self.bottomArea = BottomArea(self.window, self.screen.windowWidth, self.screen.controlHeight)
        self.bottomArea.grid(row = 2, column = 0)

        #gameover screen
        self.gameOver = GameOverScreen(self.window, int(self.screen.windowWidth*0.4), int(self.screen.playHeight*0.9))
        self.gameOver.grid(row = 1, column= 0)
        self.gameOver.lower()

        self.mainMenu = MainMenu(self.window, int(self.screen.playwidth*0.6), int(self.screen.playHeight*0.9) )
        self.mainMenu.grid(row=1, column=0)

        self.helpMenu = HelpMenu(self.window, int(self.screen.playwidth*0.6), int(self.screen.playHeight*0.9))
        self.helpMenu.grid(row=1, column=0)
        self.helpMenu.lower()
        

        self.settingsMenu = SettingsMenu(self.window, int(self.screen.playwidth*0.6), int(self.screen.playHeight*0.9))
        self.settingsMenu.grid(row = 1, column= 0)
        self.settingsMenu.lower()

    def random_x(self):
        return int(random.random()*(self.screen.playwidth-100))
    
       

        
if __name__ == "__main__":
    myui = Ui()
    
    myui.gameOver.lift()
    
    myui.window.mainloop()

    