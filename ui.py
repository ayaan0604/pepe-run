import random
from tkinter import *
from PIL import Image, ImageTk
from pepe import Pepe


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
        
        self.window = Tk()

        

    def random_x(self):
        return int(random.random()*(self.screen.playwidth-100))
    
    def setup_images(self):
        self.window.geometry(f"{self.screen.windowWidth}x{self.screen.windowHeight}")
        self.window.title("Pepe Run")
        
        #setup_images()
        pepe=PhotoImage(file="assets/pepe.png",height=self.screen.windowHeight,width=self.screen.windowWidth)

        self.window.iconphoto(True,pepe)
        self.window.config(bg="black")

        backgroundimg=Image.open("assets/playareaBG.png")
        resizedBgimg=backgroundimg.resize((self.screen.windowWidth,self.screen.windowHeight))
        self.bgimage=ImageTk.PhotoImage(resizedBgimg)
        self.bglabel=Label(image=self.bgimage)
        self.bglabel.place(x = 0, y = 0)
    
    def setup_play_area(self):
        #frame for play area
        playArea=Frame(self.window,width=self.screen.playwidth,height=self.screen.playHeight,bd=10,relief=RAISED)
        playArea.place(x=0,y=20)
        #bg for play area
        rawpabg=Image.open("assets/playareaBG.png")
        resizedpabg=rawpabg.resize((int(self.screen.playwidth-25),int(self.screen.playHeight-25)))
        self.playAreaBg=ImageTk.PhotoImage(image=resizedpabg)
        playAreaBglabel=Label(playArea,image=self.playAreaBg)
        playAreaBglabel.place(x=0,y=0)

        self.playArea = playArea
        #setup pepe
        self.pepe= Pepe(playArea, self.screen)
        self.pepe.place()
    
    def setup_buttons(self, control):
        #button config
        self.rightButton=Button(control,text="➡️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
        self.leftButton=Button(control,text="⬅️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
        self.upButton=Button(control,text="⬆️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
        self.downButton=Button(control,text="⬇️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)

        #button placemnet
        self.rightButton.place(x=self.screen.controlWidth*0.6,y=0.2*self.screen.controlHeight)
        self.leftButton.place(x=self.screen.controlWidth*0.25,y=0.2*self.screen.controlHeight)
        self.upButton.place(x=self.screen.controlWidth/2.3,y=0.01*self.screen.controlHeight)
        self.downButton.place(x=self.screen.controlWidth/2.3,y=0.45*self.screen.controlHeight)

    def setup_control_area(self):
         #frame for control area
        control=Frame(self.window,width=self.screen.controlWidth,height=self.screen.controlHeight,bd=10,relief=SUNKEN,bg="black")
        control.place(x=(self.screen.windowWidth/2-self.screen.controlWidth/2),y=self.screen.windowHeight*0.8)

        self.setup_buttons(control)

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
        
        self.setup_images()
        self.setup_play_area()

        self.setup_control_area()

        self.setup_score_counter()

        self.setup_life_counter()


        self.setup_gameover_screen()

        

        
    
       


        

       

       

        
if __name__ == "__main__":
    myui = Ui()
    myui.setup_ui()
    myui.window.mainloop()
