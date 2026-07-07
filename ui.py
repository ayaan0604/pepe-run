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
            bd = 10
        )
       

        self.backgroundImage = ImageLabel(
            self,
            "assets/playareaBG.png",
            int(width-25),
            int(height-25)
        )

        self.backgroundImage.place(x = 0, y = 0)


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

        self.playwidth=self.windowWidth*0.95
        self.playHeight=self.windowHeight*0.74

        self.controlHeight=self.windowHeight*0.19
        self.controlWidth=self.windowWidth*0.4

class Ui:
    def __init__(self):
        
        self.screen = Screen()

        self.pepe = None
        
        self.window = App(self.screen.windowWidth, self.screen.windowHeight, "Pepe Run")

        

    def random_x(self):
        return int(random.random()*(self.screen.playwidth-100))
    

    
    def setup_play_area(self):
        
        self.playArea = PlayArea(self.window, self.screen.playwidth, self.screen.playHeight)
        self.playArea.place(x=20,y=20)

        #setup pepe
        self.pepe= Pepe(self.playArea, self.screen)
        self.pepe.place()
    
   
       

    def setup_bottom_area(self):
         #frame for control area
        self.bottomArea = BottomArea(self.window, self.screen.windowWidth, self.screen.controlHeight)
        self.bottomArea.place(x=0,y=self.screen.windowHeight - self.screen.controlHeight)

        

    def setup_score_counter(self):
        score_counter=Frame(self.window,width=200,height=40,bg="black")
        score_counter.place(x=0,y=0)
        score_text=Label(score_counter,text="Score: ",font=("Komika Axis",15,"bold"),bg="black",fg="yellow")
        self.score_number=Label(score_counter,text="0",font=("Komika Axis",15,"bold"),bg="black",fg="yellow")
        score_text.place(x=0,y=0)
        self.score_number.place(x=80,y=0)

    def setup_life_counter(self):
         #life counter
        life_counter=Frame(self.window,width=100,height=40,bg="black")
        life_counter.place(x=self.screen.windowWidth-100,y=0)
        self.life_text=Label(life_counter,text="🩷"*self.pepe.maxLives,font=("Arial",20),bg="black", fg="red")
        self.life_text.place(x=0,y=0)

    def setup_gameover_screen(self):
        #gameoverscreen
        self.game_over_frame=Frame(self.window,width=500,height=300,bd=10,relief=RAISED)
        self.game_over_frame.place(x=self.screen.windowWidth/2-250,y=self.screen.windowHeight/2-200)

        self.gameover_image_raw=Image.open("assets/gameOver.png")

        self.gameover_image_resized=ImageTk.PhotoImage(self.gameover_image_raw.resize((470,275)))

        self.gameover_popup=Label(self.game_over_frame,image=self.gameover_image_resized)

        #restart button
        self.restart_button=Button(self.game_over_frame,
                            text="Restart",
                            bg="#000000",
                            fg="#28ed38",
                            font=("Lucida Console",15,"bold"),
                            width=15,
                            height=1,
                            bd=0,
                            relief=RAISED)

        #restart_button.config(command=restart)
        # self.game_over_frame.bind("<Return>",restart)

        #score place
        self.score_display=Label(self.game_over_frame,text="0",
                            width=10,
                            height=1,
                            font=("Komika Axis",15,"bold"),
                            bg="#151552",
                            padx= 1,
                            pady= 1,
                            fg="white"
                            )

        self.gameover_popup.place(x=0,y=0)
        self.restart_button.place(x=55,y=210)
        self.score_display.place(x=100,y=107)

        self.game_over_frame.lower()


   

    def setup_ui(self):
        
        
        self.setup_play_area()

        self.setup_bottom_area()

        self.setup_score_counter()

        self.setup_life_counter()



        self.setup_gameover_screen()

        

        
    
       


        

       

       

        
if __name__ == "__main__":
    myui = Ui()
    myui.setup_ui()

   
    frame = imread("assets/preview.png")
    print(frame)

    myui.window.after(
        100,
        lambda: myui.bottomArea.cam.update_camera(frame)
    )

    

    myui.window.mainloop()

    