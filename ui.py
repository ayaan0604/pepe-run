import random
from tkinter import *
from PIL import Image, ImageTk
from pepe import Pepe
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
            bd = 4
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
        self.cam = Cam(self, width*0.2, height*0.85)
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
            bd=3,
            relief="ridge"
        )

        self.imageLabel = Label(self, bg =  "red")
        self.imageLabel.place(relx= 0, rely= 0, relwidth = 1, relheight=1)

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

        self.scoreLabel.place(relx = 0, x= 10, rely = 0)
        self.lifeLabel.place(relx = 1, rely = 0, x = -10, anchor = "ne")
    
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
        self.restart_button=Button(self,
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
            font=("Lucida Console",12,"bold"),
            width= int(width * 0.025),
            bd = 2
        )

        self.restart_button.place(relx=0.33, rely=0.805, anchor = "center")
        self.score_display.place(relx=0.19,rely=0.43)
        self.quitButton.place(relx = 0.17, rely = 0.9)

        self.lower()

    def show(self, score):
        self.score_display.config(text = f'{score}')
        self.lift()
    
    def hide(self):
        self.lower()
        
    def set_restart(self, command):
        self.restart_button.config(command = command)

    def set_quit(self, command):
        self.quitButton.config(command = command)
        

            


class App(Tk):
    def __init__(self, width, height, title):
        super().__init__()

        self.geometry(f"{width}x{height}")
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
        self.gameOver = GameOverScreen(self.window, int(self.screen.windowWidth*0.4), int(self.screen.windowHeight*0.8))
        self.gameOver.place(relx = 0.5, rely = 0.5, anchor = "center")
        

    def random_x(self):
        return int(random.random()*(self.screen.playwidth-100))
    
   
        


   



       

        
if __name__ == "__main__":
    myui = Ui()
   
    myui.topArea.update_lives(4)
    myui.topArea.update_score(100)
    
    myui.window.mainloop()

    